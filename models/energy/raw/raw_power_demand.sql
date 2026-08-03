{# 電力調査統計 3-(2) 都道府県別電力需要実績の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_demand.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_demand.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'pref_code': 'VARCHAR',
        'pref_name': 'VARCHAR',
        'extra_high_demand_mwh': 'DOUBLE',
        'extra_high_retailers': 'INTEGER',
        'high_demand_mwh': 'DOUBLE',
        'high_retailers': 'INTEGER',
        'low_demand_mwh': 'DOUBLE',
        'low_regulated_demand_mwh': 'DOUBLE',
        'low_liberalized_demand_mwh': 'DOUBLE',
        'low_retailers': 'INTEGER',
        'total_demand_mwh': 'DOUBLE',
        'total_retailers': 'INTEGER',
        'published_as_of': 'DATE'
    }
)
