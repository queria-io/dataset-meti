## データ出典

経済産業省が公表する3つの統計を収録しています。

- [経済産業省 経済解析室](https://www.meti.go.jp/statistics/tyo/sanzi/)の第３次産業活動指数（2020年基準）。
  サービス産業の生産活動を業種別・月次の指数（2020年=100）で示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/total_energy/)の総合エネルギー統計 時系列表。
  国のエネルギー需給・電源構成・CO2排出量・エネルギー自給率を年度別に示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/electric_power/ep002/)の電力調査統計。
  小売電気事業者が供給した電力需要量と、電気事業者の発電所の発電電力量・発電所数・最大出力を
  都道府県別・月次で、需要電力量と逆潮流量を市区町村別・月次で、
  火力発電所が消費した燃料を燃料種別・月次で示します。
  需要量・発電量・発電所数・最大出力には事業者別の内訳もあります。

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

## テーブル: power_generation_by_operator

電力調査統計の統計表 2-(1)「発電実績」を、事業者×月で1レコードとした月次データです。
2016年度4月以降を収録します。原典の合計行（全事業者計）はありません。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- operator_name: 事業者名（VARCHAR、原典の表記どおり）
- is_retail: 小売電気事業者に該当するか（BOOLEAN）
- is_general_transmission_distribution: 一般送配電事業者に該当するか（BOOLEAN）
- is_transmission: 送電事業者に該当するか（BOOLEAN）
- is_distribution: 配電事業者に該当するか（BOOLEAN）
- is_specified_transmission_distribution: 特定送配電事業者に該当するか（BOOLEAN）
- is_generation: 発電事業者に該当するか（BOOLEAN）
- is_specified_wholesale: 特定卸供給事業者に該当するか（BOOLEAN）
- hydro_conventional_mwh: 水力発電所のうち一般水力（DOUBLE、MWh）
- hydro_pumped_storage_mwh: 水力発電所のうち揚水式（DOUBLE、MWh）
- hydro_mwh: 水力発電所の計（DOUBLE、MWh）
- thermal_coal_mwh: 火力発電所のうち石炭（DOUBLE、MWh）
- thermal_lng_mwh: 火力発電所のうちＬＮＧ（DOUBLE、MWh）
- thermal_oil_mwh: 火力発電所のうち石油（DOUBLE、MWh）
- thermal_lpg_mwh: 火力発電所のうちＬＰＧ（DOUBLE、MWh）
- thermal_other_gas_mwh: 火力発電所のうちその他ガス（DOUBLE、MWh）
- thermal_bituminous_mwh: 火力発電所のうち歴青質混合物（DOUBLE、MWh）
- thermal_other_mwh: 火力発電所のうちその他の燃料（DOUBLE、MWh）
- thermal_mwh: 火力発電所の計（DOUBLE、MWh）
- nuclear_mwh: 原子力発電所の発電電力量（DOUBLE、MWh）
- wind_mwh: 新エネルギー等発電所のうち風力（DOUBLE、MWh）
- solar_mwh: 新エネルギー等発電所のうち太陽光（DOUBLE、MWh）
- geothermal_mwh: 新エネルギー等発電所のうち地熱（DOUBLE、MWh）
- biomass_mwh: バイオマスを主燃料とする発電電力量（DOUBLE、MWh。再掲）
- waste_mwh: 廃棄物を主燃料とする発電電力量（DOUBLE、MWh。再掲）
- storage_battery_mwh: 新エネルギー等発電所のうち蓄電池の放電電力量（DOUBLE、MWh）
- new_energy_mwh: 新エネルギー等発電所の計（DOUBLE、MWh）
- other_mwh: その他の発電電力量（DOUBLE、MWh）
- total_mwh: 発電電力量の合計（DOUBLE、MWh）
- published_as_of: 当該月の値の公表時点（DATE）

### 利用上の注意

