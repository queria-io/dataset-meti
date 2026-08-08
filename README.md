## データ出典

経済産業省が公表する3つの統計を収録しています。

- [経済産業省 経済解析室](https://www.meti.go.jp/statistics/tyo/sanzi/)の第３次産業活動指数（2020年基準）。
  サービス産業の生産活動を業種別・月次の指数（2020年=100）で示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/total_energy/)の総合エネルギー統計 時系列表。
  国のエネルギー需給・電源構成・CO2排出量・エネルギー自給率を年度別に示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/electric_power/ep002/)の電力調査統計。
  小売電気事業者が供給した電力需要量と、電気事業者の発電所の発電電力量を都道府県別・月次で示します。
  電力需要量は事業者別の内訳もあります。

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

## テーブル: power_demand_by_prefecture

電力調査統計の統計表 3-(2)「都道府県別電力需要実績」を、都道府県×月で1レコードとした
月次データです。2016年度4月以降を収録します。47都道府県のみで、全国計の行はありません。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- pref_code: 都道府県コード（VARCHAR、全国地方公共団体コード 2 桁）
- pref_name: 都道府県名（VARCHAR）
- extra_high_demand_mwh: 特別高圧の電力需要量（DOUBLE、MWh）
- extra_high_retailers: 特別高圧で当該月に需要実績のある小売電気事業者数（INTEGER）
- high_demand_mwh: 高圧の電力需要量（DOUBLE、MWh）
- high_retailers: 高圧で当該月に需要実績のある小売電気事業者数（INTEGER）
- low_demand_mwh: 低圧の電力需要量（DOUBLE、MWh）
- low_regulated_demand_mwh: 低圧のうち特定需要（経過措置料金）の電力需要量（DOUBLE、MWh）
- low_liberalized_demand_mwh: 低圧のうち自由料金の電力需要量（DOUBLE、MWh）
- low_retailers: 低圧で当該月に需要実績のある小売電気事業者数（INTEGER）
- total_demand_mwh: 全電圧計の電力需要量（DOUBLE、MWh）
- total_retailers: 全電圧計で当該月に需要実績のある小売電気事業者数（INTEGER）
- published_as_of: 当該月の値の公表時点（DATE）

### 利用上の注意

- 需要量の単位は MWh です。原典は 1,000kWh 表記で、値は同じです。
- total_demand_mwh は extra_high + high + low です。区分別を合計したうえに total を足すと
  二重計上になります。low_regulated / low_liberalized も low_demand_mwh の内訳です。
- 末尾が retailers の列は需要量ではなく事業者の数です。区分をまたいで足せません。
  total_retailers は重複を除いた数なので、各区分の事業者数の合計より小さくなります。
- 全国計は持ちません。都道府県を合算すると原典の合計行と丸め誤差程度ずれます
  （相対誤差はおおむね 1e-5 以下）。2025年4月の低圧のみ、都道府県の合算が原典の合計行より
  約 447,000 MWh 大きく、原典の側で整合していません。
- 値は後から改定されます。published_as_of がその月の値の公表時点です。年度が閉じた後に
  公表される年度計は、改定前の月次を積んだ値になっていることがあるため取り込んでいません
  （本テーブルの月次を合算すると改定後の年度計になります）。
- 沖縄県の特定需要には高圧が一部含まれる、という注記が原典にあります。
- 2015年度以前は旧 Excel 形式での配布のため収録していません。

## テーブル: power_generation_by_prefecture

電力調査統計の統計表 2-(2)「都道府県別発電実績」を、都道府県×月で1レコードとした
月次データです。2016年度4月以降を収録します。47都道府県のみで、全国計の行はありません。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- pref_code: 都道府県コード（VARCHAR、全国地方公共団体コード 2 桁）
- pref_name: 都道府県名（VARCHAR）
- hydro_mwh: 水力発電所の発電電力量（DOUBLE、MWh）
- thermal_mwh: 火力発電所の発電電力量（DOUBLE、MWh）
- nuclear_mwh: 原子力発電所の発電電力量（DOUBLE、MWh）
- wind_mwh: 新エネルギー等発電所のうち風力の発電電力量（DOUBLE、MWh）
- solar_mwh: 新エネルギー等発電所のうち太陽光の発電電力量（DOUBLE、MWh）
- geothermal_mwh: 新エネルギー等発電所のうち地熱の発電電力量（DOUBLE、MWh）
- biomass_mwh: バイオマスを主燃料とする発電電力量（DOUBLE、MWh。再掲）
- waste_mwh: 廃棄物を主燃料とする発電電力量（DOUBLE、MWh。再掲）
- storage_battery_mwh: 新エネルギー等発電所のうち蓄電池の放電電力量（DOUBLE、MWh）
- new_energy_mwh: 新エネルギー等発電所の計（DOUBLE、MWh）
- other_mwh: その他の発電電力量（DOUBLE、MWh）
- total_mwh: 発電電力量の合計（DOUBLE、MWh）
- published_as_of: 当該月の値の公表時点（DATE）

