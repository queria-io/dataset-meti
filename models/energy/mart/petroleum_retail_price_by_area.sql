select
    survey_date,
    year,
    product_name,
    price_unit,
    area_order,
    area_name,
    area_level,
    pref_code,
    pref_name,
    price_yen,
    fuel_tax_yen,
    consumption_tax_rate,
    includes_consumption_tax
from {{ ref('stg_petroleum_retail_price') }}
