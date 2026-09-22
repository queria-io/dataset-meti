{# 年月から年・月と年度（4月始まり）を導く。原典は暦年の月次で、年度を持つ列は無い。 #}

select
    cast(left(year_month, 4) as integer) as year,
    cast(right(year_month, 2) as integer) as month,
    case
        when cast(right(year_month, 2) as integer) >= 4
            then cast(left(year_month, 4) as integer)
        else cast(left(year_month, 4) as integer) - 1
    end as fiscal_year,
    year_month,
    business_type,
    item_order,
    item_name,
    item_name_en,
    sales_value_million_yen,
    establishments
from {{ ref('raw_retail_sales_business_type') }}
