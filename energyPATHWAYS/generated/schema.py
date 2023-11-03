#
# This is a generated file. Manual edits may be lost!
#
import sys
from energyPATHWAYS.data_object import DataObject # superclass of generated classes

_Module = sys.modules[__name__]  # get ref to our own module object

class DemandDrivers(DataObject):
    _instances_by_key = {}
    _table_name = "DemandDrivers"
    _key_col = 'name'
    _cols = ["base_driver", "extrapolation_growth", "extrapolation_method", "geography",
             "geography_map_key", "input_type", "interpolation_method", "name", "other_index_1",
             "other_index_2", "unit_base", "unit_prefix"]
    _df_cols = ["gau", "value", "oth_2", "oth_1", "year", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandDrivers._instances_by_key[self._key] = self

        self.base_driver = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.geography_map_key = None
        self.input_type = None
        self.interpolation_method = None
        self.name = name
        self.other_index_1 = None
        self.other_index_2 = None
        self.unit_base = None
        self.unit_prefix = None

    def set_args(self, scenario, base_driver=None, extrapolation_growth=None, extrapolation_method=None, geography=None,
                 geography_map_key=None, input_type=None, interpolation_method=None, name=None,
                 other_index_1=None, other_index_2=None, unit_base=None, unit_prefix=None):
        self.check_scenario(scenario)

        self.base_driver = base_driver
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.name = name
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.unit_base = unit_base
        self.unit_prefix = unit_prefix

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, base_driver, input_type, unit_prefix, unit_base, geography, other_index_1,
         other_index_2, geography_map_key, interpolation_method, extrapolation_method,
         extrapolation_growth,) = tup

        self.set_args(scenario, base_driver=base_driver, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography,
                  geography_map_key=geography_map_key, input_type=input_type,
                  interpolation_method=interpolation_method, name=name, other_index_1=other_index_1,
                  other_index_2=other_index_2, unit_base=unit_base, unit_prefix=unit_prefix)

class DemandEnergyDemands(DataObject):
    _instances_by_key = {}
    _table_name = "DemandEnergyDemands"
    _key_col = 'subsector'
    _cols = ["demand_technology_index", "driver_1", "driver_2", "driver_3", "driver_denominator_1",
             "driver_denominator_2", "extrapolation_growth", "extrapolation_method",
             "final_energy_index", "geography", "geography_map_key", "input_type",
             "interpolation_method", "is_stock_dependent", "other_index_1", "other_index_2",
             "subsector", "unit"]
    _df_cols = ["gau", "demand_technology", "value", "oth_2", "oth_1", "year", "final_energy",
             "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, subsector, scenario):
        DataObject.__init__(self, subsector, scenario)

        DemandEnergyDemands._instances_by_key[self._key] = self

        self.demand_technology_index = None
        self.driver_1 = None
        self.driver_2 = None
        self.driver_3 = None
        self.driver_denominator_1 = None
        self.driver_denominator_2 = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.final_energy_index = None
        self.geography = None
        self.geography_map_key = None
        self.input_type = None
        self.interpolation_method = None
        self.is_stock_dependent = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.subsector = subsector
        self.unit = None

    def set_args(self, scenario, demand_technology_index=None, driver_1=None, driver_2=None, driver_3=None,
                 driver_denominator_1=None, driver_denominator_2=None, extrapolation_growth=None,
                 extrapolation_method=None, final_energy_index=None, geography=None,
                 geography_map_key=None, input_type=None, interpolation_method=None,
                 is_stock_dependent=None, other_index_1=None, other_index_2=None, subsector=None,
                 unit=None):
        self.check_scenario(scenario)

        self.demand_technology_index = demand_technology_index
        self.driver_1 = driver_1
        self.driver_2 = driver_2
        self.driver_3 = driver_3
        self.driver_denominator_1 = driver_denominator_1
        self.driver_denominator_2 = driver_denominator_2
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.final_energy_index = final_energy_index
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.is_stock_dependent = is_stock_dependent
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.subsector = subsector
        self.unit = unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (subsector, is_stock_dependent, input_type, unit, driver_denominator_1,
         driver_denominator_2, driver_1, driver_2, driver_3, geography, final_energy_index,
         demand_technology_index, other_index_1, other_index_2, interpolation_method,
         extrapolation_method, extrapolation_growth, geography_map_key,) = tup

        self.set_args(scenario, demand_technology_index=demand_technology_index, driver_1=driver_1, driver_2=driver_2,
                  driver_3=driver_3, driver_denominator_1=driver_denominator_1,
                  driver_denominator_2=driver_denominator_2, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, final_energy_index=final_energy_index,
                  geography=geography, geography_map_key=geography_map_key, input_type=input_type,
                  interpolation_method=interpolation_method, is_stock_dependent=is_stock_dependent,
                  other_index_1=other_index_1, other_index_2=other_index_2, subsector=subsector, unit=unit)

class DemandEnergyEfficiencyMeasures(DataObject):
    _instances_by_key = {}
    _table_name = "DemandEnergyEfficiencyMeasures"
    _key_col = 'name'
    _cols = ["extrapolation_growth", "extrapolation_method", "geography", "input_type",
             "interpolation_method", "lifetime_variance", "max_lifetime", "mean_lifetime",
             "min_lifetime", "name", "other_index_1", "other_index_2", "stock_decay_function",
             "subsector", "unit"]
    _df_cols = ["gau", "value", "oth_2", "oth_1", "year", "final_energy"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandEnergyEfficiencyMeasures._instances_by_key[self._key] = self

        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.input_type = None
        self.interpolation_method = None
        self.lifetime_variance = None
        self.max_lifetime = None
        self.mean_lifetime = None
        self.min_lifetime = None
        self.name = name
        self.other_index_1 = None
        self.other_index_2 = None
        self.stock_decay_function = None
        self.subsector = None
        self.unit = None

    def set_args(self, scenario, extrapolation_growth=None, extrapolation_method=None, geography=None, input_type=None,
                 interpolation_method=None, lifetime_variance=None, max_lifetime=None, mean_lifetime=None,
                 min_lifetime=None, name=None, other_index_1=None, other_index_2=None,
                 stock_decay_function=None, subsector=None, unit=None):
        self.check_scenario(scenario)

        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.lifetime_variance = lifetime_variance
        self.max_lifetime = max_lifetime
        self.mean_lifetime = mean_lifetime
        self.min_lifetime = min_lifetime
        self.name = name
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.stock_decay_function = stock_decay_function
        self.subsector = subsector
        self.unit = unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, subsector, input_type, unit, geography, other_index_1, other_index_2,
         interpolation_method, extrapolation_method, extrapolation_growth, stock_decay_function,
         min_lifetime, max_lifetime, mean_lifetime, lifetime_variance,) = tup

        self.set_args(scenario, extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, input_type=input_type, interpolation_method=interpolation_method,
                  lifetime_variance=lifetime_variance, max_lifetime=max_lifetime,
                  mean_lifetime=mean_lifetime, min_lifetime=min_lifetime, name=name,
                  other_index_1=other_index_1, other_index_2=other_index_2,
                  stock_decay_function=stock_decay_function, subsector=subsector, unit=unit)

class DemandEnergyEfficiencyMeasuresCost(DataObject):
    _instances_by_key = {}
    _table_name = "DemandEnergyEfficiencyMeasuresCost"
    _key_col = 'parent'
    _cols = ["cost_denominator_unit", "cost_of_capital", "currency", "currency_year",
             "extrapolation_growth", "extrapolation_method", "geography", "interpolation_method",
             "is_levelized", "other_index_1", "other_index_2", "parent"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "final_energy"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, parent, scenario):
        DataObject.__init__(self, parent, scenario)

        DemandEnergyEfficiencyMeasuresCost._instances_by_key[self._key] = self

        self.cost_denominator_unit = None
        self.cost_of_capital = None
        self.currency = None
        self.currency_year = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.is_levelized = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.parent = parent

    def set_args(self, scenario, cost_denominator_unit=None, cost_of_capital=None, currency=None, currency_year=None,
                 extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, is_levelized=None, other_index_1=None, other_index_2=None,
                 parent=None):
        self.check_scenario(scenario)

        self.cost_denominator_unit = cost_denominator_unit
        self.cost_of_capital = cost_of_capital
        self.currency = currency
        self.currency_year = currency_year
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.is_levelized = is_levelized
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.parent = parent

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (parent, currency, currency_year, cost_denominator_unit, cost_of_capital, is_levelized,
         geography, other_index_1, other_index_2, interpolation_method, extrapolation_method,
         extrapolation_growth,) = tup

        self.set_args(scenario, cost_denominator_unit=cost_denominator_unit, cost_of_capital=cost_of_capital,
                  currency=currency, currency_year=currency_year,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method,
                  is_levelized=is_levelized, other_index_1=other_index_1, other_index_2=other_index_2,
                  parent=parent)

class DemandFuelSwitchingMeasures(DataObject):
    _instances_by_key = {}
    _table_name = "DemandFuelSwitchingMeasures"
    _key_col = 'name'
    _cols = ["final_energy_from", "final_energy_to", "lifetime_variance", "max_lifetime",
             "mean_lifetime", "min_lifetime", "name", "stock_decay_function", "subsector"]
    _df_cols = []
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandFuelSwitchingMeasures._instances_by_key[self._key] = self

        self.final_energy_from = None
        self.final_energy_to = None
        self.lifetime_variance = None
        self.max_lifetime = None
        self.mean_lifetime = None
        self.min_lifetime = None
        self.name = name
        self.stock_decay_function = None
        self.subsector = None

    def set_args(self, scenario, final_energy_from=None, final_energy_to=None, lifetime_variance=None, max_lifetime=None,
                 mean_lifetime=None, min_lifetime=None, name=None, stock_decay_function=None,
                 subsector=None):
        self.check_scenario(scenario)

        self.final_energy_from = final_energy_from
        self.final_energy_to = final_energy_to
        self.lifetime_variance = lifetime_variance
        self.max_lifetime = max_lifetime
        self.mean_lifetime = mean_lifetime
        self.min_lifetime = min_lifetime
        self.name = name
        self.stock_decay_function = stock_decay_function
        self.subsector = subsector

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, subsector, final_energy_from, final_energy_to, stock_decay_function, max_lifetime,
         min_lifetime, mean_lifetime, lifetime_variance,) = tup

        self.set_args(scenario, final_energy_from=final_energy_from, final_energy_to=final_energy_to,
                  lifetime_variance=lifetime_variance, max_lifetime=max_lifetime,
                  mean_lifetime=mean_lifetime, min_lifetime=min_lifetime, name=name,
                  stock_decay_function=stock_decay_function, subsector=subsector)

