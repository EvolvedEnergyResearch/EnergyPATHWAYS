# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
import xlwings as xw
import sys
import pandas as pd
import numpy as np
from collections import OrderedDict
import csv
import six
import time
import pdb

wb = None
sht = None
directory = None
config_name = 'config.INI'
SENSITIVTY_LABEL = 'sensitivity'

control_tab = 'controls'
cases_tab = 'cases'
index_divider = '--'
none_str = '_none_'


config_options = OrderedDict([
    ("DATABASE", OrderedDict([
        ("database_path", "todo"),
    ])),
    ("CALCULATION_PARAMETERS", OrderedDict([
        ("parallel_process",                            "todo"),
        ("num_cores",                                   "todo"),
        ("shape_check",                                 "todo"),
    ])),
    ("TIME", OrderedDict([
        ("current_year",                                "todo"),
        ("end_year",                                    "todo"),
        ("weather_years",                               "todo"),
        ("dispatch_outputs_timezone",                   "todo"),
    ])),
    ("GEOGRAPHY", OrderedDict([
        ("default_geography_map_key",                   "todo"),
        ("demand_primary_geography",                    "todo"),
        ("primary_subset",                              "todo"),
        ("breakout_geography",                          "todo"),
        ("include_foreign_gaus",                        "todo"),
        ("disagg_geography",                            "todo"),
        ("disagg_breakout_geography",                   "todo"),
    ])),
    ("UNITS", OrderedDict([
        ("energy_unit",                                 "todo"),
        ("mass_unit",                                   "todo"),
        ("currency_name",                               "todo"),
        ("currency_year",                               "todo"),
        ("inflation_rate",                              "todo"),
    ])),
    ("DEMAND_OUTPUT_DETAIL", OrderedDict([
        ("dod_years_subset",                            "todo"),
        ("dod_vintage",                                 "todo"),
        ("dod_demand_technology",                       "todo"),
        ("dod_cost_type",                               "todo"),
        ("dod_new_replacement",                         "todo"),
        ("dod_other_index_1",                           "todo"),
        ("dod_other_index_2",                           "todo"),
        ("dod_output_hourly_profiles",                  "todo"),
        ("dod_hourly_profile_final_energy_types",       "todo"),
        ("dod_hourly_profile_years",                    "todo"),
        ("dod_hourly_profile_keep_subsector",           "todo"),
        ("dod_hourly_profile_keep_feeder",              "todo"),
    ])),
    ("DEMAND_CALCULATION_PARAMETERS", OrderedDict([
        ("use_service_demand_modifiers",                "todo"),
        ("removed_demand_levels",                       "todo"),
    ])),
    ("RIO", OrderedDict([
        ("rio_years",                                   "todo"),
        ("ep2rio_final_energy_shapes",                  "todo"),
        ("rio_standard_mass_unit",                      "todo"),
        ("rio_standard_energy_unit",                    "todo"),
        ("rio_standard_distance_unit",                  "todo"),
        ("rio_standard_volume_unit",                    "todo"),
        ("rio_flex_load_subsectors",                    "todo"),
        ("rio_optimizable_subsectors",                  "todo"),
        ('active_subsectors',                           "todo"),
        ('rio_optimizable_subsectors',                  "todo"),
        ('rio_flex_load_subsectors',                    "todo"),
    ])),
    ("RIO_DB", OrderedDict([
        ('rio_database_path',                           "todo"),
        ('shape_database_path',                         "todo"),
    ])),
    ("LOG", OrderedDict([
        ("log_level",                                   "todo"),
        ("stdout",                                      "todo"),
    ])),
])

MEASURE_CATEGORIES = ("DemandEnergyEfficiencyMeasures",
                      "DemandFuelSwitchingMeasures",
                      "DemandServiceDemandMeasures",
                      "DemandSalesShareMeasures",
                      "DemandStockMeasures",)

def _msg(message):
    wb.sheets[cases_tab].range('python_msg').value = message

def _clear_msg():
    wb.sheets[cases_tab].range('python_msg').clear_contents()


