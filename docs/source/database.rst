====================
Database
====================

Key Concepts
====================

Geographies
--------------------

Cleaning methods
--------------------

Sensitivities
--------------------

When loading the model, EnergyPATHWAYS will use the data from ``table`` for the specified ``parent_id`` that contain this value in the ``sensitivity`` column. When no sensitivity is specifid for a particular table and parent_id, EnergyPATHWAYS will load the data that has ``NULL`` in the ``sensitivity`` column.

Tables
====================
i.	Subsectors
ii.	FinalEnergy
iii.	DemandDrivers
iv.	DemandEnergyDemands
v.	DemandServiceDemands
vi.	DemandStock
vii.	DemandSales
viii.	DemandTechs
ix.	ServiceDemandModifiers
x.	ServiceLinks
xi.	Geographies
xii.	GeographiesSpatialJoin
xiii.	GeographyMapKeys
xiv.	OtherIndexes

Measures
====================

EnergyPATHWAYS operates at its simplest on the level of measures and scenarios. Scenarios are an aggregation of measures, defined here as actions undertaken to change the energy system from a business-as-usual projection.

Demand-Side Measures
--------------------

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

   **Flexible Load Measures** (database table: ``DemandFlexibleLoadMeasures``)
      Flexible load measures define the amount of electric load in a subsector that we anticipate can be moved in time. For example, if we wanted 25% of residential electric water heating to be dynamically used to reduce peak loads and facilitate renewable integration, we could achieve that with a flexible load measure.