class DemandFuelSwitchingMeasuresCost(DataObject):
    _instances_by_key = {}
    _table_name = "DemandFuelSwitchingMeasuresCost"
    _key_col = 'parent'
    _cols = ["cost_denominator_unit", "cost_of_capital", "currency", "currency_year",
             "extrapolation_growth", "extrapolation_method", "geography", "interpolation_method",
             "is_levelized", "other_index_1", "other_index_2", "parent"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, parent, scenario):
        DataObject.__init__(self, parent, scenario)

        DemandFuelSwitchingMeasuresCost._instances_by_key[self._key] = self

        self.cost_denominator_unit = None
        self.cost_of_capital = None
        self.currency = None
        self.currency_year = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.is_levelized = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.parent = parent

    def set_args(self, scenario, cost_denominator_unit=None, cost_of_capital=None, currency=None, currency_year=None,
                 extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, is_levelized=None, other_index_1=None, other_index_2=None,
                 parent=None):
        self.check_scenario(scenario)

        self.cost_denominator_unit = cost_denominator_unit
        self.cost_of_capital = cost_of_capital
        self.currency = currency
        self.currency_year = currency_year
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.is_levelized = is_levelized
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.parent = parent

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (parent, currency, currency_year, cost_denominator_unit, cost_of_capital, is_levelized,
         geography, other_index_1, other_index_2, interpolation_method, extrapolation_method,
         extrapolation_growth,) = tup

        self.set_args(scenario, cost_denominator_unit=cost_denominator_unit, cost_of_capital=cost_of_capital,
                  currency=currency, currency_year=currency_year,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method,
                  is_levelized=is_levelized, other_index_1=other_index_1, other_index_2=other_index_2,
                  parent=parent)

class DemandFuelSwitchingMeasuresEnergyIntensity(DataObject):
    _instances_by_key = {}
    _table_name = "DemandFuelSwitchingMeasuresEnergyIntensity"
    _key_col = 'parent'
    _cols = ["extrapolation_growth", "extrapolation_method", "geography", "interpolation_method",
             "other_index_1", "other_index_2", "parent"]
    _df_cols = ["gau", "value", "oth_2", "oth_1", "year"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, parent, scenario):
        DataObject.__init__(self, parent, scenario)

        DemandFuelSwitchingMeasuresEnergyIntensity._instances_by_key[self._key] = self

        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.parent = parent

    def set_args(self, scenario, extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, other_index_1=None, other_index_2=None, parent=None):
        self.check_scenario(scenario)

        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.parent = parent

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (parent, geography, other_index_1, other_index_2, interpolation_method,
         extrapolation_method, extrapolation_growth,) = tup

        self.set_args(scenario, extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method,
                  other_index_1=other_index_1, other_index_2=other_index_2, parent=parent)

class DemandFuelSwitchingMeasuresImpact(DataObject):
    _instances_by_key = {}
    _table_name = "DemandFuelSwitchingMeasuresImpact"
    _key_col = 'parent'
    _cols = ["extrapolation_growth", "extrapolation_method", "geography", "input_type",
             "interpolation_method", "other_index_1", "other_index_2", "parent", "unit"]
    _df_cols = ["gau", "value", "oth_2", "oth_1", "year"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, parent, scenario):
        DataObject.__init__(self, parent, scenario)

        DemandFuelSwitchingMeasuresImpact._instances_by_key[self._key] = self

        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.input_type = None
        self.interpolation_method = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.parent = parent
        self.unit = None

    def set_args(self, scenario, extrapolation_growth=None, extrapolation_method=None, geography=None, input_type=None,
                 interpolation_method=None, other_index_1=None, other_index_2=None, parent=None, unit=None):
        self.check_scenario(scenario)

        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.parent = parent
        self.unit = unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (parent, input_type, unit, geography, other_index_1, other_index_2, interpolation_method,
         extrapolation_method, extrapolation_growth,) = tup

        self.set_args(scenario, extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, input_type=input_type, interpolation_method=interpolation_method,
                  other_index_1=other_index_1, other_index_2=other_index_2, parent=parent, unit=unit)

