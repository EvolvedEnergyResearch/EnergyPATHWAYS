========
Database
========

Overview
--------
The EnergyPATHWAYS database represents all energy consuming sectors and subsectors of the economy, including residential, commercial, industrial, and transportation energy demands. This includes calibrated energy demand by subsector, and the scenario measures that impact energy demand by changing the way energy is consumed under different policy, technology, feasibility, or economic assumptions. You will make changes to the database to represent different goals and constraints.

Example components of demand scenarios include different rates of electrification of vehicles and appliances, different efficiency assumptions, different service demand assumptions such as adjustments to vehicle miles traveled, and different rates of electrification in industry. These can be used to represent policies that impact the demand side, or uncertainty about outcomes on the demand side due to consumer behavior and/or policy implementation.

Database Column Glossary
------------------------

**cost_of_capital**
    Technology cost of capital used in calculating levelized cost outputs.

**currency**
    Data input currency. Can be any from the currency table.

**currency_year**
    Year of currency value, used in inflating or deflating costs to a common year.

**extrapolation_method**
    Method used to extrapolate data to years not explicitly defined in the database. See Timeseries cleaning methods.

**interpolation_method**
    Method used to interpolate data between given years, can be different than the extrapolation method. See Timeseries cleaning methods.

**input_type**
    Specifying whether the input data represents an 'intensity' or a 'total' value.

**notes**
    Optional user notes for database rows.

**sensitivity**
    Sensitivity tag for the data input. Used when assigning sensitivity values to a scenario.

**source**
    Optional specification of the source of the data input.

**unit**
    Input unit for the data. The pint library is used for unit conversions and most units are supported.

**vintage**
    Specifies the sales year of a technology.

**year**
    Specifies the year of the data input.

**value**
    The value of the data input, must be numerical.

**final_energy**
    Specifies the final energy type of the data input. Can be any from the final energy table. Column may be optional.

**subsector**
    Specifies the subsector of the data input. Can be any from the subsector table. Column may be optional.

**demand_technology**
    Specifies the demand technology for energy or service demand. Column may be optional.

**min_lifetime**
    Minimum lifetime of a technology in years. User must either specify the min & max lifetime or the mean & lifetime variance.

**max_lifetime**
    Maximum lifetime of a technology in years. User must either specify the min & max lifetime or the mean & lifetime variance.

**mean_lifetime**
    Average lifetime of a technology in years. User must either specify the min & max lifetime or the mean & lifetime variance.

**lifetime_variance**
    Lifetime variance of a technology in years. User must either specify the min & max lifetime or the mean & lifetime variance.

**shape**
    Hourly shape of the service demand for a sector, subsector, or technology.

**linked**
    Technology that the current technology is linked to. For example, a heat pump that provides heating is also linked to a heat pump that provides cooling.

**stock_link_ratio**
    Allows the user to change the ratio of stock between linked technologies.

**driver_1**
    Energy demand driver useful for extrapolating demand. Can be any from the driver table. Multiple drivers can be used together to create a composite.

**driver_2**
    Energy demand driver useful for extrapolating demand. Can be any from the driver table. Multiple drivers can be used together to create a composite.

**driver_3**
    Energy demand driver useful for extrapolating demand. Can be any from the driver table. Multiple drivers can be used together to create a composite.

**driver_denominator_1**
    Indicates that the input data has been normalized by an underlying driver. For example, light duty service demand may be input as annual vehicle miles traveled per person. In this case, the driver denominator would be 'population'.

**driver_denominator_2**
    Indicates that the input data has been normalized by an underlying driver. For example, light duty service demand may be input as annual vehicle miles traveled per person. In this case, the driver denominator would be 'population'.

**base_driver**
    Used in the DemandDrivers table to help extrapolate drivers. For example, a driver of residential floor area may have a base driver of households, which may have a base driver of population.

**gau**
    Stands for 'geographical analysis unit' and is the term used to reference a single zone (or element) within a geographical category. For example, within a geography of state, each individual state is a gau.

**geography**
    Specifies the geographical category of the data input.

**geography_map_key**
    Used to upscale or downscale data inputs between geographies. See :ref:`Geographies`.

**is_stock_dependent**
    Used in the service demand table to specify whether total service demand is dependent on the size of the stock (True/False).

**is_service_demand_dependent**
    Used to specify whether energy demand or the size of a stock is dependent on the total size of the service demand (True/False).

**other_index_1**
    Optional additional index category to maintain during calculations. For example, in the residential sector, building type may be maintained as an additional level of granularity.

**other_index_2**
    Optional additional index category to maintain during calculations. For example, in the residential sector, building type may be maintained as an additional level of granularity.

**oth_1**
    One element from the other_index_1 category. If other_index_1 is 'building_type', oth_1 may be 'detached single family'.

**oth_2**
    One element from the other_index_1 category. If other_index_1 is 'building_type', oth_1 may be 'detached single family'.


Measures
--------

EnergyPATHWAYS operates at its simplest on the level of measures and scenarios. Scenarios are an aggregation of measures, defined here as actions undertaken to change the energy system from a business-as-usual projection.

On the demand side, we employ the following six types of measures:

   **Sales Share Measures** (database table: ``DemandSalesShareMeasures``)
      These measures change the deployment of technologies using the concept of sales shares. If we wanted to change the penetration of electric vehicles (EVs) into the market, we could develop a measure that creates any level of adoption we want.  These measures can be used in any subsectors with technology-level stock representation.

   **Stock Measures** (database table: ``DemandStockMeasures``)
      These measure also change the deployment of technologies using the concept of stock instead of sales. While equipment sales are the equipment put into service in a specific year and thus of a certain vintage, equipment stock are all stocks that are operating in a certain year of a variety of vintages. If we want to say that the sum of all EVs on the road in 2030 will equal 1.5 million, we would do so with a stock measure. These measures can be used in any subsectors with technology-level stock representation.

   **Service Demand Measures** (database table: ``DemandServiceDemandMeasures``)
     These measures alter the projection of service demand in a demand subsector. For example, if we projected a 25% decline in vehicle miles traveled due to land-use and ridesharing policies, we could enter that as a measure here.

   **Energy Efficiency Measures** (database table: ``DemandEnergyEfficiencyMeasures``)
      Energy efficiency measures are used in demand subsectors where we do not have technology and stock-level representation of end-use equipment.  We can change the trajectory of energy demand, however, by implementing generic energy efficiency measures that can achieve energy reductions at a specified cost.

   **Fuel-Switching Measures** (database table: ``DemandFuelSwitchingMeasures``)
      Fuel switching measures are also used in demand subsectors without technology-level representations. We can implement these measures to change the composition of final energy demand. For example, if we wanted to change the final energy type in process heating from pipeline gas to electricity, we could do so with a fuel–switching measure.

Geographies
-----------
Three input tables govern the geographies used in EnergyPATHWAYS. These are Geographies, GeographyMapKeys, and GeographiesSpatialJoin. The first two files reference the GeographiesSpatialJoin table and help identify and validate the columns. When creating a database for a new location, the GeographiesSpatialJoin table is often the very first file that gets updated.

