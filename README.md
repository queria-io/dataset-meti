## データ出典

経済産業省が公表する3つの統計を収録しています。

- [経済産業省 経済解析室](https://www.meti.go.jp/statistics/tyo/sanzi/)の第３次産業活動指数（2020年基準）。
  サービス産業の生産活動を業種別・月次の指数（2020年=100）で示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/total_energy/)の総合エネルギー統計 時系列表。
  国のエネルギー需給・電源構成・CO2排出量・エネルギー自給率を年度別に示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/electric_power/ep002/)の電力調査統計。
  小売電気事業者が供給した電力需要量と、電気事業者の発電所の発電電力量を都道府県別・月次で、
  需要電力量と逆潮流量を市区町村別・月次で示します。

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

## データ更新手順

main.py が3つの統計の公開 Excel を取得して CSV へ整形し、dbt build で各テーブルを再生成する。
時系列表のファイル名は公表年度と確報／速報で変わり、電力調査統計のファイル名は年度で命名規則が
変わる（西暦・元号・機械判読用レイアウト版）ため、いずれも統計表一覧ページからリンクを解決している。
電力調査統計は統計表ごと・年度ごとに1ファイルなので、1回のビルドで統計表数×年度数だけ取得する。
発電実績と市町村別逆潮流量は列の構成が年度で変わる（蓄電池の列は後から足された）ため、
列位置ではなく見出しで対応づけている。見出しが増減したらそこで失敗する。
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
