select
    fiscal_year,
    year,
    month,
    year_month,
    industry_order,
    industry_name,
    industry_name_en,
    sales_value_billion_yen
from {{ ref('stg_commercial_sales_industry') }}