class DemandSales(DataObject):
    _instances_by_key = {}
    _table_name = "DemandSales"
    _key_col = 'demand_technology'
    _cols = ["demand_technology", "extrapolation_growth", "extrapolation_method", "geography",
             "input_type", "interpolation_method", "other_index_1", "other_index_2", "subsector"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandSales._instances_by_key[self._key] = self

        self.demand_technology = demand_technology
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.input_type = None
        self.interpolation_method = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.subsector = None

    def set_args(self, scenario, demand_technology=None, extrapolation_growth=None, extrapolation_method=None,
                 geography=None, input_type=None, interpolation_method=None, other_index_1=None,
                 other_index_2=None, subsector=None):
        self.check_scenario(scenario)

        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.subsector = subsector

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (subsector, geography, other_index_1, other_index_2, input_type, interpolation_method,
         extrapolation_method, extrapolation_growth, demand_technology,) = tup

        self.set_args(scenario, demand_technology=demand_technology, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography, input_type=input_type,
                  interpolation_method=interpolation_method, other_index_1=other_index_1,
                  other_index_2=other_index_2, subsector=subsector)

class DemandSalesShareMeasures(DataObject):
    _instances_by_key = {}
    _table_name = "DemandSalesShareMeasures"
    _key_col = 'name'
    _cols = ["demand_technology", "extrapolation_growth", "extrapolation_method", "geography",
             "input_type", "interpolation_method", "name", "other_index_1", "replaced_demand_tech",
             "subsector"]
    _df_cols = ["vintage", "gau", "oth_1", "value"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandSalesShareMeasures._instances_by_key[self._key] = self

        self.demand_technology = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.input_type = None
        self.interpolation_method = None
        self.name = name
        self.other_index_1 = None
        self.replaced_demand_tech = None
        self.subsector = None

    def set_args(self, scenario, demand_technology=None, extrapolation_growth=None, extrapolation_method=None,
                 geography=None, input_type=None, interpolation_method=None, name=None,
                 other_index_1=None, replaced_demand_tech=None, subsector=None):
        self.check_scenario(scenario)

        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.name = name
        self.other_index_1 = other_index_1
        self.replaced_demand_tech = replaced_demand_tech
        self.subsector = subsector

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, subsector, geography, other_index_1, demand_technology, replaced_demand_tech,
         input_type, interpolation_method, extrapolation_method, extrapolation_growth,) = tup

        self.set_args(scenario, demand_technology=demand_technology, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography, input_type=input_type,
                  interpolation_method=interpolation_method, name=name, other_index_1=other_index_1,
                  replaced_demand_tech=replaced_demand_tech, subsector=subsector)

class DemandSectors(DataObject):
    _instances_by_key = {}
    _table_name = "DemandSectors"
    _key_col = 'name'
    _cols = ["max_lag_hours", "max_lead_hours", "name", "shape"]
    _df_cols = []
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandSectors._instances_by_key[self._key] = self

        self.max_lag_hours = None
        self.max_lead_hours = None
        self.name = name
        self.shape = None

    def set_args(self, scenario, max_lag_hours=None, max_lead_hours=None, name=None, shape=None):
        self.check_scenario(scenario)

        self.max_lag_hours = max_lag_hours
        self.max_lead_hours = max_lead_hours
        self.name = name
        self.shape = shape

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, shape, max_lead_hours, max_lag_hours,) = tup

        self.set_args(scenario, max_lag_hours=max_lag_hours, max_lead_hours=max_lead_hours, name=name, shape=shape)

class DemandServiceDemandMeasures(DataObject):
    _instances_by_key = {}
    _table_name = "DemandServiceDemandMeasures"
    _key_col = 'name'
    _cols = ["extrapolation_growth", "extrapolation_method", "geography", "geography_map_key",
             "input_type", "interpolation_method", "lifetime_variance", "max_lifetime",
             "mean_lifetime", "min_lifetime", "name", "other_index_1", "other_index_2",
             "stock_decay_function", "subsector", "unit"]
    _df_cols = ["gau", "value", "oth_2", "oth_1", "year"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandServiceDemandMeasures._instances_by_key[self._key] = self

        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.geography_map_key = None
        self.input_type = None
        self.interpolation_method = None
        self.lifetime_variance = None
        self.max_lifetime = None
        self.mean_lifetime = None
        self.min_lifetime = None
        self.name = name
        self.other_index_1 = None
        self.other_index_2 = None
        self.stock_decay_function = None
        self.subsector = None
        self.unit = None

    def set_args(self, scenario, extrapolation_growth=None, extrapolation_method=None, geography=None,
                 geography_map_key=None, input_type=None, interpolation_method=None,
                 lifetime_variance=None, max_lifetime=None, mean_lifetime=None, min_lifetime=None,
                 name=None, other_index_1=None, other_index_2=None, stock_decay_function=None,
                 subsector=None, unit=None):
        self.check_scenario(scenario)

        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.lifetime_variance = lifetime_variance
        self.max_lifetime = max_lifetime
        self.mean_lifetime = mean_lifetime
        self.min_lifetime = min_lifetime
        self.name = name
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.stock_decay_function = stock_decay_function
        self.subsector = subsector
        self.unit = unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, subsector, input_type, unit, geography, other_index_1, other_index_2,
         interpolation_method, extrapolation_method, extrapolation_growth, stock_decay_function,
         min_lifetime, max_lifetime, mean_lifetime, lifetime_variance, geography_map_key,) = tup

        self.set_args(scenario, extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, geography_map_key=geography_map_key, input_type=input_type,
                  interpolation_method=interpolation_method, lifetime_variance=lifetime_variance,
                  max_lifetime=max_lifetime, mean_lifetime=mean_lifetime, min_lifetime=min_lifetime,
                  name=name, other_index_1=other_index_1, other_index_2=other_index_2,
                  stock_decay_function=stock_decay_function, subsector=subsector, unit=unit)

class DemandServiceDemandMeasuresCost(DataObject):
    _instances_by_key = {}
    _table_name = "DemandServiceDemandMeasuresCost"
    _key_col = 'parent'
    _cols = ["cost_denominator_unit", "cost_of_capital", "currency", "currency_year",
             "extrapolation_growth", "extrapolation_method", "geography", "interpolation_method",
             "is_levelized", "other_index_1", "other_index_2", "parent"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, parent, scenario):
        DataObject.__init__(self, parent, scenario)

        DemandServiceDemandMeasuresCost._instances_by_key[self._key] = self

        self.cost_denominator_unit = None
        self.cost_of_capital = None
        self.currency = None
        self.currency_year = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.is_levelized = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.parent = parent

    def set_args(self, scenario, cost_denominator_unit=None, cost_of_capital=None, currency=None, currency_year=None,
                 extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, is_levelized=None, other_index_1=None, other_index_2=None,
                 parent=None):
        self.check_scenario(scenario)

        self.cost_denominator_unit = cost_denominator_unit
        self.cost_of_capital = cost_of_capital
        self.currency = currency
        self.currency_year = currency_year
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.is_levelized = is_levelized
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.parent = parent

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (parent, currency, currency_year, cost_denominator_unit, cost_of_capital, is_levelized,
         geography, other_index_1, other_index_2, interpolation_method, extrapolation_method,
         extrapolation_growth,) = tup

        self.set_args(scenario, cost_denominator_unit=cost_denominator_unit, cost_of_capital=cost_of_capital,
                  currency=currency, currency_year=currency_year,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method,
                  is_levelized=is_levelized, other_index_1=other_index_1, other_index_2=other_index_2,
                  parent=parent)

