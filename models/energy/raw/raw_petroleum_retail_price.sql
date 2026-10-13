{# 石油製品価格調査 給油所小売価格（週次）の生データ。
   main.py が資源エネルギー庁の公開 Excel（週次ファイル）を取得・整形して
   .queria/meti_petroleum_retail_price.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_petroleum_retail_price.csv',
    header=true,
    columns={
        'survey_date': 'DATE',
        'product_name': 'VARCHAR',
        'price_unit': 'VARCHAR',
        'area_order': 'INTEGER',
        'area_name': 'VARCHAR',
        'area_level': 'VARCHAR',
        'pref_code': 'VARCHAR',
        'pref_name': 'VARCHAR',
        'price_yen': 'DOUBLE',
        'fuel_tax_yen': 'DOUBLE',
        'consumption_tax_rate': 'DOUBLE'
    }
)