def error_check_database():
    pass

def ensure_iterable(obj):
    if isinstance(obj, six.string_types):
        return [obj]
    else:
        try:
            iter(obj)
            return list(obj)
        except TypeError:
            return [obj]

def get_selected_item(column_range):
    row = wb.app.selection.row
    column = sht.range(column_range).column
    item = sht.cells(row, column).value
    return item

def load_config(system_path, sections_to_load='all'):
    cfg_path = os.path.join(system_path, config_name)
    active_subsectors_dict = {}
    with open(cfg_path, 'r') as infile:
        csvreader = csv.reader(infile, delimiter='=')
        sheet = wb.sheets(cases_tab)
        section_name = None
        for row in csvreader:
            if len(row) and row[0][0] == '[':
                section_name = row[0].strip('[').strip(']')
                sheet = wb.sheets(control_tab) if section_name in ["RIO", "RIO_DB", "CALCULATION_PARAMETERS"] else wb.sheets(cases_tab)
                continue
            if len(row) == 0 or row[0][0]=="#":
                continue
            if sections_to_load != 'all' and section_name not in ensure_iterable(sections_to_load):
                continue
            if len(row) == 1:
                parts = row[0].split(':')
                # if the length of parts is 3, it means we probably split a system path and need to put it back together
                if len(parts)==3:
                    row = [parts[0], parts[1]+':'+parts[2]]
                else:
                    row = [parts[0], parts[1]]
            option_name = row[0].rstrip().lstrip()
            value = row[1].rstrip().lstrip()
            if option_name in ['active_subsectors', 'rio_optimizable_subsectors', 'rio_flex_load_subsectors']:
                active_subsectors_dict[option_name] = [s.rstrip().lstrip() for s in value.split('||')]
                continue
            elif option_name == 'rio_years':
                # vertical list
                value = [[int(s)] for s in value.split(',')]
                wb.sheets(control_tab).range('rio_years').clear_contents()
            try:
                sheet.range(option_name).value = value
            except:
                print('unable to load config option named: {}'.format(option_name))

    if len(active_subsectors_dict):
        load_active_subsectors_into_excel(active_subsectors_dict)

def load_active_subsectors_into_excel(active_techs_dict):
    make_connections()
    subsectors = get_available_subsectors()
    subsectors['Is active?'] = [sub in active_techs_dict['active_subsectors'] for sub in subsectors['Subsector'].values]
    subsectors['Optimized?'] = [sub in active_techs_dict['rio_optimizable_subsectors'] for sub in subsectors['Subsector'].values]
    subsectors['Flexible load?'] = [sub in active_techs_dict['rio_flex_load_subsectors'] for sub in subsectors['Subsector'].values]
    subsectors = subsectors.sort_values(['Sector', 'Subsector'])

    wb.sheets(control_tab).range('active_subsector_table').clear_contents()
    wb.sheets(control_tab).range('active_subsector_table').value =[list(subsectors.columns)]+list(subsectors.values)

def get_available_subsectors():
    make_connections()
    db_dir = wb.sheets(cases_tab).range('database_path').value
    from energyPATHWAYS.generated.ep_db_loader import EnergyPathwaysDatabase
    db = EnergyPathwaysDatabase.get_database(db_dir, load=False)
    subsectors = pd.read_csv(db.file_map['DemandSubsectors'])[['sector', 'name']]
    subsectors.columns = ['Sector', 'Subsector']
    return subsectors

def is_strnumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def format_cfg_value(value):
    if type(value) is list:
        return ", ".join([str(format_cfg_value(s)) for s in value if s is not None])
    return int(value) if is_strnumeric(str(value)) and (int(value) - value == 0) else value

def get_active_subsector_table():
    subsector_table = wb.sheets(control_tab).range('active_subsector_table').value
    subsector_table = [row for row in subsector_table if row[0]]
    subsector_table = pd.DataFrame(subsector_table[1:], columns=subsector_table[0])
    return subsector_table