- 単位は MWh です。原典は 1,000kWh 表記で、値は同じです。
- **operator_name は一意のキーになりません。** 同じ事業者名が同じ月に2行並ぶことが
  8事業者・のべ66件あります（2016〜2022年度）。値が同じ2行のこともあり、その場合は
  原典の合計行に1回しか入っていません（2022年8月の戸畑共同火力株式会社で 435,978 MWh）。
  事業者名で合算すると原典の全国計より多く出ます。
- 事業者名は原典の表記のままで名寄せしていません。法人格の書き方（株式会社／(株)）や
  半角カナが年度で変わるため、同じ会社が別の文字列になる月があります
  （例: 中部電力(株) が2019年10月から 中部電力株式会社）。時系列で追うときは名寄せが要ります。
- total_mwh は hydro + thermal + nuclear + new_energy_mwh + other です。hydro_mwh は
  一般＋揚水式、thermal_mwh は燃料別7列の和、new_energy_mwh は wind + solar + geothermal +
  storage_battery の計です。内訳を合計したうえに計や total_mwh を足すと二重計上になります。
- biomass_mwh と waste_mwh は主燃料で見た火力からの再掲です。thermal_mwh にも
  new_energy_mwh にも total_mwh にも含まれません。単純に足すと二重計上になります。
- storage_battery_mwh は2023年度4月に、is_distribution と is_specified_wholesale は
  2022年度4月（電気事業法改正での区分新設）に原典へ足された列です。それ以前は NULL です。
- 原典で「α」（0より大きく1,000kWh未満）と表記されたセルは数値にできないため NULL です。
  239セルあり、2016〜2023年度に出ます。空欄のセルも NULL です。
- 原典の内訳と計が合わない行があります。計だけに値があり燃料別の内訳が全て0の行
  （2022年5月 昭和電工株式会社の火力 55,206 MWh など）、逆に内訳だけに値があり計が0の行
  （2023年9月 愛知蒲郡バイオマス発電合同会社のその他燃料 26,984 MWh など）があります。
  total_mwh の恒等式が崩れる行は 159,151 行中 233 行で、うち大半は1〜5 MWh の丸めです。
  いずれも原典セルを確認済みで、取り込み時の読み違いではありません。原典どおり収録しています。
- 発電電力量が負の行が25行あります（2018年7月 太平洋セメント(株) の石炭 -125 MWh など）。
  これも原典どおりです。
- 2016年度の4月・5月には原典に合計行がありません。他の119か月では、事業者の行を合計した値が
  原典の合計行と一致します（上記の重複掲載と、2022年2月の新エネルギー等の計の 37 MWh を除く）。
- power_generation_by_prefecture（統計表 2-(2)）は同じ発電実績を都道府県別に集計したものです。
  こちらは事業者別で、火力の燃料別内訳と水力の揚水式内訳を持つ一方、地域の内訳はありません。
  事業者と都道府県を突き合わせる鍵は原典にないので、2つの表を結合することはできません。
- 値は後から改定されます。published_as_of がその月の値の公表時点です（2016年度の全月と
  2017年度の前半は原典に記載が無く NULL）。年度計のシートは取り込んでいません。
- 2015年度以前は旧 Excel 形式での配布のため収録していません。

## テーブル: power_plants_by_prefecture