### 利用上の注意

- 単位は MWh です。原典は 1,000kWh 表記で、値は同じです。
- total_mwh は hydro + thermal + nuclear + new_energy_mwh + other です。new_energy_mwh は
  wind + solar + geothermal + storage_battery の計です。種別を合計したうえに計や total_mwh を
  足すと二重計上になります。
- biomass_mwh と waste_mwh は主燃料で見た再掲です。new_energy_mwh にも total_mwh にも
  含まれません（発電量としては火力等の中に入っています）。再生可能エネルギーの発電量を
  出すときにこれらを単純に足すと二重計上になります。
- storage_battery_mwh は2023年度4月に原典へ足された列です。それ以前の年度は NULL になります。
- 発電量と power_demand_by_prefecture の需要量は別の統計表です。同じ pref_code と year_month で
  突き合わせられますが、発電した都道府県と消費した都道府県は送電により一致しません。
  差を県内の過不足として読むことはできません。
- 全国計は持ちません。都道府県ごとの内訳を足した値が原典の合計セルと丸め誤差程度ずれる行が
  2016年度に7件あります（最大 2.3 MWh。原典の合計セルが整数に丸められているためです）。
- 2026年4月分は原典の側で都道府県の行がずれています。玄海（佐賀県）と川内（鹿児島県）の
  原子力の発電量が、それぞれ長崎県・沖縄県の行に入っています（機械判読用レイアウト版でも
  都道府県コード42・47として同じ値が入っており、取り込み時の読み違いではありません）。
  他の120か月には同じずれはありません。原典どおりに収録しているので、原子力を県別に見るときは
  この月を除くか、原典の訂正を待ってください。
- 値は後から改定されます。published_as_of がその月の値の公表時点です（2016年度の全月と
  2017年度の前半は原典に記載が無く NULL）。年度計のシートは取り込んでいません。
- 2015年度以前は旧 Excel 形式での配布のため収録していません。

## テーブル: power_demand_by_operator

電力調査統計の統計表 3-(1)「電力需要実績」を、事業者×月で1レコードとした月次データです。
2016年度4月以降を収録します（毎月のビルドで伸びます）。原典は1シートに事業者区分ごとの
2つの表を並べており、operator_category がその区分です。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- operator_category: 事業者区分コード（VARCHAR、deemed_retailer / other_retailer）
- operator_category_ja: 事業者区分名（VARCHAR、みなし小売電気事業者等 / みなし小売電気事業者以外）
- operator_name: 事業者名（VARCHAR、原典の表記どおり）
- is_retail: 小売電気事業者に該当するか（BOOLEAN）
- is_general_transmission_distribution: 一般送配電事業者に該当するか（BOOLEAN）
- is_transmission: 送電事業者に該当するか（BOOLEAN）
- is_distribution: 配電事業者に該当するか（BOOLEAN）
- is_specified_transmission_distribution: 特定送配電事業者に該当するか（BOOLEAN）
- is_generation: 発電事業者に該当するか（BOOLEAN）
- is_specified_wholesale: 特定卸供給事業者に該当するか（BOOLEAN）
- liberalized_demand_mwh: その他需要（自由料金）の計（DOUBLE、MWh）
- liberalized_extra_high_demand_mwh: 自由料金のうち特別高圧（DOUBLE、MWh）
- liberalized_high_demand_mwh: 自由料金のうち高圧（DOUBLE、MWh）
- liberalized_low_demand_mwh: 自由料金のうち低圧の計（DOUBLE、MWh）
- liberalized_low_lighting_demand_mwh: 自由料金の低圧のうち電灯（DOUBLE、MWh）
- liberalized_low_power_demand_mwh: 自由料金の低圧のうち電力（DOUBLE、MWh）
- regulated_demand_mwh: 特定需要（経過措置料金）の計（DOUBLE、MWh）
- regulated_lighting_demand_mwh: 経過措置料金のうち電灯（DOUBLE、MWh）
- regulated_power_demand_mwh: 経過措置料金のうち電力（DOUBLE、MWh）
- last_resort_supply_mwh: 最終保障供給（DOUBLE、MWh）
- remote_island_supply_mwh: 離島供給（DOUBLE、MWh）
- total_demand_mwh: 合計（DOUBLE、MWh）
- published_as_of: 当該月の値の公表時点（DATE）

### 利用上の注意

- 需要量の単位は MWh です。原典は 1,000kWh 表記で、値は同じです。
- 区分によって持つ列が違います。みなし小売電気事業者以外（other_retailer）の表は自由料金の
  6列しか原典に無いため、regulated_*・last_resort_supply_mwh・remote_island_supply_mwh・
  total_demand_mwh は NULL になります。区分をまたいで需要量を合計するときは
  liberalized_demand_mwh を使ってください（total_demand_mwh を合計すると
  みなし小売電気事業者以外の分が落ちます）。