def get_cfg_value(sheet, option_name):
    try:
        if option_name=="weather_years":
            value = sheet.range(option_name).value
            if not is_strnumeric(value):
                value = ', '.join([val.rstrip().lstrip() for val in value.split(',')])
        elif option_name=="active_subsectors":
            subsector_table = get_active_subsector_table()
            value = '|| '.join(subsector_table[subsector_table['Is active?']==True]['Subsector'].values)
        elif option_name == "rio_optimizable_subsectors":
            subsector_table = get_active_subsector_table()
            value = '|| '.join(subsector_table[subsector_table['Optimized?']==True]['Subsector'].values)
        elif option_name=="rio_flex_load_subsectors":
            subsector_table = get_active_subsector_table()
            value = '|| '.join(subsector_table[subsector_table['Flexible load?']==True]['Subsector'].values)
        else:
            value = sheet.range(option_name).value
        return format_cfg_value(value)
    except:
        raise ValueError("Error saving config option: {}".format(option_name))



def save_config(system_path):
    cfg_path = os.path.join(system_path, config_name)
    linesep = '\n'
    with open(cfg_path, 'w') as outfile:
        for section_name, section in config_options.items():
            sheet = wb.sheets(control_tab) if section_name in ["RIO", "RIO_DB", "CALCULATION_PARAMETERS"] else wb.sheets(cases_tab)
            outfile.write("##################################################"+linesep)
            outfile.write("[{}]".format(section_name)+linesep)
            outfile.write("##################################################"+linesep)
            for option_name, option_description in section.items():
                value = get_cfg_value(sheet, option_name)
                if value is None:
                    outfile.write('{} ='.format(option_name)+linesep)
                else:
                    outfile.write("{} = {}".format(option_name, value)+linesep)
            outfile.write(linesep)


def make_connections():
    global wb, sht, directory
    if wb is not None:
        return
    # Make a connection to the calling Excel file
    try:
        wb = xw.Book.caller()
        sht = wb.sheets.active
        directory = os.path.dirname(wb.fullname)
    except:
        wb = xw.Book('scenario_builder.xlsm')
        sht = wb.sheets.active
        directory = os.getcwd()


def path_is_valid_system(path):
    if os.path.isdir(path) and os.path.isfile(os.path.join(path, config_name)):
        return True
    else:
        return False

def get_system_date_modified(path):
    return datetime.fromtimestamp(os.path.getmtime(os.path.join(path, config_name))).strftime('%Y-%m-%d %H:%M')

def is_valid_sensitivity(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, 'BULK_LOAD.csv'))

def get_system_runs_count(path):
    return len(get_system_run_names(path))

def get_system_run_names(path):
    if not os.path.exists(os.path.join(path, 'runs_key.csv')):
        return []
    sensitivities = pd.read_csv(os.path.join(path, 'runs_key.csv'), index_col=0, nrows=1)
    return sensitivities.columns

def get_saved_systems(base_dir):
    make_connections()
    saved_systems = []
    for folder in os.listdir(base_dir):
        path = os.path.join(base_dir, folder)
        if path_is_valid_system(path):
            # todo: fill in methods for sensitivities count and system status
            num_sensitivities = get_system_runs_count(path)
            timestamp = get_system_date_modified(path)
            saved_systems.append([folder, num_sensitivities, timestamp])
    return saved_systems

def refresh_run_list_control():
    make_connections()
    base_dir = wb.sheets(control_tab).range('scenario_folder_controls').value
    saved_systems = get_saved_systems(base_dir)
    sht.range('control_runs_box').clear_contents()
    sht.range('control_runs_box').value = saved_systems

def refresh_run_list_case_setup():
    make_connections()
    base_dir = wb.sheets(cases_tab).range('scenario_folder_case_setup').value
    saved_systems = get_saved_systems(base_dir)
    sht.range('setup_runs_box').clear_contents()
    sht.range('setup_runs_box').value = saved_systems

def run_launch_prep():
    make_connections()
    system_name = wb.sheets(control_tab).range('queued_scenario_name').value
    update_config(system_name, ["RIO", "RIO_DB", "CALCULATION_PARAMETERS"])