電力調査統計の統計表 1-(2)「都道府県別発電所数、出力」を、都道府県×月で1レコードとした
月次データです。2019年度4月以降を収録します。47都道府県のみで、全国計の行はありません。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- pref_code: 都道府県コード（VARCHAR、全国地方公共団体コード 2 桁）
- pref_name: 都道府県名（VARCHAR）
- hydro_plants: 水力発電所の発電所数（INTEGER）
- hydro_capacity_kw: 水力発電所の最大出力計（DOUBLE、kW）
- thermal_plants: 火力発電所の発電所数（INTEGER）
- thermal_capacity_kw: 火力発電所の最大出力計（DOUBLE、kW）
- nuclear_plants: 原子力発電所の発電所数（INTEGER）
- nuclear_capacity_kw: 原子力発電所の最大出力計（DOUBLE、kW）
- wind_plants: 新エネルギー等発電所のうち風力の発電所数（INTEGER）
- wind_capacity_kw: 新エネルギー等発電所のうち風力の最大出力計（DOUBLE、kW）
- solar_plants: 新エネルギー等発電所のうち太陽光の発電所数（INTEGER）
- solar_capacity_kw: 新エネルギー等発電所のうち太陽光の最大出力計（DOUBLE、kW）
- geothermal_plants: 新エネルギー等発電所のうち地熱の発電所数（INTEGER）
- geothermal_capacity_kw: 新エネルギー等発電所のうち地熱の最大出力計（DOUBLE、kW）
- biomass_plants: バイオマスを主燃料とする発電所数（INTEGER、再掲）
- biomass_capacity_kw: バイオマスを主燃料とする発電所の最大出力計（DOUBLE、kW。再掲）
- waste_plants: 廃棄物を主燃料とする発電所数（INTEGER、再掲）
- waste_capacity_kw: 廃棄物を主燃料とする発電所の最大出力計（DOUBLE、kW。再掲）
- storage_battery_plants: 新エネルギー等発電所のうち蓄電池の設備数（INTEGER）
- storage_battery_capacity_kw: 新エネルギー等発電所のうち蓄電池の最大出力計（DOUBLE、kW）
- new_energy_plants: 新エネルギー等発電所の計（INTEGER）
- new_energy_capacity_kw: 新エネルギー等発電所の最大出力計（DOUBLE、kW）
- other_plants: その他の発電所数（INTEGER）
- other_capacity_kw: その他の発電所の最大出力計（DOUBLE、kW）
- total_plants: 発電所数の合計（INTEGER）
- total_capacity_kw: 最大出力計の合計（DOUBLE、kW）
- published_as_of: 当該月の値の公表時点（DATE）

### 利用上の注意

- 最大出力の単位は kW です。発電実績（power_generation_by_prefecture）は MWh なので、
  設備あたりの発電量を出すときは単位を揃えてください。
- 発電所数と最大出力は数え方が違います。一つの発電所に電源種別の異なる発電機がある場合、
  発電所数は最大出力が最大となる種別にだけ計上され、最大出力は種別ごとに計上されます
  （原典の備考）。種別ごとの発電所数を足しても発電所の実数にはなりません。
- total_plants / total_capacity_kw は 水力＋火力＋原子力＋新エネルギー等の計＋その他 です。
  new_energy_* は 風力＋太陽光＋地熱＋蓄電池 の計です。種別を合計したうえに計や total を
  足すと二重計上になります。
- biomass_* と waste_* は主燃料で見た火力発電所からの再掲です。new_energy_* にも total_* にも
  含まれません。再生可能エネルギーの設備量を出すときにこれらを単純に足すと二重計上になります。
- storage_battery_* は2023年度4月に原典へ足された列です。それ以前の年度は NULL になります。
- 原典の側で計・合計と内訳の和が一致しない行があります。発電所数で28行（最大5か所のずれ）、
  最大出力で42行（1kW 超のずれ。最大 107,650kW）、丸め程度（1kW 以下）のずれが192行あり、
  85か月のうち20か月に散っています。原典のセルを直接確認したうえで原典どおり収録しています。
- 2026年4月分は原典の側で都道府県の行がずれています。玄海（佐賀県）と川内（鹿児島県）の
  原子力発電所が、それぞれ長崎県・沖縄県の行に入っています（発電実績の同じ月にも同じずれが
  あります）。原子力を県別に見るときはこの月を除くか、原典の訂正を待ってください。
- 都道府県×月の粒度と pref_code は power_generation_by_prefecture・power_demand_by_prefecture と
  共通なので、year_month + pref_code で突き合わせられます。ただし発電実績が2016年度から
  あるのに対しこの表は2019年度からで、2018年度以前は統計表 1「電気事業者の発電所数、出力」に
  まとめられており都道府県別の内訳がありません。
- 値は後から改定されます。published_as_of がその月の値の公表時点です。この統計表は年度ごとに
  まとめて公表され直すため、同じ年度の12か月がほぼ同じ日付になります。年度計のシートは
  取り込んでいません。

## テーブル: power_plants_by_operator

