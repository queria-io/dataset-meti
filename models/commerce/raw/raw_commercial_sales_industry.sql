{# 商業動態統計調査 業種別商業販売額（月次）の生データ。
   main.py が METI 公開 Excel を取得・整形して .queria/meti_commercial_sales_industry.csv に保存する。 #}

{{ config(materialized='table') }}

select *
from read_csv(
    '.queria/meti_commercial_sales_industry.csv',
    header=true,
    {# 英語の項目名にコンマが入るので、引用符を明示する（自動判定だと引用符なしと見なされる） #}
    quote='"',
    escape='"',
    columns={
        'year_month': 'VARCHAR',
        'industry_order': 'INTEGER',
        'industry_name': 'VARCHAR',
        'industry_name_en': 'VARCHAR',
        'sales_value_billion_yen': 'DOUBLE'
    }
)
