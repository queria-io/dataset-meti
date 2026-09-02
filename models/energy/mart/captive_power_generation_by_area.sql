select
    fiscal_year,
    year,
    month,
    year_month,
    area_name,
    power_source_group,
    power_source_name,
    is_reference,
    generation_mwh,
    station_use_and_loss_mwh,
    transmission_to_utilities_mwh,
    transmission_to_specified_supply_mwh,
    transmission_to_other_operators_mwh,
    transmission_total_mwh,
    transmission_via_exchange_mwh,
    self_consumption_mwh
from {{ ref('stg_power_generation_captive') }}
