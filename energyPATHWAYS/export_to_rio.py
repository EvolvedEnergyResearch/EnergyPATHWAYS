
from energyPATHWAYS.outputs import Output, delete_csv_files_in_folder
import os
from energyPATHWAYS import util
import shutil
import energyPATHWAYS.config as cfg
import pandas as pd
import logging
import pdb
import copy
import numpy as np
import numpy_financial as npf
from collections import defaultdict
import glob
import pickle
from RIO.riodb.rio_db_loader import RioDatabase
from energyPATHWAYS import shapes2
import energyPATHWAYS.scenario_loader as scenario_loader
from energyPATHWAYS.geomapper import GeoMapper
from energyPATHWAYS.unit_converter import UnitConverter
import click
import datetime as DT
from csvdb import CsvDatabase

class BlendMapDict(dict):
    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            # Check if the exact key exists
            if key in self:
                return super().__getitem__(key)
            # Fallback to the key with np.nan as the first item
            fallback_key = (np.nan, key[1])
            if fallback_key in self:
                return super().__getitem__(fallback_key)
        # Raise KeyError if no match found
        raise KeyError(f"Key {key} not found")

class RioExport(object):
    def __init__(self, model, shape_owner):
        self.model = model
        self.demand = model.demand
        self.scenario = model.scenario_id
        self.shape_owner = shape_owner
        self.base_path = os.path.join(cfg.workingdir, self.scenario, 'EP2RIO')
        self.results_path = os.path.join(cfg.workingdir, self.scenario, 'demand_outputs')
        self.db = CsvDatabase.get_database(cfg.getParam('database_path', section='DATABASE'), output_tables=True, load=False)
        logging.info(self.base_path)
        self.scenario_index = 0
        self.make_blend_mapping()

    def write_all(self):
        self.write_demand_subsector()
        self.write_demand_shapes()
        self.write_demand_side_levelized_costs()
        self.write_demand_side_spending()
        self.write_exo_demand()

    def make_blend_mapping(self):
        blend_group = util.table_data('FinalEnergyRIOBlendGroups').copy()
        del blend_group['notes']
        # get the list of subsectors where final_energy == 'electricity' and blend_group does not equal 'electricity'
        self.shape_subsectors_to_exclude = {}
        final_energy_shape_types = cfg.ep2rio_final_energy_shapes + [cfg.electricity_energy_type]
        for final_energy_shape_type in final_energy_shape_types:
            subsector_list = blend_group.loc[(blend_group['blend_group'] != final_energy_shape_type) & (blend_group['final_energy'] == final_energy_shape_type) & (~blend_group['subsector'].isnull()), 'subsector'].tolist()
            self.shape_subsectors_to_exclude[final_energy_shape_type] = subsector_list if len(subsector_list) else None
        blend_group = blend_group.set_index(['subsector', 'final_energy'])
        self.blend_mapping = {key: BlendMapDict(value) for key, value in blend_group.to_dict().items()}

    def write_demand_side_levelized_costs(self):
        logging.info('EP2RIO: Writing demand-side levelized cost')
        df = self.demand.group_output('levelized_costs',levels_to_keep=['year', 'vintage', GeoMapper.demand_primary_geography, 'subsector','cost_type'])
        if df is not None:
            df = df.groupby(level=df.index.names).sum()
            df = GeoMapper.geo_map(df, GeoMapper.demand_primary_geography, GeoMapper.demand_primary_geography, 'total')
            df = df.reorder_levels(['year', 'vintage', GeoMapper.demand_primary_geography, 'subsector','cost_type']).sort_index()
            df['updated_vintage'] = ['historical' if vintage < min(cfg.rio_years) else 'future' for vintage in df.index.get_level_values('vintage')]
            df = df.set_index('updated_vintage', append=True)
            df = util.remove_df_levels(df, 'vintage')
            util.replace_index_name(df,'vintage','updated_vintage')
            currency = df.columns[0].split()[1].lower()
            currency_year = df.columns[0].split()[0]
            df.columns = ['value']
            existing_subsectors = df.index.get_level_values('subsector').unique()
            cost_types = df.index.get_level_values('cost_type').unique()
            missing_subsectors = util.flatten_list([[subsector_name for subsector_name in sector.subsectors.keys() if subsector_name not in existing_subsectors] for sector in self.demand.sectors.values()])
            new_index = pd.MultiIndex.from_product([cfg.years, ['future','historical'], GeoMapper.demand_geographies, missing_subsectors,cost_types], names=['year', 'vintage', GeoMapper.demand_primary_geography, 'subsector','cost_type'])
            missing_subsector_df = pd.DataFrame(0, index=new_index, columns=['value'])
            df = util.df_list_concatenate([df, missing_subsector_df])
            util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
            df = df.groupby(level=df.index.names).sum()
            df['currency'] = currency
            df['currency_year'] = currency_year
            df['interpolation_method'] = 'linear_interpolation'
            df['extrapolation_method'] = 'nearest'
            df['extrapolation_growth_rate'] = 0
            df['geography'] = GeoMapper.demand_primary_geography
            df['sensitivity'] = self.scenario
            df = df.reset_index()
            df = df[['subsector','cost_type','currency', 'currency_year','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','vintage','year','value','sensitivity']]

            df['value'] = df['value'].round(0)
            path = os.path.join(self.base_path, 'DEMAND_LEVELIZED_COSTS.csvd')
            Output.write(df, "{}.csv".format(self.scenario), path, compression='gzip', index=False, lower_case=True)

    def write_demand_side_spending(self):
        logging.info('EP2RIO: Writing demand-side spending')
        df = self.demand.group_output('annual_costs',levels_to_keep=['year', GeoMapper.demand_primary_geography, 'subsector','demand_technology','cost_type'])

        if df is not None:
            df = df.groupby(level=df.index.names).sum()
            df = GeoMapper.geo_map(df, GeoMapper.demand_primary_geography, GeoMapper.demand_primary_geography, 'total')
            df = df.reorder_levels(['year', GeoMapper.demand_primary_geography, 'subsector','demand_technology','cost_type']).sort_index()
            currency = df.columns[0].split()[1].lower()
            currency_year = df.columns[0].split()[0]
            df.columns = ['value']
            existing_subsectors = df.index.get_level_values('subsector').unique()
            cost_types = df.index.get_level_values('cost_type').unique()
            missing_subsectors = util.flatten_list([[subsector_name for subsector_name in sector.subsectors.keys() if subsector_name not in existing_subsectors] for sector in self.demand.sectors.values()])
            new_index = pd.MultiIndex.from_product([cfg.years, ['future','historical'], GeoMapper.demand_geographies, missing_subsectors,cost_types], names=['year', 'vintage', GeoMapper.demand_primary_geography, 'subsector','cost_type'])
            missing_subsector_df = pd.DataFrame(0, index=new_index, columns=['value'])
            df = util.df_list_concatenate([df, missing_subsector_df])
            util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
            df['currency'] = currency
            df['currency_year'] = currency_year
            df['interpolation_method'] = 'linear_interpolation'
            df['extrapolation_method'] = 'nearest'
            df['extrapolation_growth_rate'] = ''
            df['geography'] = GeoMapper.demand_primary_geography
            df['sensitivity'] = self.scenario
            df = df.reset_index()
            df = df[['subsector','demand_technology','cost_type','currency', 'currency_year','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','year','value','sensitivity']]
            df['value'] = df['value'].round(0)
            path = os.path.join(self.base_path, 'DEMAND_SPEND.csvd')
            Output.write(df, "{}.csv".format(self.scenario), path, compression='gzip', index=False, lower_case=True)


    def rio_unit_lookup(self, unit_type):
        if unit_type == 'mass':
            return cfg.rio_standard_mass_unit
        elif unit_type == 'distance':
            return cfg.rio_standard_distance_unit
        elif unit_type == 'volume':
            return cfg.rio_standard_volume_unit
        else:
            return cfg.rio_standard_energy_unit

    def write_exo_demand(self):
        logging.info('EP2RIO: Writing blend inputs')
        exo_demand = self.get_blend_exo_demand()
        exo_demand = exo_demand.set_index([x for x in exo_demand.columns if x!='value'])

        def filter_exo(df):
            if (df==0).all().all():
                df = df.xs(df.index.get_level_values('year')[0], level='year', drop_level=False).xs(df.index.get_level_values('blend')[0], level='blend', drop_level=False)
            else:
                df = df.groupby(level=['blend'],group_keys=False).filter(lambda x: x.sum()!=0)
            return util.remove_df_levels(df, 'name')
        exo_demand = exo_demand.groupby(level=['name']).apply(filter_exo)
        exo_demand = exo_demand.reset_index()[['name', 'sector','unit', 'geography', 'gau','interpolation_method', 'extrapolation_method','blend','year', 'value', 'sensitivity']]

        Output.write(exo_demand, "EXO_DEMAND.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def get_blend_exo_demand(self):
        df = self.demand.outputs.d_energy.groupby(level=['year','sector','subsector',GeoMapper.demand_primary_geography,'final_energy', 'unit'],group_keys=False).sum()
        # subset df for just the rio run years
        df = df.loc[(cfg.rio_years, slice(None), slice(None), slice(None), slice(None), slice(None)),:]

        df = df[[not self.blend_mapping['drop_final_energy'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]]
        df['blend'] = [self.blend_mapping['blend_group'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]
        df = df.set_index('blend', append=True)
        # special case where we reverse the sign when exporting to RIO for some blends
        df['value'] *= np.array([-1 if self.blend_mapping['reverse_sign_EP2RIO'][x] else 1 for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))])
        df = df.groupby(level=['year','sector','subsector',GeoMapper.demand_primary_geography,'blend','unit'],group_keys=False).sum()

        df_electricity = df.xs('electricity', level='blend', drop_level=False)
        df_electricity *= UnitConverter.unit_convert(unit_from_num=cfg.calculation_energy_unit,unit_to_num='GWh')
        df_electricity = Output.clean_rio_df(df_electricity)
        df_electricity['unit'] = 'gigawatt_hour'

        # get the blends that are not 'electricity', these already have units
        df_non_electricity = df.drop('electricity', level='blend')
        df_non_electricity = Output.clean_rio_df(df_non_electricity)

        df = pd.concat((df_electricity, df_non_electricity))
        util.replace_column_name(df, 'name', 'subsector')

        df['interpolation_method'] = 'linear_interpolation'
        df['extrapolation_method'] = 'nearest'
        df['sensitivity'] = self.scenario
        return df

    def format_shape_meta_row(self, shape_name):
        row = [shape_name,'weather date','total','energy',cfg.getParam('dispatch_outputs_timezone', section='TIME'),
                    GeoMapper.demand_primary_geography,"",'linear_interpolation','nearest',True]
        return row

    def write_demand_shapes(self):
        logging.info('EP2RIO: Writing demand-side shapes')
        # to get bulk load
        shape_meta = [['name','shape_type','input_type','shape_unit_type','time_zone','geography','geography_map_key','interpolation_method','extrapolation_method','is_active']]
        final_energy_shapes = cfg.ep2rio_final_energy_shapes + [cfg.electricity_energy_type]
        for final_energy in set(final_energy_shapes):
            path = os.path.join(self.base_path, 'ShapeData', final_energy + '.csvd')
            allocate_to_feeder = True if final_energy == cfg.electricity_energy_type else False
            written_years = []
            dfs = []
            for year in cfg.rio_years:
                df = self.demand.aggregate_final_energy_shapes(year, final_energy, reconciliation_step=False, allocate_to_feeder=allocate_to_feeder, exclude_subsectors=self.shape_subsectors_to_exclude[final_energy])
                if df is None:
                    continue
                df.index = df.index.rename('gau', level=GeoMapper.demand_primary_geography)
                df = Output.clean_rio_df(df)
                df['value'] = df['value'].clip(0.01,None).round(2)
                df['year'] = year
                df['sensitivity'] = self.scenario
                dfs.append(df)
                written_years.append(year)
            if len(written_years):
                shape_meta.append(self.format_shape_meta_row(final_energy))

            file_name = '{}_{}.csv'.format(final_energy, self.scenario)
            Output.write(pd.concat(dfs), file_name, path, compression='gzip', index=False, lower_case=True)

        # to get subsectors for optimizable and flex load subsectors
        for subsector_name in set(cfg.rio_optimizable_subsectors + cfg.rio_flex_load_subsectors):
            path = os.path.join(self.base_path, 'ShapeData', subsector_name + '.csvd')
            sector_name = [sector.name for sector in self.demand.sectors.values() if subsector_name in sector.subsectors]
            if len(sector_name):
                sector_name = sector_name[0]
                written_years = []
                dfs = []
                for year in cfg.rio_years:
                    df = self.demand.sectors[sector_name].subsectors[subsector_name].aggregate_subsector_final_energy_shape(year, cfg.electricity_energy_type, allocate_to_feeder=True)
                    if df is None: # this can happen when we have no electricity demand in a year for a subsector
                        continue
                    df.index = df.index.rename('gau', level=GeoMapper.demand_primary_geography)
                    df = Output.clean_rio_df(df)
                    df['value'] = df['value'].clip(0.01,None).round(2)
                    df['year'] = year
                    df['sensitivity'] = self.scenario
                    dfs.append(df)
                    written_years.append(year)
                if len(written_years):
                    shape_meta.append(self.format_shape_meta_row(subsector_name))

                file_name = '{}_{}.csv'.format(subsector_name, self.scenario)
                if len(dfs):
                    Output.write(pd.concat(dfs), file_name, path, compression='gzip', index=False, lower_case=True)

        Output.write(pd.DataFrame(shape_meta[1:], columns=shape_meta[0]), 'SHAPE_META.csv', self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_subsector(self):
        logging.info('EP2RIO: Writing demand-side opt inputs')
        if self.shape_owner:
            self.write_dispatch_feeder_allocation()
        self.write_demand_measures()
        if len(cfg.rio_optimizable_subsectors):
            if self.shape_owner:
                self.write_demand_tech_main()
            self.write_demand_tech_service_demand()
            self.write_demand_tech_sales()
            self.write_demand_tech_capital_costs()
            self.write_demand_tech_incentives()
            self.write_demand_tech_fixed_om()
            self.write_demand_tech_service_demand_modifier()
            self.write_demand_tech_efficiency()


    def write_demand_tech_sales(self):
        sales_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    df = subsector.stock.sales
                    #df = df.groupby(level=[x for x in df.index.names if x != 'demand_technology']).transform(lambda x: x/x.sum())
                    util.replace_index_name(df,'name','demand_technology')
                    util.replace_index_name(df, 'vintage', 'year')
                    util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
                    if 'other_index_1'not in df.index.names:
                        df['other_index'] = None
                    elif 'other_index_1'in df.index.names:
                        util.replace_index_name(df, 'other_index', 'other_index_1')
                    if 'other_index_1' and 'other_index_2' in df.index.names:
                        df['other_index'] = [x + "||" + y for x,y in zip(df.index.get_level_values('other_index_1'),df.index.get_level_values('other_index_2'))]
                    df['interpolation_method'] = 'linear_interpolation'
                    df['extrapolation_method'] = 'nearest'
                    df['extrapolation_growth_rate'] = None
                    df['sensitivity'] =  self.scenario
                    df['geography'] = GeoMapper.demand_primary_geography
                    df['subsector'] = subsector_name
                    df = df.reset_index()
                    df = df[['name','subsector','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','vintage','other_index','value','sensitivity']]
                    sales_dfs.append(df)
        df = pd.concat(sales_dfs)
        df = df[df['vintage']>=min(cfg.rio_years)]
        Output.write(df, "DEMAND_TECH_SALES_MAX.csv", self.base_path, compression='gzip', index=False, lower_case=True)
        Output.write(df, "DEMAND_TECH_SALES_EP.csv", self.base_path, compression='gzip', index=False, lower_case=True)
        Output.write(df, "DEMAND_TECH_SALES_MIN.csv", self.base_path, compression='gzip', index=False, lower_case=True)


    def write_demand_tech_service_demand(self):
        service_demand_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    df1 = subsector.service_demand.values.stack('year').to_frame()
                    df2 = subsector.stock.total
                    df = util.DfOper.divi([df1,df2])
                    df.columns = ['value']
                    df = df[df.index.get_level_values('year') >= min(cfg.rio_years)]
                    df = util.add_and_set_index(df,'name', list(subsector.technologies.keys()))
                    df['subsector'] = subsector_name
                    util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
                    if subsector.service_demand.other_index_1 not in df.index.names:
                        df['other_index'] = None
                    if subsector.service_demand.other_index_1 and subsector.service_demand.other_index_2 in df.index.names:
                        df['other_index'] = [x + "||" + y for x,y in zip(df.index.get_level_values(subsector.service_demand.other_index_1),df.index.get_level_values(subsector.service_demand.other_index_2))]
                    elif subsector.service_demand.other_index_1 in df.index.names:
                        util.replace_index_name(df, 'other_index',subsector.service_demand.other_index_1)
                    df['interpolation_method'] = 'linear_interpolation'
                    df['extrapolation_method'] = 'nearest'
                    df['extrapolation_growth_rate'] = None
                    df['source'] = None
                    df['notes'] = None
                    df['sensitivity'] = self.scenario
                    df['geography'] = GeoMapper.demand_primary_geography
                    df['unit'] = subsector.service_demand.unit
                    df = df.reset_index()
                    df = df[['name','subsector','source','notes','geography','gau','unit','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','other_index','year','value','sensitivity']]
                    service_demand_dfs.append(df)
        df = pd.concat(service_demand_dfs)
        Output.write(df, "DEMAND_TECH_SERVICE_DEMAND.csv", self.base_path, compression='gzip', index=False, lower_case=True)


    def write_demand_measures(self):
        self.write_demand_ee_measure_costs()
        self.write_demand_fs_measure_costs()
        self.write_demand_ee_savings()
        self.write_demand_fs_savings()
        self.write_demand_fs_additions()

    def write_demand_ee_measure_costs(self):
        df = self.demand.group_output('ee_measure_costs', levels_to_keep=cfg.output_demand_levels + ['vintage'])
        if df is not None:
            df = self.demand.group_output('ee_measure_costs', levels_to_keep=cfg.output_demand_levels + ['vintage']).stack()
            df = df.reset_index(level='year', drop=True)
            util.replace_index_name(df, 'year', None)
            df.columns = ['value']
            df = df[df.index.get_level_values('vintage') == df.index.get_level_values('year')]
            df = df.groupby(level=[GeoMapper.demand_primary_geography, 'subsector', 'measure', 'vintage'],group_keys=False).mean().to_frame()
            df.columns = ['value']
            util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
            df['denominator_unit'] = cfg.calculation_energy_unit
            df['currency'] = cfg.currency_name
            df['currency_year'] = cfg.currency_year
            df['interpolation_method'] = 'linear_interpolation'
            df['extrapolation_method'] = 'nearest'
            df['extrapolation_growth_rate'] = None
            df['sensitivity'] = self.scenario
            df['geography'] = GeoMapper.demand_primary_geography
            df['currency'] = cfg.currency_name
            df['currency_year'] = cfg.currency_year
            df['source'] = None
            df['notes'] = None
            df = df.reset_index()
            df = df[['measure',  'source', 'notes', 'subsector','geography', 'gau', 'currency','currency_year','denominator_unit', 'interpolation_method', 'extrapolation_method', 'extrapolation_growth_rate',
                    'vintage', 'value', 'sensitivity']]
            Output.write(df, "DEMAND_EE_COSTS.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_fs_measure_costs(self):
        df = self.demand.group_output('fs_measure_costs', levels_to_keep=cfg.output_demand_levels + ['vintage'])
        if df is not None:
            df = df.stack()
            df = df.reset_index(level='year', drop=True)
            util.replace_index_name(df, 'year', None)
            df.columns = ['value']
            df = df[df.index.get_level_values('vintage') == df.index.get_level_values('year')]
            df = df.groupby(level=[GeoMapper.demand_primary_geography, 'subsector', 'measure', 'vintage'],group_keys=False).mean().to_frame()
            df.columns = ['value']
            util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
            df['denominator_unit'] = cfg.calculation_energy_unit
            df['currency'] = cfg.currency_name
            df['currency_year'] = cfg.currency_year
            df['interpolation_method'] = 'linear_interpolation'
            df['extrapolation_method'] = 'nearest'
            df['extrapolation_growth_rate'] = None
            df['sensitivity'] = self.scenario
            df['geography'] = GeoMapper.demand_primary_geography
            df['currency'] = cfg.currency_name
            df['currency_year'] = cfg.currency_year
            df['source'] = None
            df['notes'] = None
            df = df.reset_index()
            df = df[['measure', 'source', 'notes', 'subsector', 'geography', 'gau', 'currency', 'currency_year', 'denominator_unit', 'interpolation_method', 'extrapolation_method', 'extrapolation_growth_rate',
                     'vintage', 'value', 'sensitivity']]
            Output.write(df, "DEMAND_FS_COSTS.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_dispatch_feeder_allocation(self):
        df_list = []
        subsectors = []
        for sector in self.demand.sectors.values():
            for subsector in sector.subsectors.values():
                df_list.append(subsector.feeder_allocation_class.values)
                subsectors.append(subsector.name)
        df = pd.concat(df_list, keys=subsectors, names=['name'])
        util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
        df = df.reset_index()
        df['geography'] = GeoMapper.demand_primary_geography
        df['sensitivity'] = self.scenario
        df['interpolation_method'] = 'linear_interpolation'
        df['extrapolation_method'] = 'nearest'
        df['extrapolation_growth_rate'] = None
        df['geography_map_key'] = None
        Output.write(df, "DEMAND_DISPATCH_FEEDER_ALLOCATION.csv", self.base_path, compression='gzip', index=False, lower_case=True)



    def write_demand_ee_savings(self):
        df = self.demand.group_output('ee_measure_savings')
        if df is not None:
            df = df.groupby(level=['subsector','final_energy','measure','year', GeoMapper.demand_primary_geography],group_keys=False).sum()
            util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
            df = df[[not self.blend_mapping['drop_final_energy'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]]
            df['blend'] = [self.blend_mapping['blend_group'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]
            df = df.reset_index(level='final_energy', drop=True)
            df = df.set_index('blend', append=True)
            df = df.groupby(level=[df.index.names],group_keys=False).sum()
            df['unit'] = cfg.calculation_energy_unit
            df['interpolation_method'] = 'linear_interpolation'
            df['extrapolation_method'] = 'nearest'
            df['extrapolation_growth_rate'] = None
            df['source'] = None
            df['notes'] = None
            df['sensitivity'] = self.scenario
            df['geography'] = GeoMapper.demand_primary_geography
            df = df.reset_index()
            df = df[['measure',  'source', 'notes', 'subsector','geography', 'gau', 'unit', 'interpolation_method', 'extrapolation_method', 'extrapolation_growth_rate',
                     'blend', 'year', 'value', 'sensitivity']]
            Output.write(df, "DEMAND_EE_SAVINGS.csv", self.base_path, compression='gzip', index=False, lower_case=True)


    def write_demand_fs_savings(self):
        df = self.demand.group_output('fs_measure_savings')
        if df is not None:
            df = df.groupby(level=['subsector','final_energy','measure','year', GeoMapper.demand_primary_geography],group_keys=False).sum()
            util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
            df = df[[not self.blend_mapping['drop_final_energy'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]]
            df['blend'] = [self.blend_mapping['blend_group'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]
            df = df.reset_index(level='final_energy', drop=True)
            df = df.set_index('blend', append=True)
            df = df.groupby(level=[df.index.names],group_keys=False).sum()
            df['unit'] = cfg.calculation_energy_unit
            df['interpolation_method'] = 'linear_interpolation'
            df['extrapolation_method'] = 'nearest'
            df['extrapolation_growth_rate'] = None
            df['source'] = None
            df['notes'] = None
            df['sensitivity'] = self.scenario
            df['geography'] = GeoMapper.demand_primary_geography
            df = df.reset_index()
            df = df[['measure',  'source', 'notes', 'subsector','geography', 'gau', 'unit', 'interpolation_method', 'extrapolation_method', 'extrapolation_growth_rate',
                     'blend', 'year', 'value', 'sensitivity']]
            Output.write(df, "DEMAND_FS_SAVINGS.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_fs_additions(self):
        df = self.demand.group_output('fs_measure_additions')
        if df is not None:
            df = df.groupby(level=['subsector','final_energy','measure','year', GeoMapper.demand_primary_geography],group_keys=False).sum()
            util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
            df = df[[not self.blend_mapping['drop_final_energy'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]]
            df['blend'] = [self.blend_mapping['blend_group'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]
            df = df.reset_index(level='final_energy', drop=True)
            df = df.set_index('blend', append=True)
            df = df.groupby(level=[df.index.names],group_keys=False).sum()
            df['unit'] = cfg.calculation_energy_unit
            df['interpolation_method'] = 'linear_interpolation'
            df['extrapolation_method'] = 'nearest'
            df['extrapolation_growth_rate'] = None
            df['source'] = None
            df['notes'] = None
            df['sensitivity'] = self.scenario
            df['geography'] = GeoMapper.demand_primary_geography
            df = df.reset_index()
            df = df[['measure',   'source', 'notes', 'subsector','geography', 'gau', 'unit', 'interpolation_method', 'extrapolation_method', 'extrapolation_growth_rate',
                     'blend', 'year', 'value', 'sensitivity']]
            Output.write(df, "DEMAND_FS_ADDITIONS.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_tech_capital_costs(self):
        tech_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    for technology in subsector.technologies.values():
                        try:
                           df = util.DfOper.add([technology.capital_cost_new.values,technology.installation_cost_new.values if hasattr(technology.installation_cost_new,'values') else None])
                        except:
                            print ("no capital cost for ", technology.name)
                            continue
                        df = GeoMapper.geo_map(df, GeoMapper.demand_primary_geography, technology.capital_cost_new.geography,'intensity', geography_map_key=None, fill_value=0, filter_geo=False, remove_current_geography=True)
                        util.replace_index_name(df,'name','demand_technology')
                        df['subsector'] = subsector_name
                        util.replace_index_name(df, 'gau',technology.capital_cost_new.geography)
                        length = len([x for x in [technology.capital_cost_new.other_index_1,technology.capital_cost_new.other_index_2] if x is not None])

                        if length == 0:
                            df['other_index'] = None
                        elif length == 1:
                            util.replace_index_name(df, 'other_index', technology.capital_cost_new.other_index_1)
                        elif length ==2:
                            df['other_index'] = df.index.get_level_values(technology.capital_cost_new.other_index_1) + "||" + df.index.get_level_values(technology.capital_cost_new.other_index_2)
                        df['interpolation_method'] = 'linear_interpolation'
                        df['extrapolation_method'] = 'nearest'
                        df['extrapolation_growth_rate'] = None
                        df['sensitivity'] = self.scenario
                        df['geography'] = technology.capital_cost_new.geography
                        df['currency'] = cfg.currency_name
                        df['currency_year'] = cfg.currency_year
                        df['source'] = None
                        df['notes'] = None
                        df = df.reset_index()
                        df = df[['name','subsector','source','notes','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','currency','currency_year','other_index','vintage','value','sensitivity']]
                        tech_dfs.append(df)
        df = pd.concat(tech_dfs)
        df = df.drop_duplicates(subset=df.columns.difference(['vintage']))
        Output.write(df, "DEMAND_TECH_CAPITAL_COST.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_tech_incentives(self):
        tech_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    for technology in subsector.technologies.values():
                        if hasattr(technology.incentive_new,'values') and getattr(technology.incentive_new,'values') is not None:
                            df = technology.incentive_new.values
                            df = GeoMapper.geo_map(df, GeoMapper.demand_primary_geography, technology.incentive_new.geography,'intensity', geography_map_key=None, fill_value=0, filter_geo=False, remove_current_geography=True)
                            util.replace_index_name(df,'name','demand_technology')
                            df['subsector'] = subsector_name
                            util.replace_index_name(df, 'gau',technology.incentive_new.geography)
                            length = len([x for x in [technology.incentive_new.other_index_1,technology.incentive_new.other_index_2] if x is not None])

                            if length == 0:
                                df['other_index'] = None
                            elif length == 1:
                                util.replace_index_name(df, 'other_index', technology.incentive_new.other_index_1)
                            elif length ==2:
                                df['other_index'] = df.index.get_level_values(technology.incentive_new.other_index_1) + "||" + df.index.get_level_values(technology.incentive_new.other_index_2)
                            df['interpolation_method'] = 'linear_interpolation'
                            df['extrapolation_method'] = 'nearest'
                            df['extrapolation_growth_rate'] = None
                            df['sensitivity'] = self.scenario
                            df['geography'] = technology.incentive_new.geography
                            df['currency'] = cfg.currency_name
                            df['currency_year'] = cfg.currency_year
                            df['source'] = None
                            df['notes'] = None
                            df = df.reset_index()
                            df = df[['name','subsector','source','notes','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','currency','currency_year','other_index','vintage','value','sensitivity']]
                            tech_dfs.append(df)
        df = pd.concat(tech_dfs)
        #df = df.drop_duplicates(subset=df.columns.difference(['vintage']))
        Output.write(df, "DEMAND_TECH_INCENTIVE.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_tech_fixed_om(self):
        tech_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    for technology in subsector.technologies.values():
                        if not hasattr(technology.fixed_om,'values'):
                            continue
                        df = technology.fixed_om.values
                        df = GeoMapper.geo_map(df, GeoMapper.demand_primary_geography, technology.fixed_om.geography, 'intensity', geography_map_key=None, fill_value=0, filter_geo=False, remove_current_geography=True)
                        util.replace_index_name(df,'name','demand_technology')
                        df['subsector'] = subsector_name
                        util.replace_index_name(df, 'gau', technology.fixed_om.geography)
                        length = len([x for x in [technology.fixed_om.other_index_1,technology.fixed_om.other_index_2] if x is not None])
                        if length == 0:
                            df['other_index'] = None
                        elif length == 1:
                            util.replace_index_name(df, 'other_index',technology.fixed_om.other_index_1)
                        elif length ==2:
                            df['other_index'] = df.index.get_level_values(technology.fixed_om.other_index_1) + "||" + df.index.get_level_values(technology.fixed_om.other_index_2)
                        df['interpolation_method'] = 'linear_interpolation'
                        df['extrapolation_method'] = 'nearest'
                        df['extrapolation_growth_rate'] = None
                        df['sensitivity'] = self.scenario
                        df['geography'] = GeoMapper.demand_primary_geography
                        df['currency'] = cfg.currency_name
                        df['currency_year'] = cfg.currency_year
                        df['source'] = None
                        df['notes'] = None
                        df = df.reset_index()
                        df['year'] = df['vintage']
                        df = df[['name', 'subsector','source','notes','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','currency','currency_year','other_index','vintage','year','value','sensitivity']]
                        tech_dfs.append(df)
        df = pd.concat(tech_dfs)
        df = df.drop_duplicates(subset=df.columns.difference(['vintage','year']))
        Output.write(df, "DEMAND_TECH_FIXED_OM.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_tech_efficiency(self):
        tech_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    for technology in subsector.technologies.values():
                        efficiency = technology.efficiency_main.values[max(cfg.rio_years)].to_frame()
                        efficiency.columns = ['value']
                        if len(GeoMapper.geography_to_gau[technology.efficiency_main.geography])>1:
                            geography = GeoMapper.demand_primary_geography
                        else:
                            efficiency = GeoMapper.geo_map(efficiency, GeoMapper.demand_primary_geography, technology.efficiency_main.geography, 'intensity', geography_map_key= technology.efficiency_main.geography_map_key, fill_value=0, filter_geo=False, remove_current_geography=True)
                            geography = technology.efficiency_main.geography

                        if technology.efficiency_main.utility_factor !=1:
                            efficiency_aux = technology.efficiency_aux.values[max(cfg.rio_years)].to_frame() if hasattr(technology.efficiency_aux,'values') else None
                            efficiency_aux.columns = ['value']
                            if len(GeoMapper.geography_to_gau[technology.efficiency_main.geography]) == 1:
                                efficiency_aux = GeoMapper.geo_map(efficiency_aux, GeoMapper.demand_primary_geography, technology.efficiency_main.geography, 'intensity', geography_map_key=technology.efficiency_main.geography_map_key, fill_value=0, filter_geo=False, remove_current_geography=True)
                            efficiency_aux *= 1- technology.efficiency_main.utility_factor
                            efficiency_main = efficiency * technology.efficiency_main.utility_factor
                            efficiency = util.DfOper.add([efficiency_aux,efficiency_main])
                        df = efficiency
                        util.replace_index_name(df,'name','demand_technology')
                        df['subsector'] = subsector_name
                        util.replace_index_name(df, 'gau', geography)
                        df = df[[not self.blend_mapping['drop_final_energy'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]]
                        df['blend_in'] = [self.blend_mapping['blend_group'][x] for x in zip(df.index.get_level_values('subsector'), df.index.get_level_values('final_energy'))]
                        length = len([x for x in [technology.efficiency_main.other_index_1,technology.efficiency_main.other_index_2] if x is not None])
                        if length == 0:
                            df['other_index'] = None
                        elif length == 1:
                            util.replace_index_name(df, 'other_index', technology.efficiency_main.other_index_1)
                        elif length ==2:
                            df['other_index'] = df.index.get_level_values(technology.efficiency_main.other_index_1) + "||" + df.index.get_level_values(technology.efficiency_main.other_index_2)
                        df['interpolation_method'] = 'linear_interpolation'
                        df['extrapolation_method'] = 'nearest'
                        df['extrapolation_growth_rate'] = None
                        df['sensitivity'] = self.scenario
                        df['geography'] = geography
                        df['source'] = None
                        df['notes'] = None
                        df['is_numerator_service'] = True
                        energy_unit_to = technology.efficiency_main.denominator_unit if technology.efficiency_main.is_numerator_service else technology.efficiency_main.numerator_unit
                        df['denominator_unit'] =  energy_unit_to
                        df['numerator_unit'] = technology.service_demand_unit
                        df = df.reset_index()
                        df['value'] = 1/df['value']
                        df = df[df['vintage'].values>=min(cfg.rio_years)]
                        df['value']*= UnitConverter.unit_convert(1,
                                                   unit_from_den=cfg.calculation_energy_unit,
                                                   unit_to_den=energy_unit_to)
                        df = df[['name', 'subsector','source','notes','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate',
                                 'is_numerator_service','numerator_unit','denominator_unit','blend_in','other_index','vintage','value','sensitivity']]
                        tech_dfs.append(df)
        df = pd.concat(tech_dfs)
        #fuel_df = df[~df['blend_in'].isin(['electricity'])].drop_duplicates(subset=df.columns.difference(['vintage']))
        Output.write(df, "DEMAND_TECH_EFFICIENCY.csv", self.base_path, compression='gzip', index=False, lower_case=True)
        #
        # electric_df = df[df['blend_in'].isin(['electricity'])]
        # electric_df = electric_df.drop('blend_in', axis=1)
        # electric_df = electric_df.drop_duplicates(subset=electric_df.columns.difference(['vintage']))
        # Output.write(electric_df, "DEMAND_TECH_ELECTRIC_EFFICIENCY.csv", self.base_path, compression='gzip', index=False, lower_case=True)


    def write_demand_tech_service_demand_modifier(self):
        tech_dfs = []
        tech_names = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    for technology in subsector.technologies.values():
                        if not hasattr(technology.service_demand_modifier,'values'):
                            continue
                        df = technology.service_demand_modifier.values
                        df = df.stack('year').to_frame()
                        df.columns = ['value']
                        df = GeoMapper.geo_map(df, GeoMapper.demand_primary_geography, technology.service_demand_modifier.geography, 'intensity', geography_map_key=None, fill_value=0, filter_geo=False, remove_current_geography=True)
                        util.replace_index_name(df,'name','demand_technology')
                        df['subsector'] = subsector_name
                        util.replace_index_name(df, 'gau', technology.service_demand_modifier.geography)
                        length = len([x for x in [technology.service_demand_modifier.other_index_1,technology.service_demand_modifier.other_index_2] if x is not None])
                        if length == 0:
                            df['other_index'] = None
                        elif length == 1:
                            util.replace_index_name(df, 'other_index', technology.service_demand_modifier.other_index_1)
                        elif length ==2:
                            df['other_index'] = df.index.get_level_values(technology.service_demand_modifier.other_index_1) + "||" + df.index.get_level_values(technology.service_demand_modifier.other_index_2)
                        df['interpolation_method'] = 'linear_interpolation'
                        df['extrapolation_method'] = 'nearest'
                        df['extrapolation_growth_rate'] = None
                        df['sensitivity'] = self.scenario
                        df['geography'] = GeoMapper.demand_primary_geography
                        df['source'] = None
                        df['notes'] = None
                        df = df.reset_index()
                        df = df[['subsector','source','notes','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate',
                                 'other_index','vintage','year','value','sensitivity']]
                        tech_dfs.append(df)
                        tech_names.append(technology.name)

        df = pd.concat(tech_dfs,keys=tech_names,names=['name'])
        df = df.reset_index()
        del df['level_1']
        df = df.drop_duplicates(subset=df.columns.difference(['vintage','year']))
        df['age'] = df['year'] - df['vintage']
        del df['year']
        Output.write(df, "DEMAND_TECH_SERVICE_DEMAND_MODIFIER.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_tech_main(self):
        dct = defaultdict(list)
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    for tech in subsector.technologies.values():
                        dct['name'].append(tech.name)
                        dct['subsector'].append(subsector_name)
                        dct['lifetime'].append(tech.mean_lifetime)
                        dct['outputs_group_aggregate'].append(tech.name)
                        dct['outputs_group_detailed'].append(tech.name)
                        dct['demand_tech_unit_type'].append(tech.demand_tech_unit_type)
                        dct['linked_tech'].append(tech.linked)
                        dct['link_ratio'].append(tech.stock_link_ratio)
                        dct['unit'].append(subsector.stock.unit)
                        dct['time_unit'].append(subsector.stock.time_unit)
                        dct['shape'].append(None if tech.shape==None else tech.shape)
                        dct['timestep'] = 'sample'


        df = pd.DataFrame(dct)
        Output.write(df, "DEMAND_TECH_MAIN.csv", self.base_path, compression='gzip', index=False, lower_case=True)

@click.command()
@click.option('--replace/--update', default=True, help='Replace files in the RIO directory or update them.')
def click_run(replace):
    run(replace)

def run(replace):
    cfg.initialize_config()
    GeoMapper.get_instance().log_geo()
    riodbdir = cfg.getParam('rio_database_path', section='RIO_DB')
    rio_db = RioDatabase.get_database(riodbdir, load=False)
    logging.info('Exporting to RIO database path {}'.format(riodbdir))
    rio_shape_dir = cfg.getParam('shape_database_path', section='RIO_DB')
    if rio_shape_dir is None:
        rio_shape_dir = os.path.join(riodbdir, 'Shapes', 'ShapeData')
    elif os.path.split(rio_shape_dir)[1] != 'ShapeData':
        rio_shape_dir = os.path.join(rio_shape_dir, 'ShapeData')

    # start with the csv files
    ep_base_dir = os.path.join(cfg.workingdir, '_aggregate_outputs_EP', 'EP2RIO')
    export_to_rio_files = os.listdir(ep_base_dir)
    export_to_rio_files = [file_name[:-4] for file_name in export_to_rio_files if file_name[-4:] == '.csv']
    for file_name in export_to_rio_files:
        if file_name not in rio_db.file_map:
            logging.info('WARNING file {} not found in the RIO database.'.format(file_name))
            continue
        else:
            if file_name=='SHAPE_META':
                append_when_existing, special_subset = True, ['name']
            else:
                append_when_existing, special_subset = not replace, None
            logging.info('Exporting file {} to the RIO database.'.format(file_name))

        if type(rio_db.file_map[file_name]) is list:
            csvd_file_names = [os.path.split(fm)[1].split('.')[0] for fm in rio_db.file_map[file_name]]
            file_map = rio_db.file_map[file_name][csvd_file_names.index(file_name)]
        else:
            file_map = rio_db.file_map[file_name]

        df = pd.read_csv(os.path.join(ep_base_dir, file_name + '.csv'), index_col=False)
        # want to remove all duplicates
        df = df.drop_duplicates()
        compression = 'gzip' if file_map[-3:]=='.gz' else None
        Output.write_rio(df, file_map, compression=compression, index=False, update=True, append_when_existing=append_when_existing, special_subset=special_subset)

    # special case for DEMAND_LEVELIZED_COSTS because of its size
    rio_dir = os.path.join(riodbdir, 'Demand', 'Exogenous EP Inputs', 'DEMAND_LEVELIZED_COSTS.csvd')
    ep_dir = os.path.join(ep_base_dir, 'DEMAND_LEVELIZED_COSTS.csvd')
    if os.path.exists(ep_dir):
        if os.path.isdir(rio_dir):
            if replace:
                delete_csv_files_in_folder(rio_dir)
        else:
            os.makedirs(rio_dir)

        for f in os.listdir(ep_dir):
            shutil.copy2(os.path.join(ep_dir, f), os.path.join(rio_dir, f))

    rio_dir = os.path.join(riodbdir, 'Demand', 'Exogenous EP Inputs', 'DEMAND_SPEND.csvd')
    ep_dir = os.path.join(ep_base_dir, 'DEMAND_SPEND.csvd')
    if os.path.exists(ep_dir):
        if os.path.isdir(rio_dir):
            if replace:
                delete_csv_files_in_folder(rio_dir)
        else:
            os.makedirs(rio_dir)

        for f in os.listdir(ep_dir):
            shutil.copy2(os.path.join(ep_dir, f), os.path.join(rio_dir, f))

    # now export shapes
    ep_shape_dir = os.path.join(ep_base_dir, 'ShapeData')
    for shape_type in os.listdir(ep_shape_dir):
        input_directory = os.path.join(ep_shape_dir, shape_type)
        output_directory = os.path.join(rio_shape_dir, shape_type)
        if os.path.isdir(output_directory):
            delete_csv_files_in_folder(output_directory)
        else:
            os.makedirs(output_directory)

        for f in os.listdir(input_directory):
            shutil.copy2(os.path.join(input_directory, f), os.path.join(output_directory, f))

    logging.info('Finished export to RIO')


if __name__ == "__main__":
    workingdir = r'E:\ep_runs\annual_refresh_2022_new_shapes'
    os.chdir(workingdir)
    run(replace=True)
