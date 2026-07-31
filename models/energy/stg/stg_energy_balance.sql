{# 系列ラベルから実数と比率を区別する。構成比・前年度比・自給率（％表記）は
   いずれも小数で公表されるため、単位を持つ実数と混ぜて集計できない。 #}

select
    table_no,
    table_name,
    item_name,
    item_level,
    series,
    case
        when series in ('構成比', '前年度比', '%') then 'ratio'
        else 'quantity'
    end as value_type,
    fiscal_year,
    value,
    source_edition
from {{ ref('raw_energy_balance') }}
