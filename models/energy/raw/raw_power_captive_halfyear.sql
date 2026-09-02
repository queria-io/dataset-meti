{# 電力調査統計 5 自家用発電所等実績（半期報の集計結果）の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_captive_halfyear.csv に保存する。
   電力量は原典どおり kWh で、MWh への換算は stg で行う。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_captive_halfyear.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'pref_code': 'VARCHAR',
        'pref_name': 'VARCHAR',
        'power_source_group': 'VARCHAR',
        'power_source_name': 'VARCHAR',
        'is_reference': 'BOOLEAN',
        'capacity_kw': 'DOUBLE',
        'generation_kwh': 'DOUBLE',
        'station_use_and_loss_kwh': 'DOUBLE',
        'transmission_total_kwh': 'DOUBLE',
        'transmission_to_utilities_kwh': 'DOUBLE',
        'transmission_to_specified_supply_kwh': 'DOUBLE',
        'transmission_to_other_operators_kwh': 'DOUBLE',
        'transmission_via_exchange_kwh': 'DOUBLE',
        'self_consumption_kwh': 'DOUBLE'
    }
)
