__author__ = 'Ben Haley & Ryan Jones'

import os
from energyPATHWAYS.demand import Demand
from energyPATHWAYS import util
from energyPATHWAYS.outputs import Output, compress_and_remove, special_shapes_export
import shutil
from energyPATHWAYS import config as cfg
import pandas as pd
import logging
import energyPATHWAYS.shapes2 as shapes2
import pdb
from energyPATHWAYS.scenario_loader import Scenario
import copy
import numpy as np
from energyPATHWAYS.geomapper import GeoMapper
from energyPATHWAYS import export_to_rio as ep2rio

class PathwaysModel(object):
    """
    Highest level classification of the definition of an energy system.
    """
    def __init__(self, scenario_id):
        self.scenario_id = scenario_id
        self.scenario = Scenario(self.scenario_id)
        cfg.scenario_name = scenario_id
        self.outputs = Output()
        self.demand = Demand(self.scenario)
        self.demand_solved = False

    def run(self, load_demand, export_results, save_models, shape_owner, scenario_id):
        self.scenario_id = scenario_id
        self.scenario = Scenario(self.scenario_id)
        cfg.scenario_name = scenario_id
        self.demand.scenario = self.scenario

        if os.path.isfile(os.path.join(cfg.workingdir, self.scenario_id, 'solved.true')):
            os.remove(os.path.join(cfg.workingdir, self.scenario_id, 'solved.true'))
        if os.path.isfile(os.path.join(cfg.workingdir, self.scenario_id, 'demand_outputs', '_clean_timeseries_debug.csv')):
            os.remove(os.path.join(cfg.workingdir, self.scenario_id, 'demand_outputs', '_clean_timeseries_debug.csv'))
        # self.scenario = Scenario(self.scenario_id)
        rio_scenario = self.scenario_id
        if shape_owner:
            if cfg.getParamAsBoolean('shape_check', section='CALCULATION_PARAMETERS'):
                shapes2.ShapePickler(cfg.getParam('database_path', section='DATABASE'))
            else:
                logging.warning('--SHAPES ARE ASSUMED GOOD AND ARE NOT BEING CHECKED--')
        shapes2.ShapeContainer(cfg.getParam('database_path', section='DATABASE'), self.scenario)
        self.rio_scenario = rio_scenario

        if not load_demand:
            self.calculate_demand(save_models)
            if os.path.isfile(os.path.join(cfg.workingdir, self.scenario_id, 'demand_outputs', '_clean_timeseries_debug.csv')):
                compress_and_remove(os.path.join(cfg.workingdir, self.scenario_id, 'demand_outputs', '_clean_timeseries_debug.csv'))

        ############ HELPER FLAG IF WE JUST WANT TO REDO THE SHAPES AFTER LOADING A DEMAND-SIDE PICKLE
        self.redo_shapes = True
        ############
        if load_demand and export_results and self.redo_shapes:
            # self.demand.aggregate_results()
            self.demand.electricity_reconciliation = None
            self.demand.pass_electricity_reconciliation()
            self.demand.output_subsector_electricity_profiles()

        if self.demand_solved and export_results:
            if cfg.getParamAsBoolean('ep2rio_prep', section='CALCULATION_PARAMETERS'):
                export = ep2rio.RioExport(self, shape_owner)
                export.write_all()
            self.export_result_to_csv()

            with open(os.path.join(cfg.workingdir, self.scenario_id, 'solved.true'), 'w'):
                pass

    def calculate_demand(self, save_models):
        self.demand.setup_and_solve()
        self.demand_solved = True
        if save_models:
            Output.pickle(self, file_name=str(self.scenario_id) + cfg.demand_model_append_name, path=os.path.join(cfg.workingdir, str(self.scenario_id)))

    def remove_old_results(self):
        folder = os.path.join(cfg.workingdir, self.scenario_id, 'demand_outputs')
        if os.path.isdir(folder):
            shutil.rmtree(folder, ignore_errors=True)

    def export_result_to_csv(self):

        def clean_and_write(result_df, attribute):
            """

            :param result_df: pandas dataframe
            :param attribute: string
            """
            result_df = pd.concat([result_df], keys=[self.scenario.name.upper()], names=['SCENARIO'])
            result_df = result_df.fillna(0)
            result_df = result_df.reorder_levels(sorted(result_df.index.names)).sort_index()
            Output.write(result_df, attribute + '.csv', os.path.join(cfg.workingdir, self.scenario_id, 'demand_outputs'), compression='gzip', append_when_existing=False)

        res_obj = self.demand.outputs
        for attribute in dir(res_obj):
            if self.redo_shapes and "_profiles" not in attribute:
                continue
            if cfg.getParamAsBoolean('dod_special_format_shapes_export', section='DEMAND_OUTPUT_DETAIL') and "_profiles" in attribute:
                df = getattr(res_obj, attribute)
                special_shapes_export(df, self.scenario_id)
                continue
            if isinstance(getattr(res_obj, attribute), list):
                for df in getattr(res_obj, attribute):
                    result_df = getattr(res_obj, 'clean_df')(df)
                    clean_and_write(result_df,attribute)
            elif isinstance(getattr(res_obj, attribute), pd.DataFrame):
                result_df = getattr(res_obj, 'clean_df')(getattr(res_obj, attribute))
                clean_and_write(result_df, attribute)
            else:
                continue
