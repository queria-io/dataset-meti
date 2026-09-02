{# 年月から年度（4月始まり）と年・月を導く。原典は年度単位のファイルを
   上期・下期の 2 シートに分けており、年度そのものを持つ列は無い。 #}

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
    power_source_group,
    power_source_name,
    is_reference,
    generation_mwh,
    station_use_and_loss_mwh,
    transmission_to_utilities_mwh,
    transmission_to_specified_supply_mwh,
    transmission_to_other_operators_mwh,
    transmission_total_mwh,
    transmission_via_exchange_mwh,
    self_consumption_mwh
from {{ ref('raw_power_generation_captive') }}
