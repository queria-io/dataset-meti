{# 年月から年度（4月始まり）と年・月を導く。原典は年度単位のファイルに 9 月末・3 月末の
   2 シートが入る形で、年度そのものを持つ列は無い。 #}

select
    cast(left(year_month, 4) as integer) as year,
    cast(right(year_month, 2) as integer) as month,
    case
        when cast(right(year_month, 2) as integer) >= 4
            then cast(left(year_month, 4) as integer)
        else cast(left(year_month, 4) as integer) - 1
    end as fiscal_year,
    year_month,
    area_name,
    hydro_plants,
    hydro_capacity_kw,
    thermal_steam_plants,
    thermal_steam_capacity_kw,
    thermal_gas_turbine_plants,
    thermal_gas_turbine_capacity_kw,
    thermal_internal_combustion_plants,
    thermal_internal_combustion_capacity_kw,
    thermal_plants,
    thermal_capacity_kw,
    thermal_cogeneration_plants,
    thermal_cogeneration_capacity_kw,
    nuclear_plants,
    nuclear_capacity_kw,
    wind_plants,
    wind_capacity_kw,
    solar_plants,
    solar_capacity_kw,
    geothermal_plants,
    geothermal_capacity_kw,
    storage_battery_plants,
    storage_battery_capacity_kw,
    new_energy_plants,
    new_energy_capacity_kw,
    other_plants,
    other_capacity_kw,
    total_plants,
    total_capacity_kw
from {{ ref('raw_power_plants_captive') }}
