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
    pref_code,
    pref_name,
    extra_high_demand_mwh,
    extra_high_retailers,
    high_demand_mwh,
    high_retailers,
    low_demand_mwh,
    low_regulated_demand_mwh,
    low_liberalized_demand_mwh,
    low_retailers,
    total_demand_mwh,
    total_retailers,
    published_as_of
from {{ ref('raw_power_demand') }}
