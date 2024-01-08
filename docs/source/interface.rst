====================
User Interface
====================

Tour of the user interface:
--------------

Interface Overview
==================

.. raw:: html

    <div style>
		<iframe width="560" height="315" src="https://youtu.be/eC71ub9TSSg" frameborder="0" allowfullscreen></iframe>
    </div>

Configuration Options
=====================

.. raw:: html

    <div style>
		<iframe width="560" height="315" src="https://youtu.be/cRrxK1UJHKs" frameborder="0" allowfullscreen></iframe>
    </div>

Scenarios and Sensitivities
===========================

.. raw:: html

    <div style>
		<iframe width="560" height="315" src="https://youtu.be/oY28yLv_0fI" frameborder="0" allowfullscreen></iframe>
    </div>

Launching EnergyPATHWAYS
========================

.. raw:: html

    <div style>
		<iframe width="560" height="315" src="https://youtu.be/pxMttnLEFW8" frameborder="0" allowfullscreen></iframe>
    </div>

Interface Debugging
========================

.. raw:: html

    <div style>
		<iframe width="560" height="315" src="https://youtu.be/8evvCluebMg" frameborder="0" allowfullscreen></iframe>
    </div>

Configuration options
---------------------

The configuration file is a text file that contains all the configuration options for the model. The configuration file is divided into sections, each of which contains a number of options with values that define how the model will run.

::

    ##################################################
    [DATABASE]
    ##################################################
    database_path = C:\ep_db_au\database

    ##################################################
    [CALCULATION_PARAMETERS]
    ##################################################
    parallel_process = False
    num_cores = 3
    shape_check = True

    ##################################################
    [TIME]
    ##################################################
    current_year = 2018
    end_year = 2060
    weather_years = 2018
    dispatch_outputs_timezone = Australia/NSW

    ##################################################
    [GEOGRAPHY]
    ##################################################
    default_geography_map_key = tot_p_p
    demand_primary_geography = nzau-geography
    primary_subset =
    breakout_geography =
    include_foreign_gaus = True
    disagg_geography = sa4
    disagg_breakout_geography =

    ##################################################
    [UNITS]
    ##################################################
    energy_unit = gigajoule
    mass_unit = kilogram
    currency_name = AUD
    currency_year = 2020
    inflation_rate = 0.027

    ##################################################
    [DEMAND_OUTPUT_DETAIL]
    ##################################################
    dod_years_subset =
    dod_vintage = False
    dod_demand_technology = True
    dod_cost_type = True
    dod_new_replacement = False
    dod_other_index_1 = True
    dod_other_index_2 = False
    dod_output_hourly_profiles = True
    dod_hourly_profile_final_energy_types = electricity, pipeline gas, liquid hydrogen, on-site hydrogen
    dod_hourly_profile_years = 2021, 2030, 2040, 2050, 2060
    dod_hourly_profile_keep_subsector = True
    dod_hourly_profile_keep_feeder = False

    ##################################################
    [DEMAND_CALCULATION_PARAMETERS]
    ##################################################
    use_service_demand_modifiers = True
    removed_demand_levels =

    ##################################################
    [RIO]
    ##################################################
    rio_years = 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060
    ep2rio_final_energy_shapes = pipeline gas, liquid hydrogen, industrial captured co2
    rio_standard_mass_unit = tonne
    rio_standard_energy_unit = mmbtu
    rio_standard_distance_unit = meter
    rio_standard_volume_unit = liter
    rio_flex_load_subsectors = residential water heating|| light commercial vehicles|| passenger vehicles
    rio_optimizable_subsectors =
    active_subsectors = commercial and services|| agriculture forestry and fishing|| agriculture non-energy|| basic chemical and chemical; polymer and rubber product manufacturing|| basic non-ferrous metals|| cement co2 capture|| cement; lime; plaster and concrete|| ceramics|| construction|| energy exports|| fabricated metal products|| food; beverages and tobacco|| furniture and other manufacturing|| glass and glass products|| industrial process non-energy|| iron and steel|| lulucf non-energy|| machinery and equipment|| non-metallic mineral products|| other mining|| other non-metallic mineral products|| other petroleum and coal product manufacturing|| pulp; paper and printing|| solvents; lubricants; greases and bitumen|| textile; clothing; footwear and leather|| waste non-energy|| water supply; sewerage and drainage services|| wood and wood products|| residential air conditioning|| residential clothes drying|| residential clothes washing|| residential cooktops and ovens|| residential dishwashing|| residential fans|| residential freezing|| residential it&he|| residential lighting|| residential microwave|| residential other appliances|| residential pools|| residential refrigeration|| residential space heating|| residential water heating|| articulated trucks|| buses|| domestic air transport|| domestic water transport|| international air transport|| international water transport|| light commercial vehicles|| motorcycles|| other transport; services and storage|| passenger vehicles|| rail transport|| rigid and other trucks

    ##################################################
    [RIO_DB]
    ##################################################
    rio_database_path = C:\rio_db_au\database
    shape_database_path =

    ##################################################
    [LOG]
    ##################################################
    log_level = INFO
    stdout = True