電力調査統計の統計表 1-(1)「電気事業者の発電所数、出力」を、事業者×月で1レコードとした
月次データです。2019年度4月以降を収録します。原典の合計行（全事業者計）はありません。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- operator_name: 事業者名（VARCHAR、原典の表記どおり）
- is_retail: 小売電気事業者に該当するか（BOOLEAN）
- is_general_transmission_distribution: 一般送配電事業者に該当するか（BOOLEAN）
- is_transmission: 送電事業者に該当するか（BOOLEAN）
- is_distribution: 配電事業者に該当するか（BOOLEAN）
- is_specified_transmission_distribution: 特定送配電事業者に該当するか（BOOLEAN）
- is_generation: 発電事業者に該当するか（BOOLEAN）
- is_specified_wholesale: 特定卸供給事業者に該当するか（BOOLEAN）
- hydro_conventional_plants: 水力発電所のうち一般水力の発電所数（INTEGER）
- hydro_conventional_capacity_kw: 水力発電所のうち一般水力の最大出力計（DOUBLE、kW）
- hydro_pumped_storage_plants: 水力発電所のうち揚水式の発電所数（INTEGER）
- hydro_pumped_storage_capacity_kw: 水力発電所のうち揚水式の最大出力計（DOUBLE、kW）
- hydro_plants: 水力発電所の計の発電所数（INTEGER）
- hydro_capacity_kw: 水力発電所の計の最大出力計（DOUBLE、kW）
- thermal_coal_plants: 火力発電所のうち石炭の発電所数（INTEGER）
- thermal_coal_capacity_kw: 火力発電所のうち石炭の最大出力計（DOUBLE、kW）
- thermal_lng_plants: 火力発電所のうちＬＮＧの発電所数（INTEGER）
- thermal_lng_capacity_kw: 火力発電所のうちＬＮＧの最大出力計（DOUBLE、kW）
- thermal_oil_plants: 火力発電所のうち石油の発電所数（INTEGER）
- thermal_oil_capacity_kw: 火力発電所のうち石油の最大出力計（DOUBLE、kW）
- thermal_lpg_plants: 火力発電所のうちＬＰＧの発電所数（INTEGER）
- thermal_lpg_capacity_kw: 火力発電所のうちＬＰＧの最大出力計（DOUBLE、kW）
- thermal_other_gas_plants: 火力発電所のうちその他ガスの発電所数（INTEGER）
- thermal_other_gas_capacity_kw: 火力発電所のうちその他ガスの最大出力計（DOUBLE、kW）
- thermal_bituminous_plants: 火力発電所のうち歴青質混合物の発電所数（INTEGER）
- thermal_bituminous_capacity_kw: 火力発電所のうち歴青質混合物の最大出力計（DOUBLE、kW）
- thermal_other_plants: 火力発電所のうちその他の燃料の発電所数（INTEGER）
- thermal_other_capacity_kw: 火力発電所のうちその他の燃料の最大出力計（DOUBLE、kW）
- thermal_plants: 火力発電所の計の発電所数（INTEGER）
- thermal_capacity_kw: 火力発電所の計の最大出力計（DOUBLE、kW）
- nuclear_plants: 原子力発電所の発電所数（INTEGER）
- nuclear_capacity_kw: 原子力発電所の最大出力計（DOUBLE、kW）
- wind_plants: 新エネルギー等発電所のうち風力の発電所数（INTEGER）
- wind_capacity_kw: 新エネルギー等発電所のうち風力の最大出力計（DOUBLE、kW）
- solar_plants: 新エネルギー等発電所のうち太陽光の発電所数（INTEGER）
- solar_capacity_kw: 新エネルギー等発電所のうち太陽光の最大出力計（DOUBLE、kW）
- geothermal_plants: 新エネルギー等発電所のうち地熱の発電所数（INTEGER）
- geothermal_capacity_kw: 新エネルギー等発電所のうち地熱の最大出力計（DOUBLE、kW）
- biomass_plants: バイオマスを主燃料とする発電所の発電所数（INTEGER、再掲）
- biomass_capacity_kw: バイオマスを主燃料とする発電所の最大出力計（DOUBLE、kW。再掲）
- waste_plants: 廃棄物を主燃料とする発電所の発電所数（INTEGER、再掲）
- waste_capacity_kw: 廃棄物を主燃料とする発電所の最大出力計（DOUBLE、kW。再掲）
- storage_battery_plants: 新エネルギー等発電所のうち蓄電池の発電所数（INTEGER）
- storage_battery_capacity_kw: 新エネルギー等発電所のうち蓄電池の最大出力計（DOUBLE、kW）
- new_energy_plants: 新エネルギー等発電所の計の発電所数（INTEGER）
- new_energy_capacity_kw: 新エネルギー等発電所の計の最大出力計（DOUBLE、kW）
- other_plants: その他の発電所の発電所数（INTEGER）
- other_capacity_kw: その他の発電所の最大出力計（DOUBLE、kW）
- total_plants: 合計の発電所数（INTEGER）
- total_capacity_kw: 合計の最大出力計（DOUBLE、kW）
- published_as_of: 当該月の値の公表時点（DATE）

