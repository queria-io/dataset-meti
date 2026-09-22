"""商業動態統計調査 時系列データの取得・整形。

経済産業省が公開する時系列データの Excel を取得し、ワイド形式（項目×月）の統計表を
縦持ち（項目×月の1行=1値）へ展開して CSV に保存する。

取り込むのは月次の販売額の統計表だけで、年・年度・四半期の集計表と前年比の表は使わない
（月次の実額があれば期間の集計も前年比も SQL で作れる）。

統計表ごとに列の構成も見出しの段数も違うが、次の作りは共通している:

  - 見出し行は「時間軸コード」「年月」を持つ行。その行に英語の項目名が並ぶ
  - 日本語の項目名はその 1 行上
  - 単位（10億円 / 百万円 / 店）はさらに上の行に、値を持つ列にだけ入る

そこで「時間軸コード」の位置から見出し行を探し、単位の入った列だけを値の列として拾う。
見出し行の後ろには月名・年の補助列（Month / Year）が付くが、日本語の項目名も単位も無いので
自然に外れる。拾った列が日本語の項目名のある列と一致し、かつ連続していることを確かめる。
"""

import csv
import re
from pathlib import Path

import openpyxl

from enecho import fetch_file

# 商業動態統計調査 時系列データ
BASE_URL = "https://www.meti.go.jp/statistics/tyo/syoudou/result-2/excel/"

# 業種別商業販売額（卸売業・小売業の業種別。単位 10億円）
INDUSTRY_FILE = "h2slt11j.xlsx"
INDUSTRY_SHEET = "販売額（value）(月次M)"

# 業態別の商品別販売額。百貨店・スーパーは 1 つの統計表の中でシートが業態に分かれる
BUSINESS_TYPE_SHEETS = [
    ("h2slt31j.xlsx", "合計　販売額　月次", "百貨店・スーパー"),
    ("h2slt31j.xlsx", "百貨店　販売額　月次", "百貨店"),
    ("h2slt31j.xlsx", "スーパー　販売額　月次", "スーパー"),
    ("h2slt41j.xlsx", "販売額(value)月次(Monthly)", "コンビニエンスストア"),
    ("h2slt42j.xlsx", "販売額(value)月次(Monthly)", "家電大型専門店"),
    ("h2slt43j.xlsx", "販売額(value)月次(Monthly)", "ドラッグストア"),
    ("h2slt44j.xlsx", "販売額(value)月次(Monthly)", "ホームセンター"),
]

TIME_CODE_HEADING = "時間軸コード"
YEAR_MONTH_HEADING = "年月"

# 原典の注「***」集計に必要なデータがない。「X」報告者の秘密保持のために秘匿したデータ。
# どちらも値が無いので欠測として落とす（「0」は単位未満またはゼロで、数値なのでそのまま採る）
MISSING = {"***", "X"}

UNITS = {"10億円", "百万円", "店"}
MONEY_UNITS = {"10億円", "百万円"}
ESTABLISHMENT_UNIT = "店"

_YEAR_MONTH = re.compile(r"^(\d{4})年(\d{1,2})月$")

INDUSTRY_COLUMNS = [
    "year_month",
    "industry_order",
    "industry_name",
    "industry_name_en",
    "sales_value_billion_yen",
]

BUSINESS_TYPE_COLUMNS = [
    "year_month",
    "business_type",
    "item_order",
    "item_name",
    "item_name_en",
    "sales_value_million_yen",
    "establishments",
]


def _fetch(filename: str, dest: Path) -> None:
    """統計表の Excel を取得して保存する。

    www.meti.go.jp は enecho.meti.go.jp と同じ CloudFront + WAF の下にあり、
    続けて叩くと challenge ページが返る。間隔と再取得は enecho の取得経路に任せる。
    """
    fetch_file(BASE_URL + filename, dest)


def _squash(value) -> str:
    return "" if value is None else str(value).replace("　", "").strip()


def _header_row(rows: list[tuple], sheet_name: str) -> tuple[int, int, int]:
    """見出し行の位置と、時間軸コード・年月が入る列を返す。"""
    for index, row in enumerate(rows):
        squashed = [_squash(value) for value in row]
        if TIME_CODE_HEADING in squashed and YEAR_MONTH_HEADING in squashed:
            return (
                index,
                squashed.index(TIME_CODE_HEADING),
                squashed.index(YEAR_MONTH_HEADING),
            )
    raise ValueError(f"見出し行が見つからない: {sheet_name}")


def _unit_row(rows: list[tuple], header_index: int, sheet_name: str) -> tuple:
    """単位の入った行を見出し行から上へ辿って返す。"""
    for index in range(header_index - 1, -1, -1):
        if any(_squash(value) in UNITS for value in rows[index]):
            return rows[index]
    raise ValueError(f"単位の行が見つからない: {sheet_name}")


