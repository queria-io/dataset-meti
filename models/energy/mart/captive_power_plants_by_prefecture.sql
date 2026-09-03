select
    fiscal_year,
    pref_code,
    pref_name,
    power_source_group,
    power_source_name,
    is_reference,
    plant_count
from {{ ref('stg_power_captive_halfyear_plants') }}
