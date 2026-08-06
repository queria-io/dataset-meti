{# 電力調査統計 4 火力発電燃料実績の生データ。
   main.py が資源エネルギー庁の公開 Excel を年度ごとに取得・整形して
   .queria/meti_power_thermal_fuel.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_power_thermal_fuel.csv',
    header=true,
    columns={
        'year_month': 'VARCHAR',
        'fuel_name': 'VARCHAR',
        'quantity_unit': 'VARCHAR',
        'heat_value_unit': 'VARCHAR',
        'receipt_quantity': 'DOUBLE',
        'consumption_quantity': 'DOUBLE',
        'consumption_dry_quantity': 'DOUBLE',
        'heat_value': 'DOUBLE',
        'month_end_stock_quantity': 'DOUBLE',
        'published_as_of': 'DATE'
    }
)
