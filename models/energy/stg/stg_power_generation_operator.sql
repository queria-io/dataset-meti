{# 年月から年度（4月始まり）と年・月を導く。原典は年度単位のファイルに月次シートが
   並ぶ形で、年度そのものを持つ列は無い。 #}

select
    cast(left(year_month, 4) as integer) as year,
    cast(right(year_month, 2) as integer) as month,
    case
        when cast(right(year_month, 2) as integer) >= 4
            then cast(left(year_month, 4) as integer)
        else cast(left(year_month, 4) as integer) - 1
    end as fiscal_year,
    year_month,
    operator_name,
    is_retail,
    is_general_transmission_distribution,
    is_transmission,
    is_distribution,
    is_specified_transmission_distribution,
    is_generation,
    is_specified_wholesale,
    hydro_conventional_mwh,
    hydro_pumped_storage_mwh,
    hydro_mwh,
    thermal_coal_mwh,
    thermal_lng_mwh,
    thermal_oil_mwh,
    thermal_lpg_mwh,
    thermal_other_gas_mwh,
    thermal_bituminous_mwh,
    thermal_other_mwh,
    thermal_mwh,
    nuclear_mwh,
    wind_mwh,
    solar_mwh,
    geothermal_mwh,
    biomass_mwh,
    waste_mwh,
    storage_battery_mwh,
    new_energy_mwh,
    other_mwh,
    total_mwh,
    published_as_of
from {{ ref('raw_power_generation_operator') }}
