{# 商業動態統計調査 業態別・商品別販売額（月次）の生データ。
   main.py が METI 公開 Excel を取得・整形して .queria/meti_retail_sales_business_type.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_retail_sales_business_type.csv',
    header=true,
    {# 英語の項目名にコンマが入るので、引用符を明示する（自動判定だと引用符なしと見なされる） #}
    quote='"',
    escape='"',
    columns={
        'year_month': 'VARCHAR',
        'business_type': 'VARCHAR',
        'item_order': 'INTEGER',
        'item_name': 'VARCHAR',
        'item_name_en': 'VARCHAR',
        'sales_value_million_yen': 'DOUBLE',
        'establishments': 'BIGINT'
    }
)
