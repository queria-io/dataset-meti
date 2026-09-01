"""経済産業省の統計の取得 + dbt ビルド。

1. ita:          第３次産業活動指数の公開 Excel を取得し縦持ち CSV へ整形（季調・原の月次）
2. total_energy: 総合エネルギー統計 時系列表の公開 Excel を取得し縦持ち CSV へ整形
3. power_survey: 電力調査統計 都道府県別電力需要実績の公開 Excel を年度ごとに取得し CSV へ整形
4. power_generation: 電力調査統計 都道府県別発電実績の公開 Excel を年度ごとに取得し CSV へ整形
5. power_demand_operator: 電力調査統計 電力需要実績（事業者別）の公開 Excel を年度ごとに取得し CSV へ整形
6. power_generation_operator: 電力調査統計 発電実績（事業者別）の公開 Excel を年度ごとに取得し CSV へ整形
7. power_municipality: 電力調査統計 市町村別需要電力量・逆潮流量の公開 Excel を年度ごとに取得し CSV へ整形
8. power_plants:  電力調査統計 都道府県別発電所数、出力の公開 Excel を年度ごとに取得し CSV へ整形
9. power_thermal_fuel: 電力調査統計 火力発電燃料実績の公開 Excel を年度ごとに取得し CSV へ整形
10. power_plants_operator: 電力調査統計 電気事業者の発電所数、出力の公開 Excel を年度ごとに取得し CSV へ整形
11. power_plants_captive: 電力調査統計 自家用発電所数、出力の公開 Excel を年度ごとに取得し CSV へ整形
12. power_generation_captive: 電力調査統計 自家用発電実績の公開 Excel を年度ごとに取得し CSV へ整形
13. dbt:        dbt ビルド
"""

import logging
from pathlib import Path

from dbt.cli.main import dbtRunner

import power_demand_operator
import power_generation
import power_generation_captive
import power_generation_operator
import power_municipality
import power_plants
import power_plants_captive
import power_plants_operator
import power_survey
import power_thermal_fuel
import total_energy
from ita import download_and_parse

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pipelines")

WORK_DIR = Path(".queria")
CSV_PATH = WORK_DIR / "meti_ita_monthly.csv"
ENERGY_CSV_PATH = WORK_DIR / "meti_energy_balance.csv"
POWER_CSV_PATH = WORK_DIR / "meti_power_demand.csv"
GENERATION_CSV_PATH = WORK_DIR / "meti_power_generation.csv"
DEMAND_OPERATOR_CSV_PATH = WORK_DIR / "meti_power_demand_operator.csv"
GENERATION_OPERATOR_CSV_PATH = WORK_DIR / "meti_power_generation_operator.csv"
MUNICIPAL_DEMAND_CSV_PATH = WORK_DIR / "meti_power_demand_municipality.csv"
REVERSE_FLOW_CSV_PATH = WORK_DIR / "meti_reverse_power_flow_municipality.csv"
PLANTS_CSV_PATH = WORK_DIR / "meti_power_plants.csv"
THERMAL_FUEL_CSV_PATH = WORK_DIR / "meti_power_thermal_fuel.csv"
PLANTS_OPERATOR_CSV_PATH = WORK_DIR / "meti_power_plants_operator.csv"
PLANTS_CAPTIVE_CSV_PATH = WORK_DIR / "meti_power_plants_captive.csv"
GENERATION_CAPTIVE_CSV_PATH = WORK_DIR / "meti_power_generation_captive.csv"


def dbt_build() -> None:
    dbt = dbtRunner()
    for cmd in (["deps"], ["run"], ["docs", "generate"]):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {cmd[0]} failed")


def main() -> None:
    WORK_DIR.mkdir(exist_ok=True)

    logger.info("1/13: ita (第３次産業活動指数 月次)")
    rows = download_and_parse(CSV_PATH)
    logger.info(f"  meti_ita_monthly.csv: {rows} rows")

    logger.info("2/13: total_energy (総合エネルギー統計 時系列表)")
    rows = total_energy.download_and_parse(ENERGY_CSV_PATH)
    logger.info(f"  meti_energy_balance.csv: {rows} rows")

    logger.info("3/13: power_survey (電力調査統計 都道府県別電力需要実績)")
    rows = power_survey.download_and_parse(POWER_CSV_PATH)
    logger.info(f"  meti_power_demand.csv: {rows} rows")

    logger.info("4/13: power_generation (電力調査統計 都道府県別発電実績)")
    rows = power_generation.download_and_parse(GENERATION_CSV_PATH)
    logger.info(f"  meti_power_generation.csv: {rows} rows")

    logger.info("5/13: power_demand_operator (電力調査統計 電力需要実績 事業者別)")
    rows = power_demand_operator.download_and_parse(DEMAND_OPERATOR_CSV_PATH)
    logger.info(f"  meti_power_demand_operator.csv: {rows} rows")

    logger.info("6/13: power_generation_operator (電力調査統計 発電実績 事業者別)")
    rows = power_generation_operator.download_and_parse(GENERATION_OPERATOR_CSV_PATH)
    logger.info(f"  meti_power_generation_operator.csv: {rows} rows")

    logger.info("7/13: power_municipality (電力調査統計 市町村別需要電力量・逆潮流量)")
    rows = power_municipality.download_and_parse(
        power_municipality.DEMAND, MUNICIPAL_DEMAND_CSV_PATH
    )
    logger.info(f"  meti_power_demand_municipality.csv: {rows} rows")
    rows = power_municipality.download_and_parse(
        power_municipality.REVERSE_FLOW, REVERSE_FLOW_CSV_PATH
    )
    logger.info(f"  meti_reverse_power_flow_municipality.csv: {rows} rows")

    logger.info("8/13: power_plants (電力調査統計 都道府県別発電所数、出力)")
    rows = power_plants.download_and_parse(PLANTS_CSV_PATH)
    logger.info(f"  meti_power_plants.csv: {rows} rows")

    logger.info("9/13: power_thermal_fuel (電力調査統計 火力発電燃料実績)")
    rows = power_thermal_fuel.download_and_parse(THERMAL_FUEL_CSV_PATH)
    logger.info(f"  meti_power_thermal_fuel.csv: {rows} rows")

    logger.info("10/13: power_plants_operator (電力調査統計 電気事業者の発電所数、出力)")
    rows = power_plants_operator.download_and_parse(PLANTS_OPERATOR_CSV_PATH)
    logger.info(f"  meti_power_plants_operator.csv: {rows} rows")

    logger.info("11/13: power_plants_captive (電力調査統計 自家用発電所数、出力)")
    rows = power_plants_captive.download_and_parse(PLANTS_CAPTIVE_CSV_PATH)
    logger.info(f"  meti_power_plants_captive.csv: {rows} rows")

    logger.info("12/13: power_generation_captive (電力調査統計 自家用発電実績)")
    rows = power_generation_captive.download_and_parse(GENERATION_CAPTIVE_CSV_PATH)
    logger.info(f"  meti_power_generation_captive.csv: {rows} rows")

    logger.info("13/13: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