class DemandServiceDemands(DataObject):
    _instances_by_key = {}
    _table_name = "DemandServiceDemands"
    _key_col = 'subsector'
    _cols = ["demand_technology_index", "driver_1", "driver_2", "driver_3", "driver_denominator_1",
             "driver_denominator_2", "extrapolation_growth", "extrapolation_method",
             "final_energy_index", "geography", "geography_map_key", "input_type",
             "interpolation_method", "is_stock_dependent", "other_index_1", "other_index_2",
             "subsector", "unit"]
    _df_cols = ["gau", "demand_technology", "value", "oth_2", "oth_1", "year", "final_energy",
             "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, subsector, scenario):
        DataObject.__init__(self, subsector, scenario)

        DemandServiceDemands._instances_by_key[self._key] = self

        self.demand_technology_index = None
        self.driver_1 = None
        self.driver_2 = None
        self.driver_3 = None
        self.driver_denominator_1 = None
        self.driver_denominator_2 = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.final_energy_index = None
        self.geography = None
        self.geography_map_key = None
        self.input_type = None
        self.interpolation_method = None
        self.is_stock_dependent = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.subsector = subsector
        self.unit = None

    def set_args(self, scenario, demand_technology_index=None, driver_1=None, driver_2=None, driver_3=None,
                 driver_denominator_1=None, driver_denominator_2=None, extrapolation_growth=None,
                 extrapolation_method=None, final_energy_index=None, geography=None,
                 geography_map_key=None, input_type=None, interpolation_method=None,
                 is_stock_dependent=None, other_index_1=None, other_index_2=None, subsector=None,
                 unit=None):
        self.check_scenario(scenario)

        self.demand_technology_index = demand_technology_index
        self.driver_1 = driver_1
        self.driver_2 = driver_2
        self.driver_3 = driver_3
        self.driver_denominator_1 = driver_denominator_1
        self.driver_denominator_2 = driver_denominator_2
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.final_energy_index = final_energy_index
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.is_stock_dependent = is_stock_dependent
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.subsector = subsector
        self.unit = unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (subsector, is_stock_dependent, input_type, unit, driver_denominator_1,
         driver_denominator_2, driver_1, driver_2, driver_3, geography, final_energy_index,
         demand_technology_index, other_index_1, other_index_2, interpolation_method,
         extrapolation_method, extrapolation_growth, geography_map_key,) = tup

        self.set_args(scenario, demand_technology_index=demand_technology_index, driver_1=driver_1, driver_2=driver_2,
                  driver_3=driver_3, driver_denominator_1=driver_denominator_1,
                  driver_denominator_2=driver_denominator_2, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, final_energy_index=final_energy_index,
                  geography=geography, geography_map_key=geography_map_key, input_type=input_type,
                  interpolation_method=interpolation_method, is_stock_dependent=is_stock_dependent,
                  other_index_1=other_index_1, other_index_2=other_index_2, subsector=subsector, unit=unit)

class DemandServiceEfficiency(DataObject):
    _instances_by_key = {}
    _table_name = "DemandServiceEfficiency"
    _key_col = 'subsector'
    _cols = ["denominator_unit", "energy_unit", "extrapolation_growth", "extrapolation_method",
             "geography", "geography_map_key", "interpolation_method", "other_index_1",
             "other_index_2", "sensitivity", "subsector"]
    _df_cols = ["gau", "value", "oth_2", "oth_1", "year", "final_energy"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, subsector, scenario):
        DataObject.__init__(self, subsector, scenario)

        DemandServiceEfficiency._instances_by_key[self._key] = self

        self.denominator_unit = None
        self.energy_unit = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.geography_map_key = None
        self.interpolation_method = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.sensitivity = None
        self.subsector = subsector

    def set_args(self, scenario, denominator_unit=None, energy_unit=None, extrapolation_growth=None,
                 extrapolation_method=None, geography=None, geography_map_key=None,
                 interpolation_method=None, other_index_1=None, other_index_2=None, sensitivity=None,
                 subsector=None):
        self.check_scenario(scenario)

        self.denominator_unit = denominator_unit
        self.energy_unit = energy_unit
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.interpolation_method = interpolation_method
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.sensitivity = sensitivity
        self.subsector = subsector

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (subsector, energy_unit, denominator_unit, geography, other_index_1, other_index_2,
         interpolation_method, extrapolation_method, extrapolation_growth, geography_map_key,
         sensitivity,) = tup

        self.set_args(scenario, denominator_unit=denominator_unit, energy_unit=energy_unit,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, geography_map_key=geography_map_key,
                  interpolation_method=interpolation_method, other_index_1=other_index_1,
                  other_index_2=other_index_2, sensitivity=sensitivity, subsector=subsector)

class DemandServiceLink(DataObject):
    _instances_by_key = {}
    _table_name = "DemandServiceLink"
    _key_col = 'name'
    _cols = ["linked_subsector", "name", "service_demand_share", "subsector", "year"]
    _df_cols = []
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandServiceLink._instances_by_key[self._key] = self

        self.linked_subsector = None
        self.name = name
        self.service_demand_share = None
        self.subsector = None
        self.year = None

    def set_args(self, scenario, linked_subsector=None, name=None, service_demand_share=None, subsector=None, year=None):
        self.check_scenario(scenario)

        self.linked_subsector = linked_subsector
        self.name = name
        self.service_demand_share = service_demand_share
        self.subsector = subsector
        self.year = year

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, subsector, linked_subsector, service_demand_share, year,) = tup

        self.set_args(scenario, linked_subsector=linked_subsector, name=name, service_demand_share=service_demand_share,
                  subsector=subsector, year=year)

class DemandStock(DataObject):
    _instances_by_key = {}
    _table_name = "DemandStock"
    _key_col = 'subsector'
    _cols = ["demand_stock_unit_type", "driver_1", "driver_2", "driver_3", "driver_denominator_1",
             "driver_denominator_2", "extrapolation_growth", "extrapolation_method", "geography",
             "geography_map_key", "input_type", "interpolation_method", "is_service_demand_dependent",
             "other_index_1", "other_index_2", "specify_stocks_past_current_year", "subsector",
             "time_unit", "unit"]
    _df_cols = ["gau", "demand_technology", "value", "oth_2", "oth_1", "year", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, subsector, scenario):
        DataObject.__init__(self, subsector, scenario)

        DemandStock._instances_by_key[self._key] = self

        self.demand_stock_unit_type = None
        self.driver_1 = None
        self.driver_2 = None
        self.driver_3 = None
        self.driver_denominator_1 = None
        self.driver_denominator_2 = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.geography_map_key = None
        self.input_type = None
        self.interpolation_method = None
        self.is_service_demand_dependent = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.specify_stocks_past_current_year = None
        self.subsector = subsector
        self.time_unit = None
        self.unit = None

    def set_args(self, scenario, demand_stock_unit_type=None, driver_1=None, driver_2=None, driver_3=None,
                 driver_denominator_1=None, driver_denominator_2=None, extrapolation_growth=None,
                 extrapolation_method=None, geography=None, geography_map_key=None, input_type=None,
                 interpolation_method=None, is_service_demand_dependent=None, other_index_1=None,
                 other_index_2=None, specify_stocks_past_current_year=None, subsector=None,
                 time_unit=None, unit=None):
        self.check_scenario(scenario)

        self.demand_stock_unit_type = demand_stock_unit_type
        self.driver_1 = driver_1
        self.driver_2 = driver_2
        self.driver_3 = driver_3
        self.driver_denominator_1 = driver_denominator_1
        self.driver_denominator_2 = driver_denominator_2
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.is_service_demand_dependent = is_service_demand_dependent
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.specify_stocks_past_current_year = specify_stocks_past_current_year
        self.subsector = subsector
        self.time_unit = time_unit
        self.unit = unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (subsector, is_service_demand_dependent, driver_denominator_1, driver_denominator_2,
         driver_1, driver_2, driver_3, geography, other_index_1, other_index_2, geography_map_key,
         input_type, demand_stock_unit_type, unit, time_unit, interpolation_method,
         extrapolation_method, extrapolation_growth, specify_stocks_past_current_year,) = tup

        self.set_args(scenario, demand_stock_unit_type=demand_stock_unit_type, driver_1=driver_1, driver_2=driver_2,
                  driver_3=driver_3, driver_denominator_1=driver_denominator_1,
                  driver_denominator_2=driver_denominator_2, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography,
                  geography_map_key=geography_map_key, input_type=input_type,
                  interpolation_method=interpolation_method,
                  is_service_demand_dependent=is_service_demand_dependent, other_index_1=other_index_1,
                  other_index_2=other_index_2,
                  specify_stocks_past_current_year=specify_stocks_past_current_year, subsector=subsector,
                  time_unit=time_unit, unit=unit)