### 利用上の注意

- 最大出力の単位は kW です。発電実績（power_generation_by_operator）は MWh なので、
  設備あたりの発電量を出すときは単位を揃えてください。
- 発電所数と最大出力は数え方が違います。一つの発電所に電源種別の異なる発電機がある場合、
  発電所数は最大出力が最大となる種別にだけ計上され、最大出力は種別ごとに計上されます
  （原典の備考）。種別ごとの発電所数を足しても発電所の実数にはなりません。
- **operator_name は一意のキーになりません。** 同じ事業者名が同じ月に2行並ぶ組み合わせが
  30 件あります。事業者名は原典の表記のままで名寄せしていません。法人格の書き方
  （株式会社／(株)）や半角カナが年度で変わるため、同じ会社が別の文字列になる月があります。
  時系列で追うときは名寄せが要ります。2026年4月には、原典が事業者名の欄に法人番号
  （7100001032868）を書いている行が1行あり、そのまま収録しています。
- total_* は 水力＋火力＋原子力＋新エネルギー等の計＋その他 です。hydro_* は一般＋揚水式、
  thermal_* は燃料別7列の和、new_energy_* は 風力＋太陽光＋地熱＋蓄電池 の計です。
  内訳を合計したうえに計や total_* を足すと二重計上になります。
- biomass_* と waste_* は、主に使う燃料がバイオマス・廃棄物である発電所を火力発電所の欄から
  抜き出した再掲です（原典の備考3）。thermal_* と total_* には含まれ、new_energy_* には
  含まれません。再生可能エネルギーの設備量を出すときにこれらを new_energy_* に足すのは
  正しく、thermal_* や total_* に足すと二重計上になります。
- 原典はこの2列だけ、値を〔1〕〔49,000〕のように括弧付きの文字列で書いている月があります
  （再掲であることを示す原典の記法）。取り込み時に括弧と桁区切りを外して数値にしています。
  〔　　〕のような中身の無いセルは欠測です。
- storage_battery_* は2023年度4月に、is_distribution と is_specified_wholesale は2022年度4月
  （電気事業法改正での区分新設）に原典へ足された列です。それ以前は NULL です。
- 原典の空欄は NULL です。0 と空欄が同じ表の中に混ざっており、空欄を0とみなしていません。
  total_plants が NULL の行が706行あります。
- 原典の内訳と計が合わない行があります。火力の燃料別と計で4行、新エネルギー等の内訳と計で10行、
  合計と大分類の和で8行（発電所数では6行）です。内訳だけに値があり計が空欄の行
  （2023年9月 愛知蒲郡バイオマス発電合同会社の火力その他 50,000kW など）、
  再掲のバイオマスが新エネルギー等の計に入っている行（東京発電株式会社の 1,990kW など）が
  あります。後者は備考3の再掲の位置づけとも食い違います（125,640行中50行）。
  いずれも原典セルを確認済みで、原典どおり収録しています。
