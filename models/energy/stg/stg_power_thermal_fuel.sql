{# 年月から年度（4月始まり）と年・月を導く。原典は年度単位のファイルに月次シートが
   並ぶ形で、年度そのものを持つ列は無い。

   消費量×発熱量の投入熱量は導かない。石炭とバイオマスは消費量が湿・乾の 2 段で、
   発熱量のセルは 2 段にまたがる結合セルなのでどちらの基準の値か原典から決まらない。 #}

select
    cast(left(year_month, 4) as integer) as year,
    cast(right(year_month, 2) as integer) as month,
    case
        when cast(right(year_month, 2) as integer) >= 4
            then cast(left(year_month, 4) as integer)
        else cast(left(year_month, 4) as integer) - 1
    end as fiscal_year,
    year_month,
    fuel_name,
    quantity_unit,
    heat_value_unit,
    receipt_quantity,
    consumption_quantity,
    consumption_dry_quantity,
    heat_value,
    month_end_stock_quantity,
    published_as_of
from {{ ref('raw_power_thermal_fuel') }}