class DemandStockMeasures(DataObject):
    _instances_by_key = {}
    _table_name = "DemandStockMeasures"
    _key_col = 'name'
    _cols = ["demand_technology", "extrapolation_growth", "extrapolation_method", "geography",
             "interpolation_method", "name", "other_index_1", "subsector"]
    _df_cols = ["gau", "oth_1", "value", "year"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandStockMeasures._instances_by_key[self._key] = self

        self.demand_technology = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.name = name
        self.other_index_1 = None
        self.subsector = None

    def set_args(self, scenario, demand_technology=None, extrapolation_growth=None, extrapolation_method=None,
                 geography=None, interpolation_method=None, name=None, other_index_1=None, subsector=None):
        self.check_scenario(scenario)

        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.name = name
        self.other_index_1 = other_index_1
        self.subsector = subsector

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, subsector, geography, other_index_1, demand_technology, interpolation_method,
         extrapolation_method, extrapolation_growth,) = tup

        self.set_args(scenario, demand_technology=demand_technology, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography,
                  interpolation_method=interpolation_method, name=name, other_index_1=other_index_1,
                  subsector=subsector)

class DemandSubsectors(DataObject):
    _instances_by_key = {}
    _table_name = "DemandSubsectors"
    _key_col = 'name'
    _cols = ["cost_of_capital", "name", "override_service_demand_unit", "sector", "shape", "sub_type"]
    _df_cols = []
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandSubsectors._instances_by_key[self._key] = self

        self.cost_of_capital = None
        self.name = name
        self.override_service_demand_unit = None
        self.sector = None
        self.shape = None
        self.sub_type = None

    def set_args(self, scenario, cost_of_capital=None, name=None, override_service_demand_unit=None, sector=None,
                 shape=None, sub_type=None):
        self.check_scenario(scenario)

        self.cost_of_capital = cost_of_capital
        self.name = name
        self.override_service_demand_unit = override_service_demand_unit
        self.sector = sector
        self.shape = shape
        self.sub_type = sub_type

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, sector, cost_of_capital, sub_type, shape, override_service_demand_unit,) = tup

        self.set_args(scenario, cost_of_capital=cost_of_capital, name=name,
                  override_service_demand_unit=override_service_demand_unit, sector=sector, shape=shape,
                  sub_type=sub_type)

class DemandTechs(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechs"
    _key_col = 'name'
    _cols = ["additional_description", "cost_of_capital", "demand_tech_unit_type", "lifetime_variance",
             "linked", "max_lifetime", "mean_lifetime", "min_lifetime", "name", "shape", "source",
             "stock_decay_function", "stock_link_ratio", "subsector", "time_unit", "unit"]
    _df_cols = []
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandTechs._instances_by_key[self._key] = self

        self.additional_description = None
        self.cost_of_capital = None
        self.demand_tech_unit_type = None
        self.lifetime_variance = None
        self.linked = None
        self.max_lifetime = None
        self.mean_lifetime = None
        self.min_lifetime = None
        self.name = name
        self.shape = None
        self.source = None
        self.stock_decay_function = None
        self.stock_link_ratio = None
        self.subsector = None
        self.time_unit = None
        self.unit = None

    def set_args(self, scenario, additional_description=None, cost_of_capital=None, demand_tech_unit_type=None,
                 lifetime_variance=None, linked=None, max_lifetime=None, mean_lifetime=None,
                 min_lifetime=None, name=None, shape=None, source=None, stock_decay_function=None,
                 stock_link_ratio=None, subsector=None, time_unit=None, unit=None):
        self.check_scenario(scenario)

        self.additional_description = additional_description
        self.cost_of_capital = cost_of_capital
        self.demand_tech_unit_type = demand_tech_unit_type
        self.lifetime_variance = lifetime_variance
        self.linked = linked
        self.max_lifetime = max_lifetime
        self.mean_lifetime = mean_lifetime
        self.min_lifetime = min_lifetime
        self.name = name
        self.shape = shape
        self.source = source
        self.stock_decay_function = stock_decay_function
        self.stock_link_ratio = stock_link_ratio
        self.subsector = subsector
        self.time_unit = time_unit
        self.unit = unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, linked, stock_link_ratio, subsector, source, additional_description,
         demand_tech_unit_type, unit, time_unit, cost_of_capital, stock_decay_function,
         min_lifetime, max_lifetime, mean_lifetime, lifetime_variance, shape,) = tup

        self.set_args(scenario, additional_description=additional_description, cost_of_capital=cost_of_capital,
                  demand_tech_unit_type=demand_tech_unit_type, lifetime_variance=lifetime_variance,
                  linked=linked, max_lifetime=max_lifetime, mean_lifetime=mean_lifetime,
                  min_lifetime=min_lifetime, name=name, shape=shape, source=source,
                  stock_decay_function=stock_decay_function, stock_link_ratio=stock_link_ratio,
                  subsector=subsector, time_unit=time_unit, unit=unit)

