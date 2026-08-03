"""電力調査統計 都道府県別電力需要実績の取得・整形。

資源エネルギー庁が公表する統計表 3-(2)「都道府県別電力需要実績」の Excel を
年度ごとに取得し、都道府県×月の 1 行 = 1 レコードへ整形して CSV に保存する。

Excel は年度単位で 1 シート = 1 か月。シート内は都道府県が縦、契約区分
（特別高圧・高圧・低圧・合計）が横に並ぶ。低圧だけ特定需要（経過措置料金）と
自由料金の内訳を持つ。年度が閉じた後に「年度計」シートが足されるが、
月次の合算で再現できるうえ小売電気事業者数が「－」になるため取り込まない。

ファイル名は年度で命名規則が変わる（3-2-H28 / 3-2-2018 / 3-2-2020n）ため、
URL は統計表一覧ページから解決する。
"""

import csv
import logging
import re
from datetime import date
from pathlib import Path

import openpyxl

from enecho import fetch_file, fetch_text

logger = logging.getLogger("pipelines")

RESULTS_PATH = "/statistics/electric_power/ep002/results.html"
ARCHIVE_PATH = "/statistics/electric_power/ep002/results_archive.html"

# 統計表 3-(2) の Excel。年度ディレクトリ配下にあり、ファイル名の年表記は
# 西暦と元号が混在する。末尾 n は機械判読用レイアウト版で、伝統レイアウト版が
# 公表されていない年度（2020年度）だけこちらしか無い。
FILE_PATTERN = re.compile(
    r"/statistics/electric_power/ep002/xls/(\d{4})/(3-2-(?:\d{4}|H\d{2})n?\.xlsx)"
)

# 取り込む最も古い年度。2015年度以前は旧 Excel 形式（.xls）で配布されている。
FIRST_FISCAL_YEAR = 2016

# 月次シートの名前は「2025.4」または元号の「H28.4」。
SHEET_PATTERN = re.compile(r"^(\d{4}|H(\d{2}))\.(\d{1,2})$")

# データを持たないシート。表紙の Sheet1 と、年度が閉じた後に足される年度計。
# 年度計の名前は年度で揺れる（2018 / 28年度 / H29 / 2020年度）。
COVER_SHEET = "Sheet1"
ANNUAL_SHEET_PATTERN = re.compile(r"^[HR]?\d{2,4}(年度)?$")

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

# 値の並びは都道府県名の列を起点とした相対位置で、伝統レイアウト（名称が先頭列）と
# 機械判読用レイアウト（時間軸コード等が前に付き名称は 4 列目）で共通している。
VALUE_OFFSETS = {
    "extra_high_demand_mwh": 1,
    "extra_high_retailers": 2,
    "high_demand_mwh": 3,
    "high_retailers": 4,
    "low_demand_mwh": 5,
    "low_regulated_demand_mwh": 6,
    "low_liberalized_demand_mwh": 7,
    "low_retailers": 8,
    "total_demand_mwh": 9,
    "total_retailers": 10,
}

# 契約区分の見出し（都道府県名の列からの相対位置）。全電圧の見出しだけレイアウトで
# 呼び方が変わる。見出しがずれたら値の並びを信用しない。
HEADING_OFFSETS = {1: ("特別高圧",), 3: ("高圧",), 5: ("低圧",), 9: ("合計", "全電圧計")}

# 小売電気事業者数は整数で、需要量と桁も意味も違う。
COUNT_COLUMNS = {"extra_high_retailers", "high_retailers", "low_retailers", "total_retailers"}

OUTPUT_COLUMNS = ["year_month", "pref_code", "pref_name", *VALUE_OFFSETS, "published_as_of"]


def _squash(value: object) -> str:
    """セルの文字列から空白（全角含む）を落とす。原典は見出しに全角空白を挟む。"""
    return re.sub(r"\s|　", "", value) if isinstance(value, str) else ""


def resolve_sources() -> list[tuple[int, str]]:
    """統計表一覧ページから年度と Excel の URL を解決する。

    最新年度は results.html、過去年度は results_archive.html にある。同じ年度に
    伝統レイアウト版と機械判読用レイアウト版が並ぶ場合は伝統レイアウト版を採る
    （収録期間を通して列位置が一致しているのはこちら）。
    """
    found: dict[int, str] = {}
    for page in (ARCHIVE_PATH, RESULTS_PATH):
        for fiscal_year, filename in FILE_PATTERN.findall(fetch_text(page)):
            year = int(fiscal_year)
            if year < FIRST_FISCAL_YEAR:
                continue
            path = f"/statistics/electric_power/ep002/xls/{fiscal_year}/{filename}"
            if year in found and filename.endswith("n.xlsx"):
                continue
            found[year] = path
    if not found:
        raise RuntimeError("統計表 3-(2) のリンクが統計表一覧ページに見つからない")
    return sorted(found.items())


