"""行政事業レビューのシートが「関係する計画・通知等」に挙げる、経済産業省のサイトの PDF をページごとの本文にする。

経済産業省のサイトは通常の HTTP クライアントからの取得を受け付けないので、統計の Excel と同じ
fetch.py の取得関数で PDF を取得する。URL の収集と Parquet 化は shared/review_plans.py。

出典: 行政事業レビュー見える化サイト https://rssystem.go.jp 、経済産業省ウェブサイトの各資料
"""

from pathlib import Path

from fetch import fetch_pdf
from shared import review_plans

USER_AGENT = "queria-dataset-meti (+https://queria.io/)"
HOSTS = {"www.meti.go.jp"}
PDF_DIR = Path("data/plans")
PARQUET_DIR = Path("data/parquet")


def download_plans() -> None:
    review_plans.download_plans(
        HOSTS, user_agent=USER_AGENT, pdf_dir=PDF_DIR, fetch=fetch_pdf
    )


def build_plans_parquet() -> None:
    review_plans.build_plans_parquet(
        user_agent=USER_AGENT, pdf_dir=PDF_DIR, parquet_dir=PARQUET_DIR
    )