class DemandTechsAirPollution(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsAirPollution"
    _key_col = 'demand_technology'
    _cols = ["definition", "demand_technology", "energy_unit", "extrapolation_growth",
             "extrapolation_method", "geography", "interpolation_method", "mass_unit",
             "other_index_1", "other_index_2", "reference_tech"]
    _df_cols = ["vintage", "year", "gau", "final_energy", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsAirPollution._instances_by_key[self._key] = self

        self.definition = None
        self.demand_technology = demand_technology
        self.energy_unit = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.mass_unit = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None

    def set_args(self, scenario, definition=None, demand_technology=None, energy_unit=None, extrapolation_growth=None,
                 extrapolation_method=None, geography=None, interpolation_method=None, mass_unit=None,
                 other_index_1=None, other_index_2=None, reference_tech=None):
        self.check_scenario(scenario)

        self.definition = definition
        self.demand_technology = demand_technology
        self.energy_unit = energy_unit
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.mass_unit = mass_unit
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, mass_unit, energy_unit, geography,
         other_index_1, other_index_2, interpolation_method, extrapolation_method,
         extrapolation_growth,) = tup

        self.set_args(scenario, definition=definition, demand_technology=demand_technology, energy_unit=energy_unit,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method, mass_unit=mass_unit,
                  other_index_1=other_index_1, other_index_2=other_index_2, reference_tech=reference_tech)

class DemandTechsAuxEfficiency(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsAuxEfficiency"
    _key_col = 'demand_technology'
    _cols = ["age_growth_or_decay", "age_growth_or_decay_type", "definition",
             "demand_tech_efficiency_types", "demand_technology", "denominator_unit",
             "extrapolation_growth", "extrapolation_method", "final_energy", "geography",
             "interpolation_method", "is_numerator_service", "numerator_unit", "other_index_1",
             "other_index_2", "reference_tech", "shape"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsAuxEfficiency._instances_by_key[self._key] = self

        self.age_growth_or_decay = None
        self.age_growth_or_decay_type = None
        self.definition = None
        self.demand_tech_efficiency_types = None
        self.demand_technology = demand_technology
        self.denominator_unit = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.final_energy = None
        self.geography = None
        self.interpolation_method = None
        self.is_numerator_service = None
        self.numerator_unit = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None
        self.shape = None

    def set_args(self, scenario, age_growth_or_decay=None, age_growth_or_decay_type=None, definition=None,
                 demand_tech_efficiency_types=None, demand_technology=None, denominator_unit=None,
                 extrapolation_growth=None, extrapolation_method=None, final_energy=None, geography=None,
                 interpolation_method=None, is_numerator_service=None, numerator_unit=None,
                 other_index_1=None, other_index_2=None, reference_tech=None, shape=None):
        self.check_scenario(scenario)

        self.age_growth_or_decay = age_growth_or_decay
        self.age_growth_or_decay_type = age_growth_or_decay_type
        self.definition = definition
        self.demand_tech_efficiency_types = demand_tech_efficiency_types
        self.demand_technology = demand_technology
        self.denominator_unit = denominator_unit
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.final_energy = final_energy
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.is_numerator_service = is_numerator_service
        self.numerator_unit = numerator_unit
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech
        self.shape = shape

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, geography, other_index_1, other_index_2,
         final_energy, demand_tech_efficiency_types, is_numerator_service, numerator_unit,
         denominator_unit, interpolation_method, extrapolation_method, extrapolation_growth,
         age_growth_or_decay_type, age_growth_or_decay, shape,) = tup

        self.set_args(scenario, age_growth_or_decay=age_growth_or_decay,
                  age_growth_or_decay_type=age_growth_or_decay_type, definition=definition,
                  demand_tech_efficiency_types=demand_tech_efficiency_types,
                  demand_technology=demand_technology, denominator_unit=denominator_unit,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  final_energy=final_energy, geography=geography,
                  interpolation_method=interpolation_method, is_numerator_service=is_numerator_service,
                  numerator_unit=numerator_unit, other_index_1=other_index_1, other_index_2=other_index_2,
                  reference_tech=reference_tech, shape=shape)

class DemandTechsCapitalCost(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsCapitalCost"
    _key_col = 'demand_technology'
    _cols = ["currency", "currency_year", "definition", "demand_technology", "extrapolation_growth",
             "extrapolation_method", "geography", "interpolation_method", "is_levelized",
             "new_or_replacement", "other_index_1", "other_index_2", "reference_tech",
             "reference_tech_operation"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = ["new_or_replacement"]
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsCapitalCost._instances_by_key[self._key] = self

        self.currency = None
        self.currency_year = None
        self.definition = None
        self.demand_technology = demand_technology
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.is_levelized = None
        self.new_or_replacement = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None
        self.reference_tech_operation = None

    def set_args(self, scenario, currency=None, currency_year=None, definition=None, demand_technology=None,
                 extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, is_levelized=None, new_or_replacement=None,
                 other_index_1=None, other_index_2=None, reference_tech=None,
                 reference_tech_operation=None):
        self.check_scenario(scenario)

        self.currency = currency
        self.currency_year = currency_year
        self.definition = definition
        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.is_levelized = is_levelized
        self.new_or_replacement = new_or_replacement
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech
        self.reference_tech_operation = reference_tech_operation

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, geography, other_index_1, other_index_2,
         currency, currency_year, is_levelized, interpolation_method, extrapolation_method,
         extrapolation_growth, reference_tech_operation, new_or_replacement,) = tup

        self.set_args(scenario, currency=currency, currency_year=currency_year, definition=definition,
                  demand_technology=demand_technology, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography,
                  interpolation_method=interpolation_method, is_levelized=is_levelized,
                  new_or_replacement=new_or_replacement, other_index_1=other_index_1,
                  other_index_2=other_index_2, reference_tech=reference_tech,
                  reference_tech_operation=reference_tech_operation)

class DemandTechsFixedMaintenanceCost(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsFixedMaintenanceCost"
    _key_col = 'demand_technology'
    _cols = ["additional_description", "age_growth_or_decay", "age_growth_or_decay_type", "currency",
             "currency_year", "definition", "demand_technology", "extrapolation_growth",
             "extrapolation_method", "geography", "interpolation_method", "other_index_1",
             "other_index_2", "reference_tech"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsFixedMaintenanceCost._instances_by_key[self._key] = self

        self.additional_description = None
        self.age_growth_or_decay = None
        self.age_growth_or_decay_type = None
        self.currency = None
        self.currency_year = None
        self.definition = None
        self.demand_technology = demand_technology
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None

    def set_args(self, scenario, additional_description=None, age_growth_or_decay=None, age_growth_or_decay_type=None,
                 currency=None, currency_year=None, definition=None, demand_technology=None,
                 extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, other_index_1=None, other_index_2=None, reference_tech=None):
        self.check_scenario(scenario)

        self.additional_description = additional_description
        self.age_growth_or_decay = age_growth_or_decay
        self.age_growth_or_decay_type = age_growth_or_decay_type
        self.currency = currency
        self.currency_year = currency_year
        self.definition = definition
        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, geography, other_index_1, other_index_2,
         currency, currency_year, interpolation_method, extrapolation_method,
         extrapolation_growth, age_growth_or_decay_type, age_growth_or_decay,
         additional_description,) = tup

        self.set_args(scenario, additional_description=additional_description, age_growth_or_decay=age_growth_or_decay,
                  age_growth_or_decay_type=age_growth_or_decay_type, currency=currency,
                  currency_year=currency_year, definition=definition, demand_technology=demand_technology,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method,
                  other_index_1=other_index_1, other_index_2=other_index_2, reference_tech=reference_tech)

class DemandTechsFuelSwitchCost(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsFuelSwitchCost"
    _key_col = 'demand_technology'
    _cols = ["currency", "currency_year", "definition", "demand_technology", "extrapolation_growth",
             "extrapolation_method", "geography", "interpolation_method", "is_levelized",
             "other_index_1", "other_index_2", "reference_tech"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsFuelSwitchCost._instances_by_key[self._key] = self

        self.currency = None
        self.currency_year = None
        self.definition = None
        self.demand_technology = demand_technology
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.is_levelized = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None

    def set_args(self, scenario, currency=None, currency_year=None, definition=None, demand_technology=None,
                 extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, is_levelized=None, other_index_1=None, other_index_2=None,
                 reference_tech=None):
        self.check_scenario(scenario)

        self.currency = currency
        self.currency_year = currency_year
        self.definition = definition
        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.is_levelized = is_levelized
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, geography, other_index_1, other_index_2,
         currency, currency_year, is_levelized, interpolation_method, extrapolation_method,
         extrapolation_growth,) = tup

        self.set_args(scenario, currency=currency, currency_year=currency_year, definition=definition,
                  demand_technology=demand_technology, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography,
                  interpolation_method=interpolation_method, is_levelized=is_levelized,
                  other_index_1=other_index_1, other_index_2=other_index_2, reference_tech=reference_tech)

class DemandTechsIncentive(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsIncentive"
    _key_col = 'demand_technology'
    _cols = ["apply_lesser_of_incentives", "currency", "currency_year", "demand_technology",
             "extrapolation_growth", "extrapolation_method", "geography", "incentive_type",
             "include_capital_cost", "include_fuel_switching_cost", "include_installation_cost",
             "interpolation_method", "is_levelized", "other_index_1", "other_index_2"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = ["incentive_type"]
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsIncentive._instances_by_key[self._key] = self

        self.apply_lesser_of_incentives = None
        self.currency = None
        self.currency_year = None
        self.demand_technology = demand_technology
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.incentive_type = None
        self.include_capital_cost = None
        self.include_fuel_switching_cost = None
        self.include_installation_cost = None
        self.interpolation_method = None
        self.is_levelized = None
        self.other_index_1 = None
        self.other_index_2 = None

    def set_args(self, scenario, apply_lesser_of_incentives=None, currency=None, currency_year=None,
                 demand_technology=None, extrapolation_growth=None, extrapolation_method=None,
                 geography=None, incentive_type=None, include_capital_cost=None,
                 include_fuel_switching_cost=None, include_installation_cost=None,
                 interpolation_method=None, is_levelized=None, other_index_1=None, other_index_2=None):
        self.check_scenario(scenario)

        self.apply_lesser_of_incentives = apply_lesser_of_incentives
        self.currency = currency
        self.currency_year = currency_year
        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.incentive_type = incentive_type
        self.include_capital_cost = include_capital_cost
        self.include_fuel_switching_cost = include_fuel_switching_cost
        self.include_installation_cost = include_installation_cost
        self.interpolation_method = interpolation_method
        self.is_levelized = is_levelized
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, incentive_type, apply_lesser_of_incentives, include_capital_cost,
         include_installation_cost, include_fuel_switching_cost, geography, other_index_1,
         other_index_2, currency, currency_year, is_levelized, interpolation_method,
         extrapolation_method, extrapolation_growth,) = tup

        self.set_args(scenario, apply_lesser_of_incentives=apply_lesser_of_incentives, currency=currency,
                  currency_year=currency_year, demand_technology=demand_technology,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, incentive_type=incentive_type,
                  include_capital_cost=include_capital_cost,
                  include_fuel_switching_cost=include_fuel_switching_cost,
                  include_installation_cost=include_installation_cost,
                  interpolation_method=interpolation_method, is_levelized=is_levelized,
                  other_index_1=other_index_1, other_index_2=other_index_2)

class DemandTechsInstallationCost(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsInstallationCost"
    _key_col = 'demand_technology'
    _cols = ["currency", "currency_year", "definition", "demand_technology", "extrapolation_growth",
             "extrapolation_method", "geography", "interpolation_method", "is_levelized",
             "new_or_replacement", "other_index_1", "other_index_2", "reference_tech"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = ["new_or_replacement"]
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsInstallationCost._instances_by_key[self._key] = self

        self.currency = None
        self.currency_year = None
        self.definition = None
        self.demand_technology = demand_technology
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.is_levelized = None
        self.new_or_replacement = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None

    def set_args(self, scenario, currency=None, currency_year=None, definition=None, demand_technology=None,
                 extrapolation_growth=None, extrapolation_method=None, geography=None,
                 interpolation_method=None, is_levelized=None, new_or_replacement=None,
                 other_index_1=None, other_index_2=None, reference_tech=None):
        self.check_scenario(scenario)

        self.currency = currency
        self.currency_year = currency_year
        self.definition = definition
        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.is_levelized = is_levelized
        self.new_or_replacement = new_or_replacement
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, geography, other_index_1, other_index_2,
         currency, currency_year, is_levelized, interpolation_method, extrapolation_method,
         extrapolation_growth, new_or_replacement,) = tup

        self.set_args(scenario, currency=currency, currency_year=currency_year, definition=definition,
                  demand_technology=demand_technology, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography,
                  interpolation_method=interpolation_method, is_levelized=is_levelized,
                  new_or_replacement=new_or_replacement, other_index_1=other_index_1,
                  other_index_2=other_index_2, reference_tech=reference_tech)

class DemandTechsMainEfficiency(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsMainEfficiency"
    _key_col = 'demand_technology'
    _cols = ["age_growth_or_decay", "age_growth_or_decay_type", "definition", "demand_technology",
             "denominator_unit", "extrapolation_growth", "extrapolation_method", "final_energy",
             "geography", "geography_map_key", "interpolation_method", "is_numerator_service",
             "numerator_unit", "other_index_1", "other_index_2", "reference_tech", "utility_factor"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsMainEfficiency._instances_by_key[self._key] = self

        self.age_growth_or_decay = None
        self.age_growth_or_decay_type = None
        self.definition = None
        self.demand_technology = demand_technology
        self.denominator_unit = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.final_energy = None
        self.geography = None
        self.geography_map_key = None
        self.interpolation_method = None
        self.is_numerator_service = None
        self.numerator_unit = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None
        self.utility_factor = None

    def set_args(self, scenario, age_growth_or_decay=None, age_growth_or_decay_type=None, definition=None,
                 demand_technology=None, denominator_unit=None, extrapolation_growth=None,
                 extrapolation_method=None, final_energy=None, geography=None, geography_map_key=None,
                 interpolation_method=None, is_numerator_service=None, numerator_unit=None,
                 other_index_1=None, other_index_2=None, reference_tech=None, utility_factor=None):
        self.check_scenario(scenario)

        self.age_growth_or_decay = age_growth_or_decay
        self.age_growth_or_decay_type = age_growth_or_decay_type
        self.definition = definition
        self.demand_technology = demand_technology
        self.denominator_unit = denominator_unit
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.final_energy = final_energy
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.interpolation_method = interpolation_method
        self.is_numerator_service = is_numerator_service
        self.numerator_unit = numerator_unit
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech
        self.utility_factor = utility_factor

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, geography, other_index_1, other_index_2,
         final_energy, utility_factor, is_numerator_service, numerator_unit, denominator_unit,
         interpolation_method, extrapolation_method, extrapolation_growth,
         age_growth_or_decay_type, age_growth_or_decay, geography_map_key,) = tup

        self.set_args(scenario, age_growth_or_decay=age_growth_or_decay,
                  age_growth_or_decay_type=age_growth_or_decay_type, definition=definition,
                  demand_technology=demand_technology, denominator_unit=denominator_unit,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  final_energy=final_energy, geography=geography, geography_map_key=geography_map_key,
                  interpolation_method=interpolation_method, is_numerator_service=is_numerator_service,
                  numerator_unit=numerator_unit, other_index_1=other_index_1, other_index_2=other_index_2,
                  reference_tech=reference_tech, utility_factor=utility_factor)

class DemandTechsParasiticEnergy(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsParasiticEnergy"
    _key_col = 'demand_technology'
    _cols = ["age_growth_or_decay", "age_growth_or_decay_type", "definition", "demand_technology",
             "energy_unit", "extrapolation_growth", "extrapolation_method", "geography",
             "interpolation_method", "other_index_1", "other_index_2", "reference_tech", "time_unit"]
    _df_cols = ["vintage", "gau", "value", "oth_2", "oth_1", "final_energy", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsParasiticEnergy._instances_by_key[self._key] = self

        self.age_growth_or_decay = None
        self.age_growth_or_decay_type = None
        self.definition = None
        self.demand_technology = demand_technology
        self.energy_unit = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None
        self.time_unit = None

    def set_args(self, scenario, age_growth_or_decay=None, age_growth_or_decay_type=None, definition=None,
                 demand_technology=None, energy_unit=None, extrapolation_growth=None,
                 extrapolation_method=None, geography=None, interpolation_method=None, other_index_1=None,
                 other_index_2=None, reference_tech=None, time_unit=None):
        self.check_scenario(scenario)

        self.age_growth_or_decay = age_growth_or_decay
        self.age_growth_or_decay_type = age_growth_or_decay_type
        self.definition = definition
        self.demand_technology = demand_technology
        self.energy_unit = energy_unit
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech
        self.time_unit = time_unit

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, definition, reference_tech, geography, other_index_1, other_index_2,
         energy_unit, time_unit, interpolation_method, extrapolation_method, extrapolation_growth,
         age_growth_or_decay_type, age_growth_or_decay,) = tup

        self.set_args(scenario, age_growth_or_decay=age_growth_or_decay,
                  age_growth_or_decay_type=age_growth_or_decay_type, definition=definition,
                  demand_technology=demand_technology, energy_unit=energy_unit,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method,
                  other_index_1=other_index_1, other_index_2=other_index_2, reference_tech=reference_tech,
                  time_unit=time_unit)

class DemandTechsServiceDemandModifier(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsServiceDemandModifier"
    _key_col = 'demand_technology'
    _cols = ["definition", "demand_technology", "extrapolation_growth", "extrapolation_method",
             "geography", "interpolation_method", "other_index_1", "other_index_2", "reference_tech"]
    _df_cols = ["vintage", "year", "gau", "value", "oth_2", "oth_1", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, demand_technology, scenario):
        DataObject.__init__(self, demand_technology, scenario)

        DemandTechsServiceDemandModifier._instances_by_key[self._key] = self

        self.definition = None
        self.demand_technology = demand_technology
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference_tech = None

    def set_args(self, scenario, definition=None, demand_technology=None, extrapolation_growth=None,
                 extrapolation_method=None, geography=None, interpolation_method=None, other_index_1=None,
                 other_index_2=None, reference_tech=None):
        self.check_scenario(scenario)

        self.definition = definition
        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference_tech = reference_tech

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (demand_technology, geography, definition, reference_tech, other_index_1, other_index_2,
         interpolation_method, extrapolation_method, extrapolation_growth,) = tup

        self.set_args(scenario, definition=definition, demand_technology=demand_technology,
                  extrapolation_growth=extrapolation_growth, extrapolation_method=extrapolation_method,
                  geography=geography, interpolation_method=interpolation_method,
                  other_index_1=other_index_1, other_index_2=other_index_2, reference_tech=reference_tech)

class DemandTechsServiceLink(DataObject):
    _instances_by_key = {}
    _table_name = "DemandTechsServiceLink"
    _key_col = 'name'
    _cols = ["age_growth_or_decay", "age_growth_or_decay_type", "definition", "demand_technology",
             "extrapolation_growth", "extrapolation_method", "geography", "interpolation_method",
             "name", "other_index_1", "other_index_2", "reference", "sensitivity", "service_link"]
    _df_cols = ["vintage", "gau", "oth_1", "oth_2", "value"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, name, scenario):
        DataObject.__init__(self, name, scenario)

        DemandTechsServiceLink._instances_by_key[self._key] = self

        self.age_growth_or_decay = None
        self.age_growth_or_decay_type = None
        self.definition = None
        self.demand_technology = None
        self.extrapolation_growth = None
        self.extrapolation_method = None
        self.geography = None
        self.interpolation_method = None
        self.name = name
        self.other_index_1 = None
        self.other_index_2 = None
        self.reference = None
        self.sensitivity = None
        self.service_link = None

    def set_args(self, scenario, age_growth_or_decay=None, age_growth_or_decay_type=None, definition=None,
                 demand_technology=None, extrapolation_growth=None, extrapolation_method=None,
                 geography=None, interpolation_method=None, name=None, other_index_1=None,
                 other_index_2=None, reference=None, sensitivity=None, service_link=None):
        self.check_scenario(scenario)

        self.age_growth_or_decay = age_growth_or_decay
        self.age_growth_or_decay_type = age_growth_or_decay_type
        self.definition = definition
        self.demand_technology = demand_technology
        self.extrapolation_growth = extrapolation_growth
        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.interpolation_method = interpolation_method
        self.name = name
        self.other_index_1 = other_index_1
        self.other_index_2 = other_index_2
        self.reference = reference
        self.sensitivity = sensitivity
        self.service_link = service_link

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (name, service_link, demand_technology, definition, reference, geography, other_index_1,
         other_index_2, interpolation_method, extrapolation_method, extrapolation_growth,
         age_growth_or_decay_type, age_growth_or_decay, sensitivity,) = tup

        self.set_args(scenario, age_growth_or_decay=age_growth_or_decay,
                  age_growth_or_decay_type=age_growth_or_decay_type, definition=definition,
                  demand_technology=demand_technology, extrapolation_growth=extrapolation_growth,
                  extrapolation_method=extrapolation_method, geography=geography,
                  interpolation_method=interpolation_method, name=name, other_index_1=other_index_1,
                  other_index_2=other_index_2, reference=reference, sensitivity=sensitivity,
                  service_link=service_link)

class DispatchFeedersAllocation(DataObject):
    _instances_by_key = {}
    _table_name = "DispatchFeedersAllocation"
    _key_col = 'subsector'
    _cols = ["extrapolation_method", "geography", "geography_map_key", "input_type",
             "interpolation_method", "subsector"]
    _df_cols = ["gau", "year", "value", "dispatch_feeder", "sensitivity"]
    _df_filters = []
    _data_table_name = None

    def __init__(self, subsector, scenario):
        DataObject.__init__(self, subsector, scenario)

        DispatchFeedersAllocation._instances_by_key[self._key] = self

        self.extrapolation_method = None
        self.geography = None
        self.geography_map_key = None
        self.input_type = None
        self.interpolation_method = None
        self.subsector = subsector

    def set_args(self, scenario, extrapolation_method=None, geography=None, geography_map_key=None, input_type=None,
                 interpolation_method=None, subsector=None):
        self.check_scenario(scenario)

        self.extrapolation_method = extrapolation_method
        self.geography = geography
        self.geography_map_key = geography_map_key
        self.input_type = input_type
        self.interpolation_method = interpolation_method
        self.subsector = subsector

    def init_from_tuple(self, tup, scenario, **kwargs):    
        (subsector, geography, geography_map_key, input_type, interpolation_method,
         extrapolation_method,) = tup

        self.set_args(scenario, extrapolation_method=extrapolation_method, geography=geography,
                  geography_map_key=geography_map_key, input_type=input_type,
                  interpolation_method=interpolation_method, subsector=subsector)

