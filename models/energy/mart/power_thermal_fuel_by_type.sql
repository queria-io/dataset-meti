select
    fiscal_year,
    year,
    month,
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
from {{ ref('stg_power_thermal_fuel') }}
