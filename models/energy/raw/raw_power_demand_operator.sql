{# 電力調査統計 3-(1) 電力需要実績の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_demand_operator.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_demand_operator.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'operator_category': 'VARCHAR',
        'operator_category_ja': 'VARCHAR',
        'operator_name': 'VARCHAR',
        'is_retail': 'BOOLEAN',
        'is_general_transmission_distribution': 'BOOLEAN',
        'is_transmission': 'BOOLEAN',
        'is_distribution': 'BOOLEAN',
        'is_specified_transmission_distribution': 'BOOLEAN',
        'is_generation': 'BOOLEAN',
        'is_specified_wholesale': 'BOOLEAN',
        'liberalized_demand_mwh': 'DOUBLE',
        'liberalized_extra_high_demand_mwh': 'DOUBLE',
        'liberalized_high_demand_mwh': 'DOUBLE',
        'liberalized_low_demand_mwh': 'DOUBLE',
        'liberalized_low_lighting_demand_mwh': 'DOUBLE',
        'liberalized_low_power_demand_mwh': 'DOUBLE',
        'regulated_demand_mwh': 'DOUBLE',
        'regulated_lighting_demand_mwh': 'DOUBLE',
        'regulated_power_demand_mwh': 'DOUBLE',
        'last_resort_supply_mwh': 'DOUBLE',
        'remote_island_supply_mwh': 'DOUBLE',
        'total_demand_mwh': 'DOUBLE',
        'published_as_of': 'DATE'
    }
)
