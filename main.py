"""経済産業省の統計の取得 + dbt ビルド。

1. ita:          第３次産業活動指数の公開 Excel を取得し縦持ち CSV へ整形（季調・原の月次）
2. total_energy: 総合エネルギー統計 時系列表の公開 Excel を取得し縦持ち CSV へ整形
3. dbt:          dbt ビルド
"""

import logging
from pathlib import Path

from dbt.cli.main import dbtRunner

import total_energy
from ita import download_and_parse

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pipelines")

WORK_DIR = Path(".queria")
CSV_PATH = WORK_DIR / "meti_ita_monthly.csv"
ENERGY_CSV_PATH = WORK_DIR / "meti_energy_balance.csv"


def dbt_build() -> None:
    dbt = dbtRunner()
    for cmd in (["deps"], ["run"], ["docs", "generate"]):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {cmd[0]} failed")


def main() -> None:
    WORK_DIR.mkdir(exist_ok=True)

    logger.info("1/3: ita (第３次産業活動指数 月次)")
    rows = download_and_parse(CSV_PATH)
    logger.info(f"  meti_ita_monthly.csv: {rows} rows")

    logger.info("2/3: total_energy (総合エネルギー統計 時系列表)")
    rows = total_energy.download_and_parse(ENERGY_CSV_PATH)
    logger.info(f"  meti_energy_balance.csv: {rows} rows")

    logger.info("3/3: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
