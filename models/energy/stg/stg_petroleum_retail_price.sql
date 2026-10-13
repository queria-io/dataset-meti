{# 調査日から年を導き、価格が消費税込みかを持たせる。原典の注記は「2004年4月以前は
   消費税抜きの価格」で、値は2004年3月29日調査から4月5日調査で税込みの水準へ跳ぶ。
   総額表示の義務化（2004年4月1日）以降の調査日を税込みとする。 #}

select
    survey_date,
    cast(year(survey_date) as integer) as year,
    product_name,
    price_unit,
    area_order,
    area_name,
    area_level,
    pref_code,
    pref_name,
    price_yen,
    fuel_tax_yen,
    consumption_tax_rate,
    survey_date >= date '2004-04-01' as includes_consumption_tax
from {{ ref('raw_petroleum_retail_price') }}