- 2024年3月のシートには合計行の見出しがありません（行そのものはあり、値は入っています）。
  他の84か月では、事業者の行を合計した値が原典の合計行とおおむね一致します。一致しないのは
  3か月（2021年6月・2022年2月・2023年7月。最大は2022年2月の火力・石油の 8,600kW）と、
  上記の括弧付きで書かれたバイオマス・廃棄物を原典の合計が数えていない5か月です。
- power_plants_by_prefecture（統計表 1-(2)）は同じ発電所数・最大出力を都道府県別に集計した
  ものです。こちらは事業者別で、火力の燃料別内訳と水力の揚水式内訳を持つ一方、地域の内訳は
  ありません。事業者と都道府県を突き合わせる鍵は原典にないので、2つの表を結合することは
  できません。全国計は一致します（2020年3月で 5,075 か所・太陽光 10.55GW、
  2026年3月で 12,679 か所・太陽光 18.87GW）。
- 値は後から改定されます。published_as_of がその月の値の公表時点です。この統計表は年度ごとに
  まとめて公表され直すため、同じ年度の12か月がほぼ同じ日付になります。年度計のシートは
  取り込んでいません。
- 2018年度以前は統計表 1「電気事業者の発電所数、出力」にまとまっており、この形式では
  配布されていません。

## テーブル: power_demand_by_municipality

電力調査統計の統計表 6-(1)「市町村別需要電力量」を、市区町村×月で1レコードとした
月次データです。2022年度4月から2025年3月までの36か月を収録します。
1,747市区町村のみで、全国計・都道府県計の行はありません。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- pref_code: 都道府県コード（VARCHAR、全国地方公共団体コード 2 桁）
- pref_name: 都道府県名（VARCHAR）
- municipality_name: 市区町村名（VARCHAR）
- extra_high_and_high_demand_mwh: 特別高圧／高圧の需要電力量（DOUBLE、MWh）
- low_demand_mwh: 低圧の需要電力量（DOUBLE、MWh）
- total_demand_mwh: 需要電力量の合計（DOUBLE、MWh）
- published_as_of: 当該月の値の公表時点（DATE）

## テーブル: reverse_power_flow_by_municipality

電力調査統計の統計表 6-(2)「市町村別逆潮流量」を、市区町村×月で1レコードとした
月次データです。収録範囲と市区町村の粒度は power_demand_by_municipality と同じです。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- pref_code: 都道府県コード（VARCHAR、全国地方公共団体コード 2 桁）
- pref_name: 都道府県名（VARCHAR）
- municipality_name: 市区町村名（VARCHAR）
- hydro_mwh: 水力の逆潮流量（DOUBLE、MWh）
- thermal_mwh: 火力の逆潮流量（DOUBLE、MWh）
- nuclear_mwh: 原子力の逆潮流量（DOUBLE、MWh）
- wind_mwh: 風力の逆潮流量（DOUBLE、MWh）
- geothermal_mwh: 地熱の逆潮流量（DOUBLE、MWh）
- solar_mwh: 太陽光の逆潮流量（DOUBLE、MWh）
- biomass_mwh: バイオマスの逆潮流量（DOUBLE、MWh）
- storage_battery_mwh: 蓄電池の逆潮流量（DOUBLE、MWh）
- other_mwh: その他の電源の逆潮流量（DOUBLE、MWh）
- total_mwh: 逆潮流量の合計（DOUBLE、MWh）
- published_as_of: 当該月の値の公表時点（DATE）

### 利用上の注意（市区町村別の2テーブル共通）

- 単位は MWh です。原典は 1,000kWh 表記で、値は同じです。
- 市区町村の粒度は、政令指定都市が市単位（区に分かれない）、東京都特別区が区単位です。
- 原典に市区町村コードの列がないため、市区町村名で持っています。市区町村コードを持つ
  他のデータと突き合わせるときは pref_name と municipality_name で照合してください。
- **市区町村名は都道府県の中でも一意ではありません。** 北海道に泊村が2つあります
  （古宇郡泊村と、北方領土の国後郡泊村）。year_month と pref_name と municipality_name で
  グループ化すると、この2村だけ1グループに2行入ります。
