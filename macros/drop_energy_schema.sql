{# energy スキーマを enecho データセットへ移した後始末。
   モデルファイルを消しても DuckLake 側のテーブルとビューは残るので、公開中のバージョンから落とす。
   DROP はデータベース名まで修飾する (既定のデータベースは :memory:)。
   本番の Sync が 1 回通ったら、この macro と dbt_project.yml の on-run-start をまとめて消してよい #}
{% macro drop_energy_schema() %}
  {% if not execute %}{{ return('') }}{% endif %}
  {% set views = run_query(
      "SELECT view_name FROM duckdb_views()"
      ~ " WHERE database_name = 'meti' AND schema_name = 'energy'"
  ) %}
  {% for row in views.rows %}
    {% do log('dropping view meti.energy.' ~ row[0], info=True) %}
    {% do run_query('DROP VIEW meti.energy."' ~ row[0] ~ '"') %}
  {% endfor %}
  {% set tables = run_query(
      "SELECT table_name FROM duckdb_tables()"
      ~ " WHERE database_name = 'meti' AND schema_name = 'energy'"
  ) %}
  {% for row in tables.rows %}
    {% do log('dropping table meti.energy.' ~ row[0], info=True) %}
    {% do run_query('DROP TABLE meti.energy."' ~ row[0] ~ '"') %}
  {% endfor %}
  {% set schemas = run_query(
      "SELECT schema_name FROM duckdb_schemas()"
      ~ " WHERE database_name = 'meti' AND schema_name = 'energy'"
  ) %}
  {% if schemas.rows | length > 0 %}
    {% do log('dropping schema meti.energy', info=True) %}
    {% do run_query('DROP SCHEMA meti.energy') %}
  {% endif %}
{% endmacro %}