def _value_columns(
    rows: list[tuple], header_index: int, sheet_name: str
) -> list[tuple[int, str, str, str]]:
    """値を持つ列を (列位置, 日本語名, 英語名, 単位) で返す。"""
    header = rows[header_index]
    names_ja = rows[header_index - 1]
    units = _unit_row(rows, header_index, sheet_name)

    columns = []
    named = []
    for index in range(len(header)):
        unit = _squash(units[index]) if index < len(units) else ""
        name_ja = _squash(names_ja[index]) if index < len(names_ja) else ""
        if name_ja:
            named.append(index)
        if unit not in UNITS:
            continue
        if not name_ja:
            raise ValueError(f"項目名の無い値の列がある: {sheet_name} 列{index}")
        columns.append((index, name_ja, _squash(header[index]), unit))

    if not columns:
        raise ValueError(f"値の列が見つからない: {sheet_name}")

    # 項目名のある列に単位が無いのは、原典の単位の段が変わったか、単位のセルが結合されて
    # 左上以外が読めなくなったとき。黙って列を落とすと行数が減ったまま公開まで進むので止める。
    indexes = [index for index, *_ in columns]
    if named != indexes:
        missing = sorted(set(named) - set(indexes))
        raise ValueError(f"項目名はあるが単位の無い列がある: {sheet_name} 列{missing}")
    if indexes != list(range(indexes[0], indexes[-1] + 1)):
        raise ValueError(f"値の列が連続していない: {sheet_name} 列{indexes}")
    return columns


def _year_month(time_code: str, label: str, sheet_name: str) -> str:
    """時間軸コードと年月の表記から YYYYMM を返す。

    時間軸コードは先頭 4 桁が年、末尾 2 桁が月。年月の表記と突き合わせて取り違えを防ぐ。
    """
    matched = _YEAR_MONTH.match(label)
    if not matched:
        raise ValueError(f"年月の表記が読めない: {sheet_name} {label!r}")
    year, month = int(matched.group(1)), int(matched.group(2))
    if (int(time_code[:4]), int(time_code[-2:])) != (year, month):
        raise ValueError(
            f"時間軸コードと年月が食い違う: {sheet_name} {time_code} {label}"
        )
    return f"{year}{month:02d}"


def _parse_sheet(path: Path, sheet_name: str) -> list[tuple]:
    """1 シートを (年月, 項目順, 日本語名, 英語名, 単位, 値) の行へ展開する。"""
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list(workbook[sheet_name].iter_rows(values_only=True))

    header_index, time_column, label_column = _header_row(rows, sheet_name)
    value_columns = _value_columns(rows, header_index, sheet_name)

    out: list[tuple] = []
    for row in rows[header_index + 1 :]:
        if time_column >= len(row) or _squash(row[time_column]) == "":
            continue
        year_month = _year_month(
            _squash(row[time_column]), _squash(row[label_column]), sheet_name
        )
        for order, (index, name_ja, name_en, unit) in enumerate(value_columns, start=1):
            value = row[index] if index < len(row) else None
            # 数値セルのみ採用（欠測「***」と空欄は行ごと落とす）
            if not isinstance(value, (int, float)):
                if value is not None and _squash(value) not in ({""} | MISSING):
                    raise ValueError(
                        f"想定外のセル: {sheet_name} {year_month} {value!r}"
                    )
                continue
            out.append((year_month, order, name_ja, name_en, unit, value))
    return out


def _write(csv_path: Path, columns: list[str], rows: list[tuple]) -> int:
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    return len(rows)


def download_and_parse_industry(csv_path: Path, work_dir: Path | None = None) -> int:
    """業種別商業販売額（月次）を CSV に書き出し、行数を返す。"""
    work_dir = Path(work_dir) if work_dir else csv_path.parent
    work_dir.mkdir(parents=True, exist_ok=True)

    xlsx_path = work_dir / INDUSTRY_FILE
    _fetch(INDUSTRY_FILE, xlsx_path)

    rows = []
    for year_month, order, name_ja, name_en, unit, value in _parse_sheet(
        xlsx_path, INDUSTRY_SHEET
    ):
        if unit != "10億円":
            raise ValueError(f"業種別商業販売額の単位が想定と違う: {unit}")
        rows.append((year_month, order, name_ja, name_en, value))
    return _write(csv_path, INDUSTRY_COLUMNS, rows)


def download_and_parse_business_type(
    csv_path: Path, work_dir: Path | None = None
) -> int:
    """業態別・商品別販売額（月次）を CSV に書き出し、行数を返す。"""
    work_dir = Path(work_dir) if work_dir else csv_path.parent
    work_dir.mkdir(parents=True, exist_ok=True)

    fetched: set[str] = set()
    rows = []
    for filename, sheet_name, business_type in BUSINESS_TYPE_SHEETS:
        xlsx_path = work_dir / filename
        if filename not in fetched:
            _fetch(filename, xlsx_path)
            fetched.add(filename)
        for year_month, order, name_ja, name_en, unit, value in _parse_sheet(
            xlsx_path, sheet_name
        ):
            if unit in MONEY_UNITS and unit != "百万円":
                raise ValueError(f"業態別販売額の単位が想定と違う: {unit}")
            sales = value if unit in MONEY_UNITS else None
            establishments = value if unit == ESTABLISHMENT_UNIT else None
            rows.append(
                (
                    year_month,
                    business_type,
                    order,
                    name_ja,
                    name_en,
                    sales,
                    establishments,
                )
            )
    return _write(csv_path, BUSINESS_TYPE_COLUMNS, rows)