- 北方領土の6村（色丹村・泊村・留夜別村・留別村・紗那村・蘂取村）は行としては存在しますが、
  値は全期間・全項目が 0 です。
- 収録は2022年度から2024年度までの3年度分です。都道府県別の統計表（2016年度以降・毎月更新）とは
  収録範囲が違うので、同じ期間で比べられません。6-(1) は2024年度、6-(2) は2025年度が
  一覧ページの最新ですが、6-(2) の2025年度はリンクが張られているだけで実体が配信されておらず、
  取得できません。取得できなかった年度はビルドログに警告として残ります。
- power_demand_by_municipality の契約区分は「特別高圧／高圧」と「低圧」の2つです。
  都道府県別の統計表のように特別高圧と高圧には分かれていません。
  total_demand_mwh は2区分の和なので、区分を足したうえに total も足すと二重計上になります。
- 逆潮流量は発電設備から系統へ流れた電力量で、発電量そのものではありません。
  power_generation_by_prefecture の発電電力量とは別の測定です。
- storage_battery_mwh は2023年度に原典へ足された列です。2022年度は NULL になります。
- 0 ではないが単位（1,000kWh）に満たない値は、原典で「α」と記されています。数値にできないため
  NULL として収録しています。逆潮流量で 8,768 セル（電源別の列 8,517、合計 251）あり、
  そのため total_mwh も 251 行が NULL です。需要電力量に α はありません。
- 需要電力量には負の値の行があります（2022〜2024年度で4行。福島県金山町の2か月と長野県大桑村・
  鳥取県北栄町の各1か月）。原典の値がそのまま負なので、そのまま収録しています。
- 需要電力量の published_as_of は 2025-11-14 と 2025-11-20 の2つです。3か月分だけ後から
  公表されています。
- 合計と内訳の和は、原典の四捨五入により一致しないことがあります（原典の備考のとおり）。
  2022〜2024年度では、需要電力量・逆潮流量とも差が 0.5 MWh を超える行はありません。
- 年度計のシートは取り込んでいません。

## テーブル: power_thermal_fuel_by_type

電力調査統計の統計表 4「火力発電燃料実績」を、燃料種×月で1レコードとした月次データです。
2016年度4月以降を収録します。全国の値のみで、都道府県別・発電所別の内訳はありません。

- fiscal_year: 年度（INTEGER、4月始まり）
- year: 年（INTEGER、暦年）
- month: 月（INTEGER）
- year_month: 年月（VARCHAR、YYYYMM）
- fuel_name: 燃料種（VARCHAR）
- quantity_unit: 受入量・消費量・月末貯蔵量の単位（VARCHAR、t / kl / 10^3m3）
- heat_value_unit: 発熱量の単位（VARCHAR、kJ/kg / kJ/l / kJ/m3）
- receipt_quantity: 受入量（DOUBLE、単位は quantity_unit）
- consumption_quantity: 発電用の消費量（DOUBLE、単位は quantity_unit）
- consumption_dry_quantity: 乾ベースの消費量（DOUBLE、石炭・バイオマスのみ）
- heat_value: 単位量あたりの発熱量（DOUBLE、単位は heat_value_unit）
- month_end_stock_quantity: 月末貯蔵量（DOUBLE、単位は quantity_unit）
- published_as_of: 当該月の値の公表時点（DATE）

燃料種は2023年度以前が24種、2024年度以降が28種です。

| 単位 | 燃料種 |
| --- | --- |
| t | 石炭 / ＬＰＧ / ＬＮＧ / 歴青質混合物 / 廃棄物 |
| kl | Ａ重油 / Ｂ・Ｃ重油 / その他重油 / 原油 / 天然ガス液 / 軽油 / 灯油 / 廃食油 / 残渣油（アスファルト） |
| 10^3m3 | 天然ガス / ＣＯＧ / 高炉ガス / 転炉ガス / 混合ガス / 製油所ガス / 都市ガス / その他ガス |

年度によって収録される燃料種は次のとおりです。

