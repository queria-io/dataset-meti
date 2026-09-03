{# 年度計の欄の発電所数。年度そのものが原典の期間なので、月次の表と違って
   年・月を導かない。 #}

select
    fiscal_year,
    pref_code,
    pref_name,
    power_source_group,
    power_source_name,
    is_reference,
    plant_count
from {{ ref('raw_power_captive_halfyear_plants') }}
