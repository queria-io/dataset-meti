"""電力調査統計の統計表に共通する取得・読み取りの部品。

資源エネルギー庁の統計表は表番号ごとに Excel が分かれるが、配布のされ方は共通で、
年度単位のファイルに 1 シート = 1 か月が並ぶ。ファイル名の年表記は西暦と元号が混在し、
年度が閉じた後には年度計のシートが足される。
"""

import re
from datetime import date

from enecho import fetch_text

RESULTS_PATH = "/statistics/electric_power/ep002/results.html"
ARCHIVE_PATH = "/statistics/electric_power/ep002/results_archive.html"

# 取り込む最も古い年度。2015年度以前は旧 Excel 形式（.xls）で配布されている。
FIRST_FISCAL_YEAR = 2016

# 月次シートの名前は「2025.4」または元号の「H28.4」。統計表 1-(1) の2023年度だけ
# 「2023年4月」と書かれているので、区切りと末尾の「月」も許す。
SHEET_PATTERN = re.compile(r"^(\d{4}|H(\d{2}))[.年](\d{1,2})月?$")

# データを持たないシート。表紙の Sheet1 と、年度が閉じた後に足される年度計。
# 年度計の名前は統計表と年度で揺れる
# （2018 / 28年度 / H29 / H29集計 / 2020年度 / 年度 / 年度計 / 2023年度集計）。
COVER_SHEET = "Sheet1"
ANNUAL_SHEET_PATTERN = re.compile(
    r"^[HR]?\d{2,4}$|^[HR]?\d{0,4}年度(?:集計|計)?$|^[HR]?\d{0,4}集計$"
)

# 公表時点（例「２０２６年７月１日公表時点」）。全角数字を半角へ寄せてから照合する。
AS_OF_PATTERN = re.compile(r"(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日")
_FULLWIDTH_DIGITS = str.maketrans("０１２３４５６７８９", "0123456789")

# 全国地方公共団体コード（都道府県コード 2 桁）。原典は都道府県名だけを持つ。
PREFECTURE_CODES = {
    "北海道": "01", "青森県": "02", "岩手県": "03", "宮城県": "04", "秋田県": "05",
    "山形県": "06", "福島県": "07", "茨城県": "08", "栃木県": "09", "群馬県": "10",
    "埼玉県": "11", "千葉県": "12", "東京都": "13", "神奈川県": "14", "新潟県": "15",
    "富山県": "16", "石川県": "17", "福井県": "18", "山梨県": "19", "長野県": "20",
    "岐阜県": "21", "静岡県": "22", "愛知県": "23", "三重県": "24", "滋賀県": "25",
    "京都府": "26", "大阪府": "27", "兵庫県": "28", "奈良県": "29", "和歌山県": "30",
    "鳥取県": "31", "島根県": "32", "岡山県": "33", "広島県": "34", "山口県": "35",
    "徳島県": "36", "香川県": "37", "愛媛県": "38", "高知県": "39", "福岡県": "40",
    "佐賀県": "41", "長崎県": "42", "熊本県": "43", "大分県": "44", "宮崎県": "45",
    "鹿児島県": "46", "沖縄県": "47",
}

_page_cache: dict[str, str] = {}


def squash(value: object) -> str:
    """セルの文字列から空白（全角含む）を落とす。原典は見出しに全角空白を挟む。"""
    return re.sub(r"\s|　", "", value) if isinstance(value, str) else ""


def number(value: object) -> float | None:
    """数値セルだけを採る。「－」や空欄は欠測。"""
    return float(value) if isinstance(value, (int, float)) else None


def _page(path: str) -> str:
    """統計表一覧ページ。表番号ごとに読むので取得は 1 回に抑える。"""
    if path not in _page_cache:
        _page_cache[path] = fetch_text(path)
    return _page_cache[path]


def resolve_sources(table_no: str) -> list[tuple[int, str]]:
    """統計表一覧ページから年度と Excel の URL を解決する。

    ファイル名の年表記は年度で命名規則が変わる（2-2-H28 / 2-2-2018 / 3-2-2020n）ため、
    URL は組み立てずに一覧ページから拾う。最新年度は results.html、過去年度は
    results_archive.html にある。同じ年度に伝統レイアウト版と機械判読用レイアウト版
    （ファイル名末尾 n）が並ぶ場合は伝統レイアウト版を採る。
    """
    pattern = re.compile(
        r"/statistics/electric_power/ep002/xls/(\d{4})/"
        rf"({re.escape(table_no)}-(?:\d{{4}}|H\d{{2}})n?\.xlsx)"
    )
    found: dict[int, str] = {}
    for path in (ARCHIVE_PATH, RESULTS_PATH):
        for fiscal_year, filename in pattern.findall(_page(path)):
            year = int(fiscal_year)
            if year < FIRST_FISCAL_YEAR:
                continue
            if year in found and filename.endswith("n.xlsx"):
                continue
            found[year] = f"/statistics/electric_power/ep002/xls/{fiscal_year}/{filename}"
    if not found:
        raise RuntimeError(f"統計表 {table_no} のリンクが統計表一覧ページに見つからない")
    return sorted(found.items())


def published_as_of(row: tuple) -> str | None:
    """表題行から公表時点を取り出す。2017年度以前は記載が無い。"""
    for value in row:
        if isinstance(value, str):
            matched = AS_OF_PATTERN.search(value.translate(_FULLWIDTH_DIGITS))
            if matched:
                year, month, day = (int(g) for g in matched.groups())
                return date(year, month, day).isoformat()
    return None


def sheet_year_month(sheet_name: str) -> tuple[int, int] | None:
    """シート名を西暦の (年, 月) にする。元号表記は平成のみ（H28・H29）。"""
    matched = SHEET_PATTERN.match(sheet_name)
    if not matched:
        return None
    heisei = matched.group(2)
    year = 1988 + int(heisei) if heisei else int(matched.group(1))
    return year, int(matched.group(3))


def check_sheet(sheet_name: str, fiscal_year: int) -> tuple[int, int] | None:
    """月次シートなら (年, 月) を返す。データを持たないシートは None。

    読み方の分からないシートは黙って落とさない。月が 1 つ欠けても気付けなくなる。
    """
    year_month = sheet_year_month(sheet_name)
    if year_month is None:
        if sheet_name != COVER_SHEET and not ANNUAL_SHEET_PATTERN.match(sheet_name):
            raise RuntimeError(f"{fiscal_year}年度: 想定外のシート '{sheet_name}'")
        return None
    year, month = year_month
    # 年度は 4 月始まり。シート名から導いた年度がファイルの年度と食い違えば読み違い。
    if (year if month >= 4 else year - 1) != fiscal_year:
        raise RuntimeError(f"{fiscal_year}年度のファイルに {sheet_name} が入っている")
    return year, month
