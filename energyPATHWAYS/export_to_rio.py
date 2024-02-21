
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
from energyPATHWAYS import shapes2
import energyPATHWAYS.scenario_loader as scenario_loader
from energyPATHWAYS.geomapper import GeoMapper
from energyPATHWAYS.unit_converter import UnitConverter
import click
import datetime as DT

class RioExport(object):
    def __init__(self, model):
        self.model = model
        self.demand = model.demand
        self.scenario = model.scenario_id
        self.base_path = os.path.join(cfg.workingdir, self.scenario, 'EP2RIO')
        logging.info(self.base_path)
        self.scenario_index = 0

    def write_all(self):
        self.write_demand_shapes()
        self.write_demand_subsector()
        self.write_demand_side_levelized_costs()
        self.write_exo_demand()



    def write_demand_side_levelized_costs(self):
        logging.info('EP2RIO: Writing demand-side levelized cost')
        df = self.demand.group_output('levelized_costs',levels_to_keep=['year', 'vintage', GeoMapper.demand_primary_geography, 'subsector'])
        df = df.groupby(level=df.index.names).sum()
        df = GeoMapper.geo_map(df, GeoMapper.demand_primary_geography, GeoMapper.demand_primary_geography, 'total')
        df = df.reorder_levels(['year', 'vintage', GeoMapper.demand_primary_geography, 'subsector']).sort_index()
        currency = df.columns[0].split()[1].lower()
        currency_year = df.columns[0].split()[0]
        df.columns = ['value']
        existing_subsectors = df.index.get_level_values('subsector').unique()
        missing_subsectors = util.flatten_list([[subsector_name for subsector_name in sector.subsectors.keys() if subsector_name not in existing_subsectors] for sector in self.demand.sectors.values()])
        new_index = pd.MultiIndex.from_product([cfg.years, cfg.years, GeoMapper.demand_geographies, missing_subsectors], names=['year', 'vintage', GeoMapper.demand_primary_geography, 'subsector'])
        missing_subsector_df = pd.DataFrame(0, index=new_index, columns=['value'])
        missing_subsector_df = missing_subsector_df[missing_subsector_df.index.get_level_values('vintage') <= missing_subsector_df.index.get_level_values('year')]
        df = pd.concat([df, missing_subsector_df])
        util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
        df['currency'] = currency
        df['currency_year'] = currency_year
        df['interpolation_method'] = 'linear_interpolation'
        df['extrapolation_method'] = 'nearest'
        df['extrapolation_growth_rate'] = 0
        df['geography'] = GeoMapper.demand_primary_geography
        df['sensitivity'] = self.scenario
        df = df.reset_index()
        df = df[['subsector','currency', 'currency_year','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','vintage','year','value','sensitivity']]
        df['value'] = df['value'].round(0)
        path = os.path.join(self.base_path, 'DEMAND_LEVELIZED_COSTS.csvd')
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
        exo_demand.set_index([x for x in exo_demand.columns if x!='value'],inplace=True)

        def filter_exo(df):
            if (df==0).all().all():
                df = df.xs(df.index.get_level_values('year')[0], level='year', drop_level=False).xs(df.index.get_level_values('blend')[0], level='blend', drop_level=False)
            else:
                df = df.groupby(level=['blend']).filter(lambda x: x.sum()!=0)
            return util.remove_df_levels(df, 'name')

        exo_demand = exo_demand.groupby(level=['name']).apply(filter_exo)
        exo_demand = exo_demand.reset_index()[['name', 'sector','unit', 'geography', 'gau',
                 'interpolation_method', 'extrapolation_method','blend',
                 'year', 'value', 'sensitivity']]

        Output.write(exo_demand, "EXO_DEMAND.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def get_blend_exo_demand(self):
        df = self.demand.outputs.d_energy.groupby(level=['year','sector','subsector',GeoMapper.demand_primary_geography,'final_energy', 'unit']).sum()
        # subset df for just the rio run years
        df = df.loc[(cfg.rio_years, slice(None), slice(None), slice(None), slice(None), slice(None)),:]
        final_energy = util.table_data('FinalEnergy')[['name', 'blend_group']].set_index('name').to_dict()['blend_group']

        feu = df.index.get_level_values('final_energy').unique()
        if any([key not in final_energy for key in feu]):
            missing = [key for key in feu if key not in final_energy]
            logging.warning('The following final energy types are missing from the final energy table but found in final energy demand: {}'.format(missing))
            logging.warning('THESE FINAL ENERGY TYPES WILL BE DROPPED')

        df['blend'] = [final_energy.get(x, None) for x in df.index.get_level_values('final_energy')]
        df = df[(df['blend'].notnull()).values]
        df = df.set_index('blend', append=True)
        df = df.groupby(level=['year','sector','subsector',GeoMapper.demand_primary_geography,'blend','unit']).sum()

        df_electricity = df.xs('electricity', level='blend', drop_level=False)
        df_electricity *= UnitConverter.unit_convert(unit_from_num=cfg.calculation_energy_unit,unit_to_num='GWh')
        df_electricity = Output.clean_rio_df(df_electricity)
        df_electricity['unit'] = 'gigawatt_hour'

        # get the blends that are not 'electricity', these already have units
        df_non_electricity = df.drop('electricity', level='blend')
        df_non_electricity = Output.clean_rio_df(df_non_electricity)

        # special case where we reverse the sign when exporting to RIO for some blends
        reverse_sign = util.table_data('FinalEnergy')[['blend_group', 'reverse_sign_EP2RIO']].drop_duplicates()
        reverse_sign_dict = reverse_sign.set_index('blend_group').to_dict()['reverse_sign_EP2RIO']
        df_non_electricity['value'] *= np.array([-1 if reverse_sign_dict[x] else 1 for x in df_non_electricity['blend'].values])

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
            # allocate_to_feeder = False
            written_years = []
            dfs = []
            for year in cfg.rio_years:
                df = self.demand.aggregate_final_energy_shapes(year, final_energy, reconciliation_step=False, allocate_to_feeder=allocate_to_feeder, exclude_subsectors=cfg.rio_optimizable_subsectors)
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
            sector_name = [sector.name for sector in self.demand.sectors.values() if subsector_name in sector.subsectors][0]
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
            try:
                Output.write(pd.concat(dfs), file_name, path, compression='gzip', index=False, lower_case=True)
            except:
                pdb.set_trace()

        Output.write(pd.DataFrame(shape_meta[1:], columns=shape_meta[0]), 'SHAPE_META.csv', self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_subsector(self):
        logging.info('EP2RIO: Writing demand-side technology inputs')
        if len(cfg.rio_optimizable_subsectors):
            self.write_demand_existing_service_demand()
            self.write_demand_service_demand()
            self.write_demand_tech_existing_demand()
            #self.write_demand_tech_main()
            self.write_demand_tech_service_demand()
            self.write_demand_tech_sales()
            self.write_demand_tech_capital_costs()
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

        Output.write(df, "DEMAND_TECH_SALES.csv", self.base_path, compression='gzip', index=False, lower_case=True)
        df = df[df['vintage'].isin(cfg.rio_years)]
        df['value'] = 1
        df['interpolation_method'] = 'logistic'
        Output.write(df, "DEMAND_TECH_SALES_CAP.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_service_demand(self):
        service_demand_dfs = []
        subsector_names = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    df = subsector.service_demand.values.stack('year').to_frame()
                    df.columns = ['value']
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
                    df['sensitivity'] =  self.scenario
                    df['geography'] = GeoMapper.demand_primary_geography
                    df['unit'] = subsector.service_demand.unit
                    df = df.reset_index()
                    df = df[['source','notes','geography','gau','unit','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','other_index','year','value','sensitivity']]
                    service_demand_dfs.append(df)
                    subsector_names.append(subsector_name)
        df = pd.concat(service_demand_dfs,keys=subsector_names,names=['name']).reset_index()
        del df['level_1']
        Output.write(df, "DEMAND_SERVICE_DEMAND.csv", self.base_path, compression='gzip', index=False, lower_case=True)

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

    def write_demand_existing_service_demand(self):
        service_demand_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    df = util.DfOper.mult([subsector.stock.values_normal, subsector.service_demand.modifier,subsector.service_demand.values])
                    df = df.stack().to_frame()
                    util.replace_index_name(df,'year')
                    df.columns = ['value']
                    df = util.remove_df_levels(df,['final_energy','demand_technology'])
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
                    df['sensitivity'] =  self.scenario
                    df['geography'] = GeoMapper.demand_primary_geography
                    df['unit'] = subsector.service_demand.unit
                    df['name'] = subsector_name
                    df = df.reset_index()
                    df = df[['name','source','notes','geography','gau','unit','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','other_index','vintage','year','value','sensitivity']]
                    service_demand_dfs.append(df)
        df = pd.concat(service_demand_dfs)
        Output.write(df, "DEMAND_EXISTING_SERVICE_DEMAND.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_tech_existing_demand(self):
        demand_dfs = []
        final_energy = util.table_data('FinalEnergy')[['name', 'blend_group']].set_index('name').to_dict()['blend_group']
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    df = subsector.energy_forecast
                    #df = util.remove_df_levels(df,['technology'])
                    util.replace_index_name(df, 'gau', GeoMapper.demand_primary_geography)
                    df['blend_in'] = [final_energy.get(x, None) for x in df.index.get_level_values('final_energy')]
                    df = df[(df['blend_in'].notnull()).values]
                    df = util.remove_df_levels(df,['final_energy'])
                    util.replace_index_name(df,'name','demand_technology')
                    if 'other_index_1' not in df.index.names:
                        df['other_index'] = None
                    elif 'other_index_1' and 'other_index_2' in df.index.names:
                        df['other_index'] = [x + "||" + y for x,y in zip(df.index.get_level_values(subsector.service_demand.other_index_1),df.index.get_level_values(subsector.service_demand.other_index_2))]
                    elif 'other_index_1' in df.index.names:
                        util.replace_index_name(df, 'other_index','other_index_1')
                    df['interpolation_method'] = 'linear_interpolation'
                    df['extrapolation_method'] = 'nearest'
                    df['extrapolation_growth_rate'] = None
                    df['source'] = None
                    df['notes'] = None
                    df['sensitivity'] =  self.scenario
                    df['geography'] = GeoMapper.demand_primary_geography
                    df['unit'] = cfg.calculation_energy_unit
                    df['subsector'] = subsector_name
                    df = df.reset_index()
                    df = df[['name','subsector','source','notes','geography','gau','unit','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','other_index',
                             'blend_in','vintage','year','value','sensitivity']]
                    demand_dfs.append(df)
        df = pd.concat(demand_dfs)
        Output.write(df, "DEMAND_TECH_EXISTING_DEMAND.csv", self.base_path, compression='gzip', index=False, lower_case=True)

    def write_demand_tech_capital_costs(self):
        tech_dfs = []
        for subsector_name in cfg.rio_optimizable_subsectors:
            for sector in self.demand.sectors.values():
                if subsector_name in sector.subsectors.keys():
                    subsector = sector.subsectors[subsector_name]
                    for technology in subsector.technologies.values():
                        df = util.DfOper.add([technology.capital_cost_new.values,technology.installation_cost_new.values if hasattr(technology.installation_cost_new,'values') else None])
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
                        df['sensitivity'] = None
                        df['geography'] = technology.capital_cost_new.geography
                        df['currency'] = cfg.currency_name
                        df['currency_year'] = cfg.output_currency
                        df['source'] = None
                        df['notes'] = None
                        df = df.reset_index()
                        df = df[['name','subsector','source','notes','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate','currency','currency_year','other_index','vintage','value','sensitivity']]
                        tech_dfs.append(df)
        df = pd.concat(tech_dfs)
        df = df.drop_duplicates(subset=df.columns.difference(['vintage']))
        Output.write(df, "DEMAND_TECH_CAPITAL_COST.csv", self.base_path, compression='gzip', index=False, lower_case=True)

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
                        df['sensitivity'] = None
                        df['geography'] = GeoMapper.demand_primary_geography
                        df['currency'] = cfg.currency_name
                        df['currency_year'] = cfg.output_currency
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
        final_energy = util.table_data('FinalEnergy')[['name', 'blend_group']].set_index('name').to_dict()['blend_group']
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
                        df['blend_in'] = [final_energy.get(x, None) for x in df.index.get_level_values('final_energy')]
                        df = df[(df['blend_in'].notnull()).values]
                        length = len([x for x in [technology.efficiency_main.other_index_1,technology.efficiency_main.other_index_2] if x is not None])
                        if length == 0:
                            df['other_index'] = None
                        elif length == 1:
                            util.replace_index_name(df, 'other_index', technology.efficiency_main.other_index_1)
                        elif length ==2:
                            df['other_index'] = df.index.get_level_values(technology.efficiency_main.other_index_1) + "||" + df.index.get_level_values(technology.efficiency_main.other_index_2)
                        df['interpolation_method'] = 'logistic'
                        df['extrapolation_method'] = 'nearest'
                        df['extrapolation_growth_rate'] = None
                        df['sensitivity'] = None
                        df['geography'] = geography
                        df['source'] = None
                        df['notes'] = None
                        df['is_numerator_service'] = True
                        energy_unit_to = technology.efficiency_main.denominator_unit if technology.efficiency_main.is_numerator_service else technology.efficiency_main.numerator_unit
                        df['denominator_unit'] =  energy_unit_to
                        df['numerator_unit'] = technology.service_demand_unit
                        df = df.reset_index()
                        df['value'] = 1/df['value']
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
                        df['interpolation_method'] = 'logistic'
                        df['extrapolation_method'] = 'nearest'
                        df['extrapolation_growth_rate'] = None
                        df['sensitivity'] = None
                        df['geography'] = GeoMapper.demand_primary_geography
                        df['source'] = None
                        df['notes'] = None
                        df = df.reset_index()
                        df = df[['subsector','source','notes','geography','gau','interpolation_method','extrapolation_method', 'extrapolation_growth_rate',
                                 'other_index','vintage','year','value','sensitivity']]
                        tech_dfs.append(df)
                        tech_names.append(technology.name)
        df = pd.concat(tech_dfs,keys=tech_names,names=['name']).reset_index()
        del df['level_1']
        df = df.drop_duplicates(subset=df.columns.difference(['vintage','year']))
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
                        dct['unit'].append(tech.unit)
                        dct['time_unit'].append(tech.time_unit)
                        dct['shape'].append('flat' if tech.shape==None else tech.shape)
                        dct['optimize'] = 'True'


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
    from RIO.riodb.rio_db_loader import RioDatabase
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