def update_export2rio_db_path():
    make_connections()
    system_name = wb.sheets(control_tab).range('queued_scenario_name').value
    update_config(system_name, ["RIO_DB"])

def update_config(system_name, update_sections):
    linesep = '\n'
    base_dir = wb.sheets(control_tab).range('scenario_folder_controls').value
    system_path = os.path.join(base_dir, system_name)
    cfg_path = os.path.join(system_path, config_name)
    current_config = []
    with open(cfg_path, 'r') as infile:
        for row in infile:
            current_config.append(row)
    update_sections = ensure_iterable(update_sections)
    section_name = None
    with open(cfg_path, 'w') as outfile:
        for row in current_config:
            if len(row) and row[0] == '[':
                section_name = row.strip(linesep).strip('[').strip(']')
                sheet = wb.sheets(control_tab) if section_name in ["RIO", "RIO_DB", "CALCULATION_PARAMETERS"] else wb.sheets(cases_tab)
            if row==linesep or row=='\n' or len(row) == 0 or row[0]=="#" or row[0]=="[":
                outfile.write(row)
                continue
            print(section_name)
            if section_name in update_sections:
                # we are updating, so grab the data from excel
                option_name = row.split('=')[0].rstrip().lstrip()
                value = get_cfg_value(sheet, option_name)
                if value is None:
                    outfile.write('{} ='.format(option_name)+linesep)
                else:
                    outfile.write("{} = {}".format(option_name, value)+linesep)
            else:
                # we do not update, we just write the data from the existing config
                outfile.write(row)

def save_runs_key():
    make_connections()

    run_names = wb.sheets(cases_tab).range('case_names_row').value
    good_columns = np.nonzero([rn is not None for rn in run_names])[0]
    run_names = [rn for (i, rn) in enumerate(run_names) if i in good_columns]
    # these eventually become folder names, so we can't have slashes
    run_names = [rn.replace('\\', '_').replace('/', '_') for rn in run_names]
    run_names = [rn.replace('%', 'p') for rn in run_names]
    if len(run_names) > len(set(run_names)):
        raise ValueError('All run names must be unique. Please check the run names on the Sensitivity setup tab')

    sensitivities = wb.sheets(cases_tab).range('measure_table_values').value

    # get rid of extra rows at the bottom or
    sensitivities = [row for row in sensitivities if row[0] is not None and any([x is not None for x in row[7:]])]
    # get rid of extra columns to the right
    sensitivities = [row[:7] + [x for (i, x) in enumerate(row[7:]) if i in good_columns] for row in sensitivities]
    measures = [[index_divider.join([str(ind) for ind in row[2:7] if ind is not None])] + [None if col is None else 'x' for col in row[7:]] for row in sensitivities if row[1]=='measure']
    # collapse the index columns
    sensitivities = [[index_divider.join([str(ind) for ind in row[2:6] if ind is not None])] + row[6:] for row in sensitivities if row[1]!='measure']

    sens_dict = {}
    for row in sensitivities:
        ind, sens_name = row[0], row[1]
        if ind not in sens_dict:
            sens_dict[ind] = {}
        for x, run_name in zip(row[2:], run_names):
            if x is not None:
                if run_name in sens_dict[ind]:
                    raise ValueError("Two sensitivities active for index {}".format(ind))
                sens_dict[ind][run_name] = sens_name

    sensitivities = pd.DataFrame.from_dict(sens_dict)
    sensitivities.index.name = 'run_name'

    # get the correct order
    sensitivities = sensitivities.loc[run_names]
    sensitivities = sensitivities.fillna('_reference_')
    sensitivities = sensitivities.transpose()

    measures = pd.DataFrame(measures, columns=['run_name'] + run_names)
    measures = measures.set_index('run_name')

    return pd.concat((measures, sensitivities))


