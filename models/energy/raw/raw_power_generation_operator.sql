{# 電力調査統計 2-(1) 発電実績の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_generation_operator.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_generation_operator.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'operator_name': 'VARCHAR',
        'is_retail': 'BOOLEAN',
        'is_general_transmission_distribution': 'BOOLEAN',
        'is_transmission': 'BOOLEAN',
        'is_distribution': 'BOOLEAN',
        'is_specified_transmission_distribution': 'BOOLEAN',
        'is_generation': 'BOOLEAN',
        'is_specified_wholesale': 'BOOLEAN',
        'hydro_conventional_mwh': 'DOUBLE',
        'hydro_pumped_storage_mwh': 'DOUBLE',
        'hydro_mwh': 'DOUBLE',
        'thermal_coal_mwh': 'DOUBLE',
        'thermal_lng_mwh': 'DOUBLE',
        'thermal_oil_mwh': 'DOUBLE',
        'thermal_lpg_mwh': 'DOUBLE',
        'thermal_other_gas_mwh': 'DOUBLE',
        'thermal_bituminous_mwh': 'DOUBLE',
        'thermal_other_mwh': 'DOUBLE',
        'thermal_mwh': 'DOUBLE',
        'nuclear_mwh': 'DOUBLE',
        'wind_mwh': 'DOUBLE',
        'solar_mwh': 'DOUBLE',
        'geothermal_mwh': 'DOUBLE',
        'biomass_mwh': 'DOUBLE',
        'waste_mwh': 'DOUBLE',
        'storage_battery_mwh': 'DOUBLE',
        'new_energy_mwh': 'DOUBLE',
        'other_mwh': 'DOUBLE',
        'total_mwh': 'DOUBLE',
        'published_as_of': 'DATE'
    }
)
