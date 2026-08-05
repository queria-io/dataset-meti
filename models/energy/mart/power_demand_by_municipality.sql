select
    fiscal_year,
    year,
    month,
    year_month,
    pref_code,
    pref_name,
    municipality_name,
    extra_high_and_high_demand_mwh,
    low_demand_mwh,
    total_demand_mwh,
    published_as_of
from {{ ref('stg_power_demand_municipality') }}
