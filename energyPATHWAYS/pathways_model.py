__author__ = 'Ben Haley & Ryan Jones'

import os
from energyPATHWAYS.demand import Demand
from energyPATHWAYS import util
from energyPATHWAYS.outputs import Output
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
        self.outputs = Output()
        self.demand = Demand(self.scenario)
        self.demand_solved = False

    def run(self, load_demand, export_results, save_models, shape_owner):
        if os.path.isfile(os.path.join(cfg.workingdir, self.scenario_id, 'solved.true')):
            os.remove(os.path.join(cfg.workingdir, self.scenario_id, 'solved.true'))
        self.scenario = Scenario(self.scenario_id)
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

        ############ HELPER FLAG IF WE JUST WANT TO REDO THE SHAPES AFTER LOADING A DEMAND-SIDE PICKLE
        self.redo_shapes = False
        self.special_shapes_write = False
        ############
        if load_demand and export_results and self.redo_shapes:
            self.demand.electricity_reconciliation = None
            self.demand.pass_electricity_reconciliation()
            self.demand.output_subsector_electricity_profiles()

        if self.demand_solved and export_results:
            self.demand.aggregate_results()
            export = ep2rio.RioExport(self)
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
            if self.special_shapes_write and "_profiles" in attribute:
                df = getattr(res_obj, attribute)
                self.special_shapes_export(df)
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

    def special_shapes_export(self, df):
        df = df.round(0)
        df = df.astype(int)
        df_summary = df.groupby(level=[ind for ind in df.index.names if ind not in ['subsector']]).sum()
        df_summary = df_summary.squeeze().unstack('year')
        Output.write(df_summary, 'summary_shapes.csv', os.path.join(cfg.workingdir, 'shape_outputs', self.scenario_id), append_when_existing=False)
        groups = df.groupby(level=['year'])
        for i, values_slice in groups:
            values_slice = values_slice.xs(i, level='year')
            values_slice = values_slice.squeeze().unstack(GeoMapper.demand_primary_geography)
            values_slice = values_slice.reorder_levels(['sector', 'subsector', 'weather_datetime']).sort_index()
            # del values_slice['puerto rico']
            # del values_slice['quebec (state)']
            # del values_slice['alaska']
            # del values_slice['hawaii']
            Output.write(values_slice, '{}.csv'.format(i), os.path.join(cfg.workingdir, 'shape_outputs', self.scenario_id), compression='gzip', append_when_existing=False)