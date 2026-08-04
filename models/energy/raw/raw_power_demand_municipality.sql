{# 電力調査統計 6-(1) 市町村別需要電力量の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_demand_municipality.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_demand_municipality.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'pref_code': 'VARCHAR',
        'pref_name': 'VARCHAR',
        'municipality_name': 'VARCHAR',
        'extra_high_and_high_demand_mwh': 'DOUBLE',
        'low_demand_mwh': 'DOUBLE',
        'total_demand_mwh': 'DOUBLE',
        'published_as_of': 'DATE'
    }
)