- total_demand_mwh は liberalized + regulated + last_resort + remote_island です。
  liberalized_demand_mwh は特別高圧＋高圧＋低圧計、低圧計は電灯＋電力です。
  内訳を合計したうえに計や合計を足すと二重計上になります。
- operator_name は月内でも一意ではありません。同じ区分に同じ名前の行が並ぶ月が97件あります
  （岐阜電力(株) 54か月、日本瓦斯株式会社 24か月、熊本電力(株) 14か月ほか）。
  表記も年度で変わります（(株)○○ → ○○株式会社）。名寄せはしていないので、事業者名で
  集計すると重複します。
- is_distribution は2022年4月に原典へ足された欄ですが、収録範囲では該当する行が1件もありません
  （配電事業者の需要実績がまだ無いためです）。それ以前の年度は欄そのものが無いので NULL です。
- 原典の「α」（備考どおり 0.5MWh 未満の値）は数値にできないため NULL にしています。空欄も
  NULL です。合計を出すときは NULL を 0 とみなすことになる点に注意してください。
- 原典の側で計と内訳が合わない行があります。自由料金の計と電圧別の和が 1 MWh を超えてずれる行が
  107件、低圧計と電灯＋電力がずれる行が142件あり、ほとんどは数 MWh の丸めです。大きいものは
  2019年4月の東京ガス(株)で、低圧計が電灯＋電力より 27,000 MWh 大きく（自由料金の計とも
  合いません）、桁の取り違えとみられます。内訳が空欄なのに計に値がある行もあります
  （2024年2月の株式会社いなしきエナジーの高圧など）。いずれも原典どおりに収録しています。
- 需要量が負の行が1件あります（2025年4月の東京電力パワーグリッド株式会社。高圧 -17,104 MWh）。
  過去分の訂正が当月に入ったものとみられます。原典どおりに収録しています。
- 原典の合計行（区分ごとの総計）は持ちません。事業者を合算した値は原典の合計行と
  丸めの範囲で一致しますが、α を NULL にしている分だけわずかに小さくなります。
  2017年3月のみなし小売電気事業者以外の低圧電灯のように、原典の合計行そのものが
  内訳の和と合っていない月もあります。
- 都道府県別の power_demand_by_prefecture とは同じ電力調査統計の別表です。粒度が
  事業者と都道府県で違い、契約区分の切り方も違う（本表は自由料金と経過措置料金が先で、
  電圧はその内訳）ため、列を対応づけて突き合わせることはできません。
- 値は後から改定されます。published_as_of がその月の値の公表時点です。年度計のシートは
  取り込んでいません。
- 2015年度以前は旧 Excel 形式での配布のため収録していません。

## データ更新手順

main.py が3つの統計の公開 Excel を取得して CSV へ整形し、dbt build で各テーブルを再生成する。
時系列表のファイル名は公表年度と確報／速報で変わり、電力調査統計のファイル名は年度で命名規則が
変わる（西暦・元号・機械判読用レイアウト版）ため、いずれも統計表一覧ページからリンクを解決している。
電力調査統計は統計表ごと・年度ごとに1ファイルなので、1回のビルドで統計表数×年度数だけ取得する。
発電実績は列の構成が年度で変わる（蓄電池の列は後から足された）ため、列位置ではなく見出しで
対応づけている。見出しが増減したらそこで失敗する。事業者別の電力需要実績は1シートに
事業者区分ごとの表が縦に並び、区分によって見出しの段数と列数が違うため、大分類と小分類の
組み合わせで列を引いている。見出しの無い列に値があればそこで失敗する。
資源エネルギー庁のサイトは CloudFront + AWS WAF の challenge action で保護されており、短時間に
続けて取得すると HTTP 202 と検証ページが返る。取得側は間隔を空けて取り直す。
ビルドは `bash scripts/build.sh` で実行する（Queria に公開する）。

## ライセンス

経済産業省ウェブサイトのコンテンツに準拠する[公共データ利用規約（第1.0版）（PDL1.0）](https://www.meti.go.jp/main/rules.html)に従う。

出典:

- 「第３次産業活動指数」（経済産業省）（https://www.meti.go.jp/statistics/tyo/sanzi/）を加工して作成。
- 「総合エネルギー統計」（経済産業省）（https://www.enecho.meti.go.jp/statistics/total_energy/）を加工して作成。
- 「電力調査統計」（経済産業省）（https://www.enecho.meti.go.jp/statistics/electric_power/ep002/）を加工して作成。

いずれも公表 Excel の表形式を機械可読な行へ整形する加工を行っている。統計値そのものは改変していない。