def save_cases():
    make_connections()

    name = wb.sheets(cases_tab).range('run_name').value
    base_dir = wb.sheets(cases_tab).range('scenario_folder_case_setup').value

    system_path = os.path.join(base_dir, name)
    if not os.path.exists(system_path):
        os.makedirs(system_path)

    save_config(system_path)
    sensitivities = save_runs_key()
    sensitivities.to_csv(os.path.join(system_path, 'runs_key.csv'))

    refresh_run_list_case_setup()
    _msg("successfully saved all scenarios!")

def load_shape_sensitivity_record(db):
    db_dir = db.pathname
    import pickle
    max_shapes_data_modified = max([os.path.getmtime(os.path.join(db_dir, 'ShapeData', file_name)) for file_name in os.listdir(os.path.join(db_dir, 'ShapeData'))])
    pickle_path = os.path.join(db_dir, 'ShapeData', 'pickles', 'sensitivity_list.p')
    if os.path.isfile(pickle_path) and os.path.getmtime(pickle_path) > max_shapes_data_modified:
        with open(pickle_path, 'rb') as infile:
            db_sensitivities = pickle.load(infile)
    else:
        db.shapes.load_all()
        db_sensitivities = []
        for shape_name in db.shapes.slices.keys():
            data = db.shapes.get_slice(shape_name)
            # not every input table has sensitivities
            if data is None or not len(data):
                continue
            data = data.drop_duplicates()
            data = data.rename(columns={'name': 'parent name', 'sensitivity': 'measure name'})
            data['table name'] = 'ShapeData'
            data['side'] = 'd'
            data['type'] = 'sensitivity'
            data['filter1'] = none_str
            data['filter2'] = none_str
            data = data[['side', 'type', 'table name', 'parent name', 'filter1', 'filter2', 'measure name']]
            db_sensitivities.append(data)

        db_sensitivities = pd.concat(db_sensitivities) if len(db_sensitivities) else pd.DataFrame([])
        from energyPATHWAYS.util import makedirs_if_needed
        makedirs_if_needed(os.path.join(db_dir, 'ShapeData', 'pickles'))
        with open(pickle_path, 'wb') as outfile:
            pickle.dump(db_sensitivities, outfile, pickle.HIGHEST_PROTOCOL)

    return db_sensitivities

def query_all_sensitivities(db):
    sensitivities = []
    for table, file_path in db.file_map.items():
        data = db.get_table(table).data
        # not every input table has sensitivities
        if data is None or not len(data):
            continue
        data = data.rename(columns={'name': 'parent name', 'sensitivity': 'measure name'})
        for fill_filter in [1, 2]:
            if 'filter{}'.format(fill_filter) not in data.columns:
                data['filter{}'.format(fill_filter)] = none_str
        data['table name'] = table
        data['side'] = 'd' if table.startswith("Demand") or table=='ShapeData' else 's'
        data['type'] = 'sensitivity'
        data = data[['side', 'type', 'table name', 'parent name', 'filter1', 'filter2', 'measure name']]
        sensitivities.append(data)

    sensitivities.append(load_shape_sensitivity_record(db))
    if not len(sensitivities):
        return None
    sensitivities = pd.concat(sensitivities)
    return sensitivities

def query_all_measures(db):
    measures = []
    for table in MEASURE_CATEGORIES:
        data = db.get_table(table).data
        if data is None:
            continue

        parent_name = 'subsector' if table.startswith("Demand") else 'supply_node'
        data = data[['name', parent_name]].drop_duplicates()
        data.columns = ['measure name', 'parent name']
        data['side'] = 'd' if table.startswith("Demand") or table=='ShapeData' else 's'
        data['table name'] = table
        measures.append(data)

    if not len(measures):
        return None
    measures = pd.concat(measures)
    measures['type'] = 'measure'
    measures['filter1'] = none_str
    measures['filter2'] = none_str
    measures = measures[['side', 'type', 'table name', 'parent name', 'filter1', 'filter2', 'measure name']]
    return measures

