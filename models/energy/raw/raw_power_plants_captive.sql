{# 電力調査統計 5-(1) 自家用発電所数、出力の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_plants_captive.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_plants_captive.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'area_name': 'VARCHAR',
        'hydro_plants': 'INTEGER',
        'hydro_capacity_kw': 'DOUBLE',
        'thermal_steam_plants': 'INTEGER',
        'thermal_steam_capacity_kw': 'DOUBLE',
        'thermal_gas_turbine_plants': 'INTEGER',
        'thermal_gas_turbine_capacity_kw': 'DOUBLE',
        'thermal_internal_combustion_plants': 'INTEGER',
        'thermal_internal_combustion_capacity_kw': 'DOUBLE',
        'thermal_plants': 'INTEGER',
        'thermal_capacity_kw': 'DOUBLE',
        'thermal_cogeneration_plants': 'INTEGER',
        'thermal_cogeneration_capacity_kw': 'DOUBLE',
        'nuclear_plants': 'INTEGER',
        'nuclear_capacity_kw': 'DOUBLE',
        'wind_plants': 'INTEGER',
        'wind_capacity_kw': 'DOUBLE',
        'solar_plants': 'INTEGER',
        'solar_capacity_kw': 'DOUBLE',
        'geothermal_plants': 'INTEGER',
        'geothermal_capacity_kw': 'DOUBLE',
        'storage_battery_plants': 'INTEGER',
        'storage_battery_capacity_kw': 'DOUBLE',
        'new_energy_plants': 'INTEGER',
        'new_energy_capacity_kw': 'DOUBLE',
        'other_plants': 'INTEGER',
        'other_capacity_kw': 'DOUBLE',
        'total_plants': 'INTEGER',
        'total_capacity_kw': 'DOUBLE'
    }
)
