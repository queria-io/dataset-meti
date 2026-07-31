select
    table_no,
    table_name,
    item_name,
    item_level,
    series,
    value_type,
    fiscal_year,
    value,
    source_edition
from {{ ref('stg_energy_balance') }}