def _pull_sensitivities(json_dict):
    result = []
    for key1, value1 in json_dict.items():
        if type(value1) is dict:
            result += _pull_sensitivities(value1)
        elif key1 == "Sensitivities":
            result += [('d' if v['table'].startswith("Demand") or v['table']=='ShapeData' else 's',
                        'sensitivity',
                        v['table'],
                        v['name'],
                        v['sensitivity'])
                       for v in value1]
    return result

def _load_json(path):
    with open(path, 'r') as infile:
        loaded = json.load(infile)
    return loaded

def _pull_sensitivities_df(json_dict, scenario):
    result = _pull_sensitivities(json_dict)
    scenario_sensitivities = pd.DataFrame(result, columns=['side', 'type', 'table name', 'parent name', 'measure name'])
    scenario_sensitivities[scenario] = 'x'
    return scenario_sensitivities

def _pull_measures(json_dict):
    result = []
    for key1, value1 in json_dict.items():
        if type(value1) is dict:
            result += _pull_measures(value1)
        elif key1 in MEASURE_CATEGORIES:
            result += [[v, key1] for v in value1]
    return result

def _pull_measures_df(json_dict, scenario):
    result = _pull_measures(json_dict)
    scenario_measures = pd.DataFrame(result, columns=['measure name', 'table name'])
    scenario_measures[scenario] = 'x'
    return scenario_measures  # this is where we make each measure that is in a scenario show up with an x

def load_json_measures(scenario_path):
    scenarios = [file_name[:-5] for file_name in os.listdir(scenario_path) if file_name[-5:]=='.json']
    measures_df, sensitivity_df = None, None
    for scenario in scenarios:
        path = os.path.join(scenario_path, scenario + '.json')
        if not os.path.isfile(path):
            _msg("error: cannot find path {}".format(path))
            sys.exit()
        json_dict = _load_json(path)
        scenario_measures = _pull_measures_df(json_dict, scenario)
        measures_df = scenario_measures if measures_df is None else pd.merge(measures_df, scenario_measures, how='outer')
        scenario_sensitivities = _pull_sensitivities_df(json_dict, scenario)
        sensitivity_df = scenario_sensitivities if sensitivity_df is None else pd.merge(sensitivity_df, scenario_sensitivities, how='outer')
    return measures_df, sensitivity_df

def load_runs_key(scenario_path):
    # it's possible we are hitting refresh and we haven't yet saved any sensitivities
    if not os.path.exists(os.path.join(scenario_path, 'runs_key.csv')):
        return pd.DataFrame()
    sensitivities = pd.read_csv(os.path.join(scenario_path, 'runs_key.csv'), index_col=0)
    if len(sensitivities)==0:
        return pd.DataFrame()
    run_names = sensitivities.columns
    sensitivity_dict = {}
    measure_dict = {}
    for ind, data in sensitivities.iterrows():
        # file, name, filter1, filter2
        exp_ind = ind.split(index_divider)
        table_name = exp_ind[0]
        if table_name in MEASURE_CATEGORIES:
            measure_name = exp_ind[-1]
            exp_ind = exp_ind[:-1]
            exp_ind = tuple(exp_ind)
            for run_name, is_x in zip(data.index, data.values):
                if exp_ind + (measure_name,) not in measure_dict:
                    measure_dict[exp_ind + (measure_name,)] = {}
                measure_dict[exp_ind + (measure_name,)][run_name] = none_str if pd.isnull(is_x) else 'x'
        else:
            # fill in none_str for filters if they don't exist, a string in necessary for pandas to be happy
            exp_ind += [none_str]*(4-len(exp_ind))
            exp_ind = tuple(exp_ind)
            for run_name, sens_name in zip(data.index, data.values):
                if exp_ind + (sens_name,) not in sensitivity_dict:
                    sensitivity_dict[exp_ind + (sens_name,)] = {}
                sensitivity_dict[exp_ind + (sens_name,)][run_name] = 'x'

    sensitivities = pd.DataFrame.from_dict(sensitivity_dict).transpose()[run_names]
    sensitivities.index.names = ['table name', 'parent name', 'filter1', 'filter2', 'measure name']
    measures = pd.DataFrame.from_dict(measure_dict).transpose()[run_names]
    measures.index.names = ['table name', 'parent name', 'measure name']

    return measures.reset_index(), sensitivities.reset_index()

