{# 年月から年度（4月始まり）と年・月を導き、電力量を MWh へ換算する。
   原典の単位は kWh（注8）で、同じ統計の 5-(2) や他の電力調査統計の表が
   1,000kWh 単位なので、そのままでは 1,000 倍ずれる。 #}

select
    cast(left(year_month, 4) as integer) as year,
    cast(right(year_month, 2) as integer) as month,
    case
        when cast(right(year_month, 2) as integer) >= 4
            then cast(left(year_month, 4) as integer)
        else cast(left(year_month, 4) as integer) - 1
    end as fiscal_year,
    year_month,
    pref_code,
    pref_name,
    power_source_group,
    power_source_name,
    is_reference,
    capacity_kw,
    generation_kwh / 1000 as generation_mwh,
    station_use_and_loss_kwh / 1000 as station_use_and_loss_mwh,
    transmission_to_utilities_kwh / 1000 as transmission_to_utilities_mwh,
    transmission_to_specified_supply_kwh / 1000 as transmission_to_specified_supply_mwh,
    transmission_to_other_operators_kwh / 1000 as transmission_to_other_operators_mwh,
    transmission_total_kwh / 1000 as transmission_total_mwh,
    transmission_via_exchange_kwh / 1000 as transmission_via_exchange_mwh,
    self_consumption_kwh / 1000 as self_consumption_mwh
from {{ ref('raw_power_captive_halfyear') }}