| 燃料種 | 単位 | 収録年度 |
| --- | --- | --- |
| バイオマス | t | 2016〜2023年度 |
| その他 | t | 2016〜2023年度 |
| 木質バイオマス | t | 2024年度〜 |
| その他バイオマス | t | 2024年度〜 |
| アンモニア | t | 2024年度〜 |
| 水素 | t | 2024年度〜 |
| その他①（単位ｔ報告） | t | 2024年度〜 |
| その他②（単位ｋｌ報告） | kl | 2024年度〜 |

### 利用上の注意

- 単位は燃料種ごとに違います。quantity_unit を確認せずに燃料種をまたいで数量を合計できません。
  熱量に揃えるには heat_value（単位は heat_value_unit）を掛けます。単位の対応は
  t × kJ/kg・kl × kJ/l・10^3m3 × kJ/m3 のいずれも MJ になります。
- 石炭とバイオマスだけ、消費量が湿ベースと乾ベースの2段で公表されています。
  consumption_quantity が湿ベース、consumption_dry_quantity が乾ベースです。
  受入量と月末貯蔵量は湿ベースのみで、他の燃料種の consumption_dry_quantity は NULL です。
- 発熱量がどちらの基準の値かは、2023年度以前は原典から決まりません（湿・乾の2行にまたがる
  結合セルとして1つ置かれています）。2024年度以降は乾の行に置かれています。石炭とバイオマスの
  熱量換算は湿・乾のどちらを使うかで1割前後変わるため、派生列は持たせていません。
- 2024年度に燃料種の区分が変わりました。バイオマスが木質バイオマスとその他バイオマスに分かれ、
  アンモニアと水素が加わり、その他が単位別に2つ（その他①（単位ｔ報告）／その他②（単位ｋｌ報告））に
  なりました。2023年度以前は24種、2024年度以降は28種です。バイオマスの系列は接続しません。
- 消費量は発電用のみで、雑用に使った分は含みません（原典の備考）。
- 月末貯蔵量は振替・棚卸しによる出入りを調整した後の値です（原典の備考）。
- 合計や「計」にあたる行は原典にありません。燃料種を足しても二重計上にはなりません。
- power_generation_by_prefecture の thermal_mwh は同じ火力発電の発電量側の値ですが、
  こちらは投入した燃料の側で、粒度（全国のみ）も単位も違います。
- 値は後から改定されます。published_as_of がその月の値の公表時点です（2016年度の全月と
  2017年度の前半は原典に記載が無く NULL）。年度計のシートは取り込んでいません。
- 2015年度以前は旧 Excel 形式での配布のため収録していません。

## データ更新手順

main.py が3つの統計の公開 Excel を取得して CSV へ整形し、dbt build で各テーブルを再生成する。
時系列表のファイル名は公表年度と確報／速報で変わり、電力調査統計のファイル名は年度で命名規則が
変わる（西暦・元号・機械判読用レイアウト版）ため、いずれも統計表一覧ページからリンクを解決している。
電力調査統計は統計表ごと・年度ごとに1ファイルなので、1回のビルドで統計表数×年度数だけ取得する。
発電実績・発電所数・市町村別逆潮流量・燃料実績は列の構成や見出しが年度で変わる（発電実績・
発電所数と逆潮流量は蓄電池・配電事業者・特定卸供給事業者の列が後から足された。燃料実績は
2016年度にだけ余分な列があり、2021年4月は月末貯蔵量の見出しが年度末貯蔵量になっている）ため、
列位置ではなく見出しで対応づけている。知らない見出しが出たらそこで失敗する。
月次シートの名前も年度で揺れる（2025.4 / H28.4 / 2023年4月）ので、読み方の分からないシートは
黙って飛ばさずに失敗させている。事業者別の電力需要実績は
1シートに事業者区分ごとの表が縦に並び、区分によって見出しの段数と列数が違うため、大分類と小分類の
組み合わせで列を引いている。見出しの無い列に値があるときも失敗させ、列の読み落としに
気付けるようにしている。
統計表一覧ページに載っていても実体が配信されていないファイルがある（6-(2) の2025年度）。
そのファイルだけ飛ばして続けるが、飛ばした年度は警告としてログに残す。
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
