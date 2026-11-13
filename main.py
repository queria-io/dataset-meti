"""経済産業省の統計の取得 + dbt ビルド。

1. ita:     第３次産業活動指数の公開 Excel を取得し縦持ち CSV へ整形（季調・原の月次）
2. syoudou: 商業動態統計調査 時系列データの公開 Excel を取得し、業種別商業販売額と
   業態別・商品別販売額の2つの CSV へ整形
3. dbt:     dbt ビルド
"""

import logging
from pathlib import Path

from dbt.cli.main import dbtRunner

import syoudou
from ita import download_and_parse

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pipelines")

WORK_DIR = Path(".queria")
CSV_PATH = WORK_DIR / "meti_ita_monthly.csv"
COMMERCIAL_SALES_INDUSTRY_CSV_PATH = WORK_DIR / "meti_commercial_sales_industry.csv"
RETAIL_SALES_BUSINESS_TYPE_CSV_PATH = WORK_DIR / "meti_retail_sales_business_type.csv"


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

    logger.info("2/3: syoudou (商業動態統計調査 時系列データ)")
    rows = syoudou.download_and_parse_industry(COMMERCIAL_SALES_INDUSTRY_CSV_PATH)
    logger.info(f"  meti_commercial_sales_industry.csv: {rows} rows")
    rows = syoudou.download_and_parse_business_type(RETAIL_SALES_BUSINESS_TYPE_CSV_PATH)
    logger.info(f"  meti_retail_sales_business_type.csv: {rows} rows")

    logger.info("3/3: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
