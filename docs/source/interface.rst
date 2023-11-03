====================
User Interface
====================

Starting a run
--------------

.. raw:: html

    <div style>
		<iframe width="560" height="315" src="https://www.youtube.com/embed/XUrZwRJWyw0" frameborder="0" allowfullscreen></iframe>
    </div>

Creating a new run
------------------

.. raw:: html

    <div style>
		<iframe width="560" height="315" src="https://www.youtube.com/embed/XUrZwRJWyw0" frameborder="0" allowfullscreen></iframe>
    </div>

Configuration options
---------------------

::

    ##################################################
    [DATABASE]
    ##################################################
    database_path = C:\ep_db_us_2021\database

    ##################################################
    [CALCULATION_PARAMETERS]
    ##################################################
    parallel_process = False
    num_cores = 3

    ##################################################
    [TIME]
    ##################################################
    current_year = 2018
    end_year = 2050
    weather_years = 2011
    dispatch_outputs_timezone = US/Eastern

    ##################################################
    [GEOGRAPHY]
    ##################################################
    default_geography_map_key = Households 2010 (complete count)
    demand_primary_geography = US-16
    supply_primary_geography = US-16
    primary_subset = Lower Forty-eight, alaska and hawaii (north america)
    breakout_geography =
    include_foreign_gaus = True
    disagg_geography = state
    disagg_breakout_geography =

    ##################################################
    [UNITS]
    ##################################################
    energy_unit = mmBtu
    mass_unit = kilogram
    currency_name = USD
    currency_year = 2018
    inflation_rate = 0.02

    ##################################################
    [DEMAND_OUTPUT_DETAIL]
    ##################################################
    dod_years_subset =
    dod_vintage = False
    dod_demand_technology = True
    dod_cost_type = False
    dod_new_replacement = False
    dod_other_index_1 = True
    dod_other_index_2 = False
    dod_subsector_electricity_profiles = True
    dod_subsector_profile_years = 2020, 2050

    ##################################################
    [DEMAND_CALCULATION_PARAMETERS]
    ##################################################
    use_service_demand_modifiers = True
    removed_demand_levels =

    ##################################################
    [RIO]
    ##################################################
    rio_years = 2020, 2025, 2030, 2035, 2040, 2045, 2050
    ep2rio_final_energy_shapes = pipeline gas, liquid hydrogen, industrial captured co2, steam
    rio_mass_blends = co2 utilization blend A, co2 utilization blend B, non-energy co2 blend, product and bunkering co2 blend, Captured CO2 Blend
    rio_volume_blends =
    rio_distance_blends =
    rio_standard_mass_unit = tonne
    rio_standard_energy_unit = mmbtu
    rio_standard_distance_unit = meter
    rio_standard_volume_unit = liter
    rio_flex_load_subsectors = commercial air conditioning|| commercial space heating|| commercial water heating|| residential air conditioning|| residential space heating|| residential water heating|| heavy duty trucks|| light duty autos|| light duty trucks|| medium duty trucks
    rio_optimizable_subsectors =
    active_subsectors = commercial air conditioning|| commercial cooking|| commercial lighting|| commercial other|| commercial refrigeration|| commercial space heating|| commercial unspecified|| commercial ventilation|| commercial water heating|| district services|| office equipment (non-p.c.)|| office equipment (p.c.)|| Cement and Lime CO2 Capture|| Other Non-Energy CO2|| agriculture-crops|| agriculture-other|| aluminum industry|| balance of manufacturing other|| bulk chemicals|| cement|| computer and electronic products|| construction|| electrical equip., appliances, and components|| fabricated metal products|| food and kindred products|| glass and glass products|| iron and steel|| lime|| machinery|| metal and other non-metallic mining|| paper and allied products|| plastic and rubber products|| transportation equipment|| wood products|| residential air conditioning|| residential building shell|| residential clothes drying|| residential clothes washing|| residential computers and related|| residential cooking|| residential dishwashing|| residential freezing|| residential furnace fans|| residential lighting|| residential other uses|| residential refrigeration|| residential secondary heating|| residential space heating|| residential televisions and related|| residential water heating|| aviation|| buses|| domestic shipping|| freight rail|| heavy duty trucks|| international shipping|| light duty autos|| light duty trucks|| lubricants|| medium duty trucks|| military use|| motorcycles|| passenger rail|| recreational boats

    ##################################################
    [RIO_DB]
    ##################################################
    rio_database_path = C:\github\RIO_US_db\database

    ##################################################
    [LOG]
    ##################################################
    log_level = INFO
    stdout = True
