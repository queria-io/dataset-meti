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
    operator_category,
    operator_category_ja,
    operator_name,
    is_retail,
    is_general_transmission_distribution,
    is_transmission,
    is_distribution,
    is_specified_transmission_distribution,
    is_generation,
    is_specified_wholesale,
    liberalized_demand_mwh,
    liberalized_extra_high_demand_mwh,
    liberalized_high_demand_mwh,
    liberalized_low_demand_mwh,
    liberalized_low_lighting_demand_mwh,
    liberalized_low_power_demand_mwh,
    regulated_demand_mwh,
    regulated_lighting_demand_mwh,
    regulated_power_demand_mwh,
    last_resort_supply_mwh,
    remote_island_supply_mwh,
    total_demand_mwh,
    published_as_of
from {{ ref('raw_power_demand_operator') }}
