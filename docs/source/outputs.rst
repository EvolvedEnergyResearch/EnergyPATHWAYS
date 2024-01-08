=======
Outputs
=======

Folder Structure
===================

General Terminology
===================

In addition to indices specific to each file, the following includes a list and description of common indices:

**Primary Geography**
  The primary geography defines the geographic granularity for an EP run.

**Sector**
  Demand sectors that include residential, commercial, transportation, and productive (industrial and agricultural sectors excluding those that are part of the energy supply chain, Ex. refining)

**Subsector**
  More detailed units of demand analysis. Associated with unique energy service demands. Ex. residential water heating.

**Final Energy**
  An energy type consumed to satisfy energy service demand. Differentiated from upstream energy use that is consumed to produce final energy.

**Scenario**
  Scenario name

**Year**
  Corresponding year of outputs.


Output Files
===================

d_annual_costs.csv
------------------

Annual spending on demand-side equipment (water heaters, vehicles, etc.) and efficiency measures. These costs are not levelized and represent actual needed outlays in each year.

d_driver.csv
------------

Underlying drivers of demand stock and service demand projections (ex., households; heating degree days). 

d_energy.csv
------------

Final energy demand by technology and final energy type (ex., pipeline gas consumed by a residential natural gas furnace).

d_levelized_costs.csv
---------------------

Demand-side equipment capital costs which are translated into annualized costs.

d_sales.csv
-----------

Quantity of demand-side equipment purchased each year by technology (ex., number of electric vehicles sold in each year)

d_service_demand.csv
--------------------

Projections of energy service demands by demand sub-sector (ex., vehicle miles traveled; lumen-hours; etc.)

d_stock.csv
-----------

Quantity of demand-side equipment stocks by technology (ex., electric vehicles; water heaters).

Index Descriptions:
- Unit: unit of demand technology stock. For example, the unit for commercial water heaters is kiloBTU capacity. 
