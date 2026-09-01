{# 電力調査統計 5-(2) 自家用発電実績の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_generation_captive.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_generation_captive.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'area_name': 'VARCHAR',
        'power_source_group': 'VARCHAR',
        'power_source_name': 'VARCHAR',
        'is_reference': 'BOOLEAN',
        'generation_mwh': 'DOUBLE',
        'station_use_and_loss_mwh': 'DOUBLE',
        'transmission_to_utilities_mwh': 'DOUBLE',
        'transmission_to_specified_supply_mwh': 'DOUBLE',
        'transmission_to_other_operators_mwh': 'DOUBLE',
        'transmission_total_mwh': 'DOUBLE',
        'transmission_via_exchange_mwh': 'DOUBLE',
        'self_consumption_mwh': 'DOUBLE'
    }
)
