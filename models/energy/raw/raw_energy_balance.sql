{# 総合エネルギー統計 時系列表の生データ。
   main.py が資源エネルギー庁の公開 Excel を取得・整形して
   .queria/meti_energy_balance.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_energy_balance.csv',
    header=true,
    columns={
        'table_no': 'INTEGER',
        'table_name': 'VARCHAR',
        'item_name': 'VARCHAR',
        'item_level': 'INTEGER',
        'series': 'VARCHAR',
        'fiscal_year': 'INTEGER',
        'value': 'DOUBLE',
        'source_edition': 'VARCHAR'
    }
)
