## データ出典

経済産業省が公表する3つの統計を収録しています。

- [経済産業省 経済解析室](https://www.meti.go.jp/statistics/tyo/sanzi/)の第３次産業活動指数（2020年基準）。
  サービス産業の生産活動を業種別・月次の指数（2020年=100）で示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/total_energy/)の総合エネルギー統計 時系列表。
  国のエネルギー需給・電源構成・CO2排出量・エネルギー自給率を年度別に示します。
- [経済産業省 資源エネルギー庁](https://www.enecho.meti.go.jp/statistics/electric_power/ep002/)の電力調査統計。
  小売電気事業者が供給した電力需要量と、電気事業者の発電所の発電電力量を都道府県別・月次で、
  火力発電所が消費した燃料を燃料種別・月次で示します。

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

main.py が経済産業省の公開 Excel を取得して CSV へ整形し、dbt build で各テーブルを再生成する。
時系列表のファイル名は公表年度と確報／速報で変わり、電力調査統計のファイル名は年度で命名規則が
変わる（西暦・元号・機械判読用レイアウト版）ため、いずれも統計表一覧ページからリンクを解決している。
電力調査統計は統計表ごと・年度ごとに1ファイルなので、1回のビルドで統計表数×年度数だけ取得する。
発電実績と燃料実績は列の構成や見出しが年度で変わる（発電実績は蓄電池の列が後から足された。
燃料実績は2016年度にだけ余分な列があり、2021年4月は月末貯蔵量の見出しが年度末貯蔵量になっている）
ため、列位置ではなく見出しで対応づけている。知らない見出しが出たらそこで失敗する。
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
