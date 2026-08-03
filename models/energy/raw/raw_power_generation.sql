{# 電力調査統計 2-(2) 都道府県別発電実績の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_generation.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_generation.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'pref_code': 'VARCHAR',
        'pref_name': 'VARCHAR',
        'hydro_mwh': 'DOUBLE',
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
