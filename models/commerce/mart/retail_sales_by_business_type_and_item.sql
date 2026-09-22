select
    fiscal_year,
    year,
    month,
    year_month,
    business_type,
    item_order,
    item_name,
    item_name_en,
    sales_value_million_yen,
    establishments
from {{ ref('stg_retail_sales_business_type') }}