def load_measures_and_sensitivities(scenario_path):
    make_connections()
    db_dir = sht.range('database_path').value

    from energyPATHWAYS.generated.ep_db_loader import EnergyPathwaysDatabase

    if os.path.exists(os.path.join(scenario_path, 'runs_key.csv')):
        # this could be made a loop if we want to load and merge multiple runs keys
        measures_df, sensitivity_df = load_runs_key(scenario_path)
    else:
        measures_df, sensitivity_df = load_json_measures(scenario_path)


    scenarios = list(measures_df.columns[2:])

    EnergyPathwaysDatabase.clear_cached_database()
    all_measures = query_all_measures(EnergyPathwaysDatabase.get_database(db_dir, load=False))
    EnergyPathwaysDatabase.clear_cached_database()
    all_sensitivities = query_all_sensitivities(EnergyPathwaysDatabase.get_database(db_dir, load=False, compile_sensitivities=True))

    how = 'left' if sht.range('filter_missing_sensitivities').value else 'outer'

    values_m = pd.merge(all_measures, measures_df, how=how)
    values_s = pd.merge(all_sensitivities, sensitivity_df, how=how)

    filter_defaults = lambda x: not (len(x) == 1 and ('[d]' in x['measure name'].values[0].lower() or x['measure name'].values[0].lower() == '_reference_'))
    values_s = values_s.groupby(['side', 'type', 'table name', 'parent name', 'filter1', 'filter2']).filter(filter_defaults)

    if sht.range('filter_inactive_sensitivities').value:
        values_m = values_m[~values_m[scenarios].isnull().all(axis=1)]
        values_s = values_s[~values_s[scenarios].isnull().all(axis=1)]

    values_m = values_m.set_index(['side', 'type', 'table name', 'parent name', 'filter1', 'filter2', 'measure name'], append=False).sort_index()
    values_s = values_s.set_index(['side', 'type', 'table name', 'parent name', 'filter1', 'filter2', 'measure name'], append=False).sort_index()
    values_s = values_s[values_m.columns]

    values = pd.concat((values_m, values_s))
    return values

def load_cases():
    make_connections()

    name = get_selected_item('setup_runs_box_name')
    base_dir = wb.sheets(cases_tab).range('scenario_folder_case_setup').value

    scenario_path = os.path.join(base_dir, name)
    if not os.path.exists(scenario_path):
        raise ValueError("Cannot find system path: {}".format(scenario_path))

    load_config(scenario_path)
    df = load_measures_and_sensitivities(scenario_path)

    case_names = df.columns
    values = df.reset_index().values
    values[np.nonzero(values == none_str)] = None

    sht.range('measure_table_values').clear_contents()
    sht.range('case_names_row').clear_contents()
    sht.range('measure_table_values').value = values
    sht.range('case_names_row').value = list(case_names)
    sht.range('run_name').value = name
    _msg("sucessfully loaded scenarios from folder {}".format(scenario_path))

def queue_selected_scenario():
    make_connections()

    name = get_selected_item('control_runs_box_name')
    base_dir = wb.sheets(control_tab).range('scenario_folder_controls').value

    system_path = os.path.join(base_dir, name)
    if not os.path.exists(system_path):
        raise ValueError("Cannot find system path: {}".format(system_path))

    load_config(system_path, ["RIO", "RIO_DB", "CALCULATION_PARAMETERS"])
    wb.sheets(control_tab).range('queued_scenario_name').value = name

    scenarios = get_system_run_names(system_path)

    wb.sheets(control_tab).range('scenario_list_controls').clear_contents()
    wb.sheets(control_tab).range('scenario_list_controls').value = [[scen] for scen in scenarios]

if __name__ == '__main__':
    # load_cases()
    save_cases()
    # run_launch_prep()
    # queue_selected_scenario()
    # refresh_run_list_control()