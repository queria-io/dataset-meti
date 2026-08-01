## データ出典

経済産業省が公表する2つの統計を収録しています。

- [経済産業省 経済解析室](https://www.meti.go.jp/statistics/tyo/sanzi/)の第３次産業活動指数（2020年基準）。
  サービス産業の生産活動を業種別・月次の指数（2020年=100）で示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/total_energy/)の総合エネルギー統計 時系列表。
  国のエネルギー需給・電源構成・CO2排出量・エネルギー自給率を年度別に示します。

## テーブル: tertiary_industry_activity_index

業種（品目）×月×系列種別を1レコードとする月次指数です。2018年1月以降を収録します。

- item_code: 品目番号（VARCHAR、例: K1D000000I = 第３次産業総合）
- item_name: 品目名称（VARCHAR、業種名）
- weight: ウエイト（DOUBLE、2020年基準の付加価値額ウエイト。第３次産業総合=10000）
- series_type: 系列種別コード（VARCHAR、seasonally_adjusted / original）
- series_type_ja: 系列種別名（VARCHAR、季節調整済指数 / 原指数）
- year_month: 年月（VARCHAR、YYYYMM）
- year: 年（INTEGER）
- month: 月（INTEGER）
- index_value: 指数値（DOUBLE、2020年＝100）

品目（item_code / item_name）は「第３次産業総合」から日本標準産業分類の大分類・中分類・
個別業種までの階層を含みます。

## テーブル: energy_balance_summary

総合エネルギー統計の時系列表を、統計表×項目×系列×年度で1レコードに展開した年度データです。
1990年度以降を収録します。全国の値のみで、地域別の内訳はありません。

- table_no: 統計表番号（INTEGER、1〜7）
- table_name: 統計表名（VARCHAR）
- item_name: 項目名（VARCHAR、エネルギー源・部門・電源等）
- item_level: 項目の階層（INTEGER、0=大項目 / 1=内訳）
- series: 系列ラベル（VARCHAR、単位または構成比・前年度比）
- value_type: 値の種類（VARCHAR、quantity=実数 / ratio=比率）
- fiscal_year: 年度（INTEGER）
- value: 値（DOUBLE）
- source_edition: 取り込んだ時系列表の版（VARCHAR、例 2024年度確報）

収録する統計表は次の7つです。

| table_no | table_name | series |
| --- | --- | --- |
| 1 | 一次エネルギー国内供給 | PJ / 原油換算万kl / 構成比 / 前年度比 |
| 2 | 最終消費(エネルギー源別) | PJ / 原油換算万kl / 構成比 / 前年度比 |
| 3 | 最終消費(部門別) | PJ / 原油換算万kl / 構成比 / 前年度比 |
| 4 | 電源構成(発電量) | 億kWh / 構成比 / 前年度比 |
| 5 | 電源構成(投入量) | PJ / 原油換算万kl / 構成比 / 前年度比 |
| 6 | CO2排出量 | Mt-CO2 / kg-CO2/kWh / 構成比 / 前年度比 |
| 7 | エネルギー自給率 | %（小数） |

### 利用上の注意

- 実数と比率が同じ value 列に入ります。table_no と series で必ず絞ってください。
- 比率（構成比・前年度比・エネルギー自給率）は小数で公表されています。0.25 は 25% を意味します。
- table_no 1・2・3・5 は PJ と原油換算万kl が同じ値の別単位表現です。両方を足すと二重計上になります。
- 合計と内訳が同じ item_name 列に並びます（item_level=0 が大項目、1 が内訳。「合計」の行もあります）。
- 再掲項目が item_level=0 に混ざります。電源構成の「ゼロエミッション電源」は原子力・水力・太陽光・
  風力・地熱・バイオマスの再掲、CO2排出量の「（参考）電力直接排出」「（参考）電力CO2排出原単位（使用端）」も
  参考値です。大項目を単純に合計するとこれらが二重に入ります。
- 「合計」の構成比は原典に行がないため収録していません（定義上 1 です）。
- 電源構成（table_no 4・5）は2010年度以降のみです。原典の注記により、2009年度以前は自家発電の
  バイオマスが別掲されていないため、それより前の系列と接続しても連続しません。
- 最新年度は確報／速報で入れ替わります。取り込んだ版は source_edition で確認できます。
- 原典で「N/A」や空欄になっているセルは行として持ちません。

### データ更新手順

main.py が2つの公開 Excel を取得して縦持ち CSV へ整形し、dbt build で各テーブルを再生成する。
時系列表のファイル名は公表年度と確報／速報で変わるため、統計表一覧ページからリンクを解決している。
資源エネルギー庁のサイトは CloudFront + AWS WAF の challenge action で保護されており、短時間に
続けて取得すると HTTP 202 と検証ページが返る。取得側は間隔を空けて取り直す。
ビルドは `bash scripts/build.sh` で実行する（Queria に公開する）。

## ライセンス

経済産業省ウェブサイトのコンテンツに準拠する[公共データ利用規約（第1.0版）（PDL1.0）](https://www.meti.go.jp/main/rules.html)に従う。

出典:

- 「第３次産業活動指数」（経済産業省）（https://www.meti.go.jp/statistics/tyo/sanzi/）を加工して作成。
- 「総合エネルギー統計」（経済産業省）（https://www.enecho.meti.go.jp/statistics/total_energy/）を加工して作成。

いずれもワイド形式の公表 Excel を縦持ちへ整形する加工を行っている。統計値そのものは改変していない。
