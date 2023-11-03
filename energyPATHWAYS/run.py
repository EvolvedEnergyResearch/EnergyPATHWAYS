# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 19:20:05 2016

@author: ryandrewjones
"""

import sys
import signal
import click
import os
import glob
import pickle
import energyPATHWAYS.config as cfg
import energyPATHWAYS.util as util
from energyPATHWAYS.pathways_model import PathwaysModel
from energyPATHWAYS import outputs
import energyPATHWAYS.shapes2 as shapes2
from energyPATHWAYS.outputs import Output
from energyPATHWAYS.geomapper import GeoMapper
import time
import datetime
import logging
import smtplib
import cProfile
import traceback
import pandas as pd
import pdb
import energyPATHWAYS.unit_converter as unit_converter

# genClasses -o schema.py -d C:\github\ep_db_us_2023\database -D energyPATHWAYS.generated.ep_db_loader.EnergyPathwaysDatabase -c energyPATHWAYS.data_object.DataObject

model = None
run_start_time = time.time()

def all_finished(all_scenarios):
    return all([sensitivity_is_finished(os.path.join(os.getcwd(), scenario)) for scenario in all_scenarios])

def sensitivity_is_finished(scenario_path):
    if os.path.exists(os.path.join(scenario_path, 'solved.true')):
        return True
    else:
        return False

@click.command()
@click.option('-s', '--scenario', type=str, multiple=True, help='Scenario name to run. More than one can be specified by repeating this option. If none are specified, the working directory will be scanned for .json files and all will be run.')
@click.option('-ld', '--load_demand/--no_load_demand', default=False, help='Load a cached model with the demand side complete.')
@click.option('--export_results/--no_export_results', default=True, help='Write results from the demand and supply sides of the model.')
@click.option('--save_models/--no_save_models', default=True, help='Cache models after running.')
@click.option('--shape_owner/--no_shape_owner', default=True, help='Controls the process that runs the shapes')
@click.option('--compile_mode/--no_compile_mode', default=False, help='Compile scenarios only.')
def click_run(scenario, load_demand, export_results, save_models, shape_owner, compile_mode):
    run(scenario, load_demand, export_results, save_models, shape_owner, compile_mode)

def run(scenarios, load_demand=False, export_results=True, save_models=True, shape_owner=True, compile_mode=False):
    global model
    cfg.initialize_config()
    cfg.log_git_commit()
    GeoMapper.get_instance().log_geo()
    scenarios = util.ensure_iterable(scenarios)

    logging.info('Scenario run list: {}'.format(', '.join(scenarios)))

    if not compile_mode:
        for scenario in scenarios:
            scenario_start_time = time.time()
            logging.info('Starting scenario {}'.format(scenario))
            logging.info('Start time {}'.format(str(datetime.datetime.now()).split('.')[0]))
            model = load_model(load_demand, scenario)
            model.run(load_demand=load_demand,
                      export_results=export_results,
                      save_models=save_models,
                      shape_owner=shape_owner)

            logging.info('EnergyPATHWAYS run for scenario {} successful!'.format(scenario))
            logging.info('Scenario calculation time {}'.format(str(datetime.timedelta(seconds=time.time() - scenario_start_time)).split('.')[0]))

    all_scenarios = util.get_all_scenario_names(cfg.workingdir)
    if (all_finished(all_scenarios) and export_results) or compile_mode:
        outputs.aggregate_scenario_results(all_scenarios)

    logging.info('Total calculation time {}'.format(str(datetime.timedelta(seconds=time.time() - run_start_time)).split('.')[0]))
    logging.shutdown()
    logging.getLogger(None).handlers = [] # necessary to totally flush the logger

def load_model(load_demand, scenario):
    if load_demand:
        demand_file = os.path.join(cfg.workingdir, str(scenario), str(scenario) + cfg.demand_model_append_name)
        if os.path.isfile(demand_file):
            with open(os.path.join(cfg.workingdir, str(scenario), str(scenario) + cfg.demand_model_append_name), 'rb') as infile:
                model = pickle.load(infile)
                logging.info('Loaded demand-side EnergyPATHWAYS model from pickle')
        else:
            raise IOError("No model file exists")
    else:
        model = PathwaysModel(scenario)
    return model


if __name__ == "__main__":
    workingdir = r'D:\test system'
    os.chdir(workingdir)
    scenario = ['test']
    run(scenario,
    load_demand   = False,
    export_results= True,
    save_models   = False,
    shape_owner   = True,
    compile_mode  = False,
    )
