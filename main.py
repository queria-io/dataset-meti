"""経済産業省の統計の取得 + dbt ビルド。

1. ita:          第３次産業活動指数の公開 Excel を取得し縦持ち CSV へ整形（季調・原の月次）
2. total_energy: 総合エネルギー統計 時系列表の公開 Excel を取得し縦持ち CSV へ整形
3. power_survey: 電力調査統計 都道府県別電力需要実績の公開 Excel を年度ごとに取得し CSV へ整形
4. power_generation: 電力調査統計 都道府県別発電実績の公開 Excel を年度ごとに取得し CSV へ整形
5. power_thermal_fuel: 電力調査統計 火力発電燃料実績の公開 Excel を年度ごとに取得し CSV へ整形
6. dbt:          dbt ビルド
"""

import logging
from pathlib import Path

from dbt.cli.main import dbtRunner

import power_generation
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
THERMAL_FUEL_CSV_PATH = WORK_DIR / "meti_power_thermal_fuel.csv"


def dbt_build() -> None:
    dbt = dbtRunner()
    for cmd in (["deps"], ["run"], ["docs", "generate"]):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {cmd[0]} failed")


def main() -> None:
    WORK_DIR.mkdir(exist_ok=True)

    logger.info("1/6: ita (第３次産業活動指数 月次)")
    rows = download_and_parse(CSV_PATH)
    logger.info(f"  meti_ita_monthly.csv: {rows} rows")

    logger.info("2/6: total_energy (総合エネルギー統計 時系列表)")
    rows = total_energy.download_and_parse(ENERGY_CSV_PATH)
    logger.info(f"  meti_energy_balance.csv: {rows} rows")

    logger.info("3/6: power_survey (電力調査統計 都道府県別電力需要実績)")
    rows = power_survey.download_and_parse(POWER_CSV_PATH)
    logger.info(f"  meti_power_demand.csv: {rows} rows")

    logger.info("4/6: power_generation (電力調査統計 都道府県別発電実績)")
    rows = power_generation.download_and_parse(GENERATION_CSV_PATH)
    logger.info(f"  meti_power_generation.csv: {rows} rows")

    logger.info("5/6: power_thermal_fuel (電力調査統計 火力発電燃料実績)")
    rows = power_thermal_fuel.download_and_parse(THERMAL_FUEL_CSV_PATH)
    logger.info(f"  meti_power_thermal_fuel.csv: {rows} rows")

    logger.info("6/6: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
