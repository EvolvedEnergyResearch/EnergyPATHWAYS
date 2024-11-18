
Model Output File Descriptions
==============================

After the model finishes its run and results folders are saved to the
model_runs folder, it is recommended to aggregate the results using the
“compile finished cases” button in the controls tab. After this process
is completed, several core data files are featured in the
\_aggregate_outputs_EP folder (in the loaded scenario folder of
model_runs). These files and their contents are summarized below. Some
files may be too large for viewing in Microsoft Excel. For this reason,
Tableu is recommended for easy viewing and chart construction.

d_air_pollution.csv: annual air pollutant emissions for each subsector
broken down by pollutant type, demand technology, energy type,
geography, and case (e.g., reference).

d_annual_costs.csv: outlines annual costs for each subsector by cost
type (e.g., capital, installation), demand technology, geography, and
case (e.g., reference).

d_annual_costs_documentation.csv: outlines stock costs for different
technologies (e.g., cost to replace a bus) by cost type (e.g., capital,
OM), geography, whether item is new or replacement, case (e.g.,
reference), and vintage (make year).

d_driver.csv: outlines all drivers and respective projections (e.g.,
population) by geography, case (e.g., reference), and year.

d_energy.csv: outlines annual energy consumption for each subsector by
demand technology, energy type, geography, case (e.g., reference).

d_levelized_costs.csv: outlines annual levelized costs for each
subsector by cost type (e.g., capital, OM), demand technology,
geography, and case (e.g., reference).

d_sales.csv: outlines annual sales of different technologies by
technology type, geography, case (e.g., reference), and
sector/subsector.

d_service_demand.csv: outlines annual service demand (e.g., kilometers)
allocation by technology type, energy type, geography, case (e.g.,
reference), and sector/subsector.

d_stock.csv: outlines annual technology stock by technology type,
geography, case (e.g., reference), and sector/subsector.

electricity_reconciliation.csv: used for debugging; represents mismatch
between bottom-up and top-down shapes, which can help guide data updates
to the bottom up shapes.

subsector_electricity_profiles.csv: outline subsector electricity demand
in GJ for every hour of the year broken down by geography, case (e.g.,
reference), sector/subsector, and year (NZAu did 10 year increments for
this output file: 20201, 2030, 2040, 2050, 2060).

subsector_liquid_hydrogen_profiles.csv: same as
subsector_electricity_profiles.csv but for liquid hydrogen demand.

subsector_on-site_hydrogen_profiles.csv: same as
subsector_electricity_profiles.csv but for on-site hydrogen demand.

subsector_pipeline_gas_profiles.csv: same as
subsector_electricity_profiles.csv but for pipeline gas demand.