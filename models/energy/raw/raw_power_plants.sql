{# 電力調査統計 1-(2) 都道府県別発電所数、出力の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_plants.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_plants.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'pref_code': 'VARCHAR',
        'pref_name': 'VARCHAR',
        'hydro_plants': 'INTEGER',
        'hydro_capacity_kw': 'DOUBLE',
        'thermal_plants': 'INTEGER',
        'thermal_capacity_kw': 'DOUBLE',
        'nuclear_plants': 'INTEGER',
        'nuclear_capacity_kw': 'DOUBLE',
        'wind_plants': 'INTEGER',
        'wind_capacity_kw': 'DOUBLE',
        'solar_plants': 'INTEGER',
        'solar_capacity_kw': 'DOUBLE',
        'geothermal_plants': 'INTEGER',
        'geothermal_capacity_kw': 'DOUBLE',
        'biomass_plants': 'INTEGER',
        'biomass_capacity_kw': 'DOUBLE',
        'waste_plants': 'INTEGER',
        'waste_capacity_kw': 'DOUBLE',
        'storage_battery_plants': 'INTEGER',
        'storage_battery_capacity_kw': 'DOUBLE',
        'new_energy_plants': 'INTEGER',
        'new_energy_capacity_kw': 'DOUBLE',
        'other_plants': 'INTEGER',
        'other_capacity_kw': 'DOUBLE',
        'total_plants': 'INTEGER',
        'total_capacity_kw': 'DOUBLE',
        'published_as_of': 'DATE'
    }
)