def _published_as_of(row: tuple) -> str | None:
    """表題行から公表時点を取り出す。2017年度以前は記載が無い。"""
    for value in row:
        if isinstance(value, str):
            matched = AS_OF_PATTERN.search(value.translate(_FULLWIDTH_DIGITS))
            if matched:
                year, month, day = (int(g) for g in matched.groups())
                return date(year, month, day).isoformat()
    return None


def _sheet_year_month(sheet_name: str) -> tuple[int, int] | None:
    """シート名を西暦の (年, 月) にする。元号表記は平成のみ（H28・H29）。"""
    matched = SHEET_PATTERN.match(sheet_name)
    if not matched:
        return None
    heisei = matched.group(2)
    year = 1988 + int(heisei) if heisei else int(matched.group(1))
    return year, int(matched.group(3))


def _name_column(rows: list[tuple], sheet_name: str) -> int:
    """都道府県名が入る列を見つける。レイアウトで先頭列か 4 列目かが変わる。"""
    for row in rows:
        for column, value in enumerate(row):
            if _squash(value) in PREFECTURE_CODES:
                return column
    raise RuntimeError(f"{sheet_name}: 都道府県名の列が見つからない")


def _check_headings(rows: list[tuple], sheet_name: str, name_column: int) -> None:
    """契約区分の見出し位置が想定どおりか確かめる。ずれたら黙って読まない。"""
    for offset, expected in HEADING_OFFSETS.items():
        column = name_column + offset
        # 見出しは結合セルで 2〜4 行目に散るため、データが始まる前の行をまとめて見る。
        found = {_squash(row[column]) for row in rows[:5] if column < len(row)}
        if not found & set(expected):
            raise RuntimeError(
                f"{sheet_name}: 列 {column} に {'/'.join(expected)} の見出しが無い"
            )


def _number(value: object) -> float | None:
    """数値セルだけを採る。「－」や空欄は欠測。"""
    return float(value) if isinstance(value, (int, float)) else None


def _parse_sheet(rows: list[tuple], sheet_name: str, year: int, month: int) -> list[tuple]:
    """1 か月のシートを都道府県ごとの行リストへ展開する。"""
    name_column = _name_column(rows, sheet_name)
    _check_headings(rows, sheet_name, name_column)
    as_of = _published_as_of(rows[0]) if rows else None
    year_month = f"{year}{month:02d}"

    out: list[tuple] = []
    for row in rows:
        name = _squash(row[name_column] if name_column < len(row) else None)
        if name not in PREFECTURE_CODES:
            continue
        values = []
        for column, offset in VALUE_OFFSETS.items():
            index = name_column + offset
            value = _number(row[index] if index < len(row) else None)
            values.append(int(value) if value is not None and column in COUNT_COLUMNS else value)
        out.append((year_month, PREFECTURE_CODES[name], name, *values, as_of))

    if len(out) != len(PREFECTURE_CODES):
        raise RuntimeError(f"{sheet_name}: 都道府県が {len(out)} 件しか読めない")
    return out


def _parse_workbook(path: Path, fiscal_year: int) -> list[tuple]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out: list[tuple] = []
    months = 0
    for sheet_name in workbook.sheetnames:
        year_month = _sheet_year_month(sheet_name)
        if year_month is None:
            # 読み方の分からないシートは黙って落とさない。月が1つ欠けても気付けなくなる。
            if sheet_name != COVER_SHEET and not ANNUAL_SHEET_PATTERN.match(sheet_name):
                raise RuntimeError(f"{fiscal_year}年度: 想定外のシート '{sheet_name}'")
            continue
        year, month = year_month
        # 年度は 4 月始まり。シート名から導いた年度がファイルの年度と食い違えば読み違い。
        if (year if month >= 4 else year - 1) != fiscal_year:
            raise RuntimeError(f"{fiscal_year}年度のファイルに {sheet_name} が入っている")
        out.extend(
            _parse_sheet(list(workbook[sheet_name].iter_rows(values_only=True)),
                         sheet_name, year, month)
        )
        months += 1
    workbook.close()
    if not months:
        raise RuntimeError(f"{fiscal_year}年度のファイルに月次シートが無い")
    return out


def download_and_parse(csv_path: Path, work_dir: Path | None = None) -> int:
    """都道府県別電力需要実績を取得・整形して CSV に書き出し、行数を返す。"""
    work_dir = Path(work_dir) if work_dir else csv_path.parent
    work_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[tuple] = []
    for fiscal_year, path in resolve_sources():
        xlsx_path = work_dir / f"power_demand_{fiscal_year}.xlsx"
        fetch_file(path, xlsx_path)
        rows = _parse_workbook(xlsx_path, fiscal_year)
        logger.info(f"  {fiscal_year}年度: {len(rows)} rows ({path})")
        all_rows.extend(rows)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(OUTPUT_COLUMNS)
        writer.writerows(all_rows)

    return len(all_rows)
