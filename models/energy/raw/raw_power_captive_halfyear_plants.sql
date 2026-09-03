{# 電力調査統計 5 自家用発電所等実績のうち、年度計の欄にしか無い発電所数の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_captive_halfyear_plants.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_captive_halfyear_plants.csv',
    header=true,
    columns={
        'fiscal_year': 'INTEGER',
        'pref_code': 'VARCHAR',
        'pref_name': 'VARCHAR',
        'power_source_group': 'VARCHAR',
        'power_source_name': 'VARCHAR',
        'is_reference': 'BOOLEAN',
        'plant_count': 'INTEGER'
    }
)
