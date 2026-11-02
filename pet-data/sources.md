# 出典一覧（sources.md）

使った全URL・取得日（すべて 2026-11-02）と、取れなかったものの分類（存在しない／非公開／取得失敗）。各Phaseの担当が作った一覧をまとめたもの。原本は logs/*_sources.md。

## 取れなかったものの早見表

| 項目 | 分類 | 理由 |
|---|---|---|
| 事務提要 平成21年度版以前（2008年度以前の内訳） | 取得失敗 | ネット上に見つからない。Wayback Machine に接続できない |
| 令和8年度版（2025年度データ） | 存在しない | 2026-11-02時点で未公表（404） |
| ペットフード協会 2013〜2022年版PDF | 取得失敗 | すべて404。2023〜2025年版の時系列表で代替 |
| 旧式の飼育頭数 2009・2011・2012年 | 取得失敗 | 報道等で見つからず |
| 狂犬病 新規登録 1997〜2004年度 | 取得失敗 | e-Statで表が見つからず |
| 業者の販売・引渡し 犬2016〜2018・2022年度、猫2016・2017年度 | 取得失敗 | 元記事が削除（404）、二次情報のみ |
| 業者の販売・死亡 犬2019年度以降の全国値 | 存在しない | 環境省は全国集計を公表せず、報道にも単年値がない |
| オークション落札価格 | 非公開 | 会員制。手数料率（8.33%＋税）のみ公開 |
| 関東・B&Bペットパーク公式サイト | 取得失敗 | 証明書エラー／503。二次サイトの値で代替 |
| fukushimagazine.com | 取得失敗 | この環境の許可ドメイン外で名前解決できず |
| コジマ公式（403）、ワンラブ・かねだい公式（特定できず）、アミーゴ公式（メンテナンス中） | 取得失敗 | — |
| ブリーダーナビ | 取得せず（規約） | 利用規約がスクレイピングを禁止 |
| IVIS・Royal Canin のページ | 取得失敗 | 403。同じ研究のPubMed抄録で代替 |
| 熊本市・札幌市の殺処分ゼロの定義 | 取得失敗 | 定義を書いた一次資料が見つからない／画像PDF |
| 猫の登録頭数 | 猫には制度がない | 狂犬病予防法の登録は犬のみ |


---

# Phase 0・5〜7（準備・計算・図・レポート）

## 親が追加で使ったURL（取得日 2026-11-02）

| 用途 | URL | 状態 |
|---|---|---|
| 東京都 致死処分の内訳（R2〜R6） | https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/2025-10-21-161638-642 | 取得（raw/zero_def/tokyo_r6.pdf） |
| 神奈川県 令和7年度 殺処分ゼロ記者発表 | https://www.pref.kanagawa.jp/docs/e8z/prs/r1526408.html | 取得 |
| 神奈川県 令和6年度 殺処分ゼロ記者発表 | https://www.pref.kanagawa.jp/docs/e8z/prs/r4181223.html | 取得 |
| 神奈川県 令和6年度 別紙1（保護・譲渡等の状況） | https://www.pref.kanagawa.jp/documents/120300/bessi1.pdf | 取得 |
| 神奈川県 令和7年度 別紙1 | https://www.pref.kanagawa.jp/documents/133795/bessi1.pdf | 取得 |
| 広島県 事務提要の殺処分3分類の定義 | https://www.pref.hiroshima.lg.jp/uploaded/attachment/412160.pdf | 取得 |
| 中央環境審議会 動物愛護部会資料（国の目標・3分類） | https://www.env.go.jp/council/content/i_10/000418138.pdf | 取得 |
| 熊本市 動物愛護（殺処分ゼロの取組） | https://www.city.kumamoto.jp/doubutuaigo/kiji00346920/index.html | 取得（定義の記載なし＝取得失敗扱い） |
| 札幌市 計画 | https://www.city.sapporo.jp/inuneko/main/documents/keikaku02-02.pdf | 取得（画像PDFで定義読めず＝取得失敗） |
| 名古屋市 動物愛護管理推進計画 | https://www.city.nagoya.jp/kenkofukushi/cmsfiles/contents/0000126/126488/03petkyouseiplan3.pdf | 取得失敗（404） |
| 青森県 動物販売業者等定期報告届出書 記載例（様式第11の2） | https://www.pref.aomori.lg.jp/soshiki/kenko/dobutu/files/20210108kisaireiteikihoukoku.pdf | 取得（raw/forms/） |
| 京都府 第一種動物取扱業の手引き | https://www.pref.kyoto.jp/doubutsu/documents/dai1doutori.pdf | 取得（raw/forms/） |
| 福岡市 定期報告書様式 | https://www.city.fukuoka.lg.jp/hofuku/dobutsukanri/life/documents/teikihoukokusyo.pdf | 取得失敗（接続不可） |
| Wayback Machine | https://web.archive.org/ | 取得失敗（この環境から接続不可） |

---

# Phase 1（環境省 事務提要）

## Phase1 sources（環境省 動物愛護管理行政事務提要 ほか）

取得日: 2026-11-02（全ファイル）。raw/env/ 以下に原本と .meta.txt。

### 一覧ページ

- 統計一覧（版の一覧）: https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu.html （H26年度版〜R07年度版の12版のみ掲載）
- 各版: gyosei-jimu_h26.html 〜 gyosei-jimu_r07.html（200）。gyosei-jimu_h17〜h25.html は 404、gyosei-jimu_r08.html も 404（2026-11-02時点で令和8年度版=FY2025データ未公開）
- dog-cat.html: https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/dog-cat.html （令和6年度 全国表＋殺処分①②③、平成16〜令和6年度 参考表）
- 旧版（H22〜H25年度版）は中央環境審議会 動物愛護部会の資料ページに掲載: https://www.env.go.jp/council/14animal/y140-27/ext.html (H22版), y140-29 (H23版), y140-36 (H24版), y140-41 (H25版)。y140-1〜50 を総当たりで確認し、該当はこの4つのみ。
- Excel版: どの版も PDF のみ（xlsx/xls/csv のリンクなし）。

### 取得ファイル（版 / ファイル / URL / HTTP）

| raw パス | URL | HTTP | 表題(council分) |
|---|---|---|---|
| council/h22/900435027.pdf | https://www.env.go.jp/council/content/i_10/900435027.pdf | 200 | 犬の引取り等の業務 [PDF	 188KB] |
| council/h22/900435028.pdf | https://www.env.go.jp/council/content/i_10/900435028.pdf | 200 | 猫の引取り等の業務 [PDF 164KB] |
| council/h22/900435032.pdf | https://www.env.go.jp/council/content/i_10/900435032.pdf | 200 | 動物取扱業の登録状況 [PDF 92KB] |
| council/h22/900435033.pdf | https://www.env.go.jp/council/content/i_10/900435033.pdf | 200 | 動物取扱業等に対する勧告、命令、罰則適用件数 [PDF 50KB] |
| council/h22/900435038.pdf | https://www.env.go.jp/council/content/i_10/900435038.pdf | 200 | 犬・猫の引取り及び負傷動物の収容状況（全国統計） [PDF 50KB] |
| council/h22/900435039.pdf | https://www.env.go.jp/council/content/i_10/900435039.pdf | 200 | 犬・猫の引取り及び負傷動物の収容状況（都道府県・政令指定都市・中核市別） [PDF 121KB] |
| council/h22/900435040.pdf | https://www.env.go.jp/council/content/i_10/900435040.pdf | 200 | 犬・ねこの引取り及び負傷動物の収容状況（全国計、昭和49年度～平成17年度） [PDF 69KB] |
| council/h22/900435042.pdf | https://www.env.go.jp/council/content/i_10/900435042.pdf | 200 | 犬の登録頭数等調査（全国計：昭和35年～平成21年度） [PDF 45KB] |
| council/h22/900435044.pdf | https://www.env.go.jp/council/content/i_10/900435044.pdf | 200 | 犬・猫の引取り等手数料及び不妊・去勢手術助成金 [PDF 216KB] |
| council/h23/900435066.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435066.pdf | 200 | 犬の引取り等の業務 [PDF 172KB] |
| council/h23/900435067.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435067.pdf | 200 | 猫の引取り等の業務 [PDF 168KB] |
| council/h23/900435071.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435071.pdf | 200 | 動物取扱業の登録状況 [PDF 71KB] |
| council/h23/900435072.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435072.pdf | 200 | 動物取扱業等に対する勧告、命令、罰則適用件数 [PDF 36KB] |
| council/h23/900435077.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435077.pdf | 200 | 犬・猫の引取り及び負傷動物の収容状況（全国統計） [PDF 42KB] |
| council/h23/900435078.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435078.pdf | 200 | 犬・猫の引取り及び負傷動物の収容状況（都道府県・政令指定都市・中核市別） [PDF 143KB] |
| council/h23/900435079.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435079.pdf | 200 | 犬・ねこの引取り及び負傷動物の収容状況（全国計、昭和49年度～平成17年度） [PDF 71KB] |
| council/h23/900435081.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435081.pdf | 200 | 犬の登録頭数等調査（全国計：昭和35年～平成22年度） [PDF 28KB] |
| council/h23/900435083.pdf | https://www.env.go.jp/council/14animal/y140-29/ext/900435083.pdf | 200 | 犬・猫の引取り等手数料及び不妊・去勢手術助成金 [PDF 210KB] |
| council/h24/900435139.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435139.pdf | 200 | 犬の引取り等の業務 [PDF 170KB] |
| council/h24/900435140.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435140.pdf | 200 | 猫の引取り等の業務 [PDF 168KB] |
| council/h24/900435144.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435144.pdf | 200 | 動物取扱業の登録状況 [PDF 50KB] |
| council/h24/900435145.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435145.pdf | 200 | 動物取扱業等に対する行政による勧告、命令、業務停止、登録取消、告発件数 [PDF 30KB] |
| council/h24/900435150.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435150.pdf | 200 | 犬・猫の引取り及び負傷動物の収容状況（全国統計） [PDF 45KB] |
| council/h24/900435151.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435151.pdf | 200 | 犬・猫の引取り及び負傷動物の収容状況（都道府県・指定都市・中核市別） [PDF 137KB] |
| council/h24/900435152.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435152.pdf | 200 | 犬・猫の引取り及び負傷動物の収容状況（全国計：昭和49年度～平成17年度） [PDF 36KB] |
| council/h24/900435154.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435154.pdf | 200 | 犬の登録頭数等調査（全国計：昭和35年～平成23年度） [PDF 36KB] |
| council/h24/900435156.pdf | https://www.env.go.jp/council/14animal/y140-36/ext/900435156.pdf | 200 | 犬・猫の引取り等手数料及び不妊・去勢手術助成金 [PDF 227KB] |
| council/h25/900434826.pdf | https://www.env.go.jp/council/14animal/ext/900434826.pdf | 200 | （１）犬の引取り等の業務 [PDF 167KB] |
| council/h25/900434827.pdf | https://www.env.go.jp/council/14animal/ext/900434827.pdf | 200 | （２）猫の引取り等の業務 [PDF 165KB] |
| council/h25/900434830.pdf | https://www.env.go.jp/council/14animal/ext/900434830.pdf | 200 | （１）動物取扱業の登録状況（総括表） [PDF 25KB] |
| council/h25/900434831.pdf | https://www.env.go.jp/council/14animal/ext/900434831.pdf | 200 | （２）動物取扱業の登録状況（都道府県・指定都市別） [PDF 45KB] |
| council/h25/900434832.pdf | https://www.env.go.jp/council/14animal/ext/900434832.pdf | 200 | （３）動物取扱業等に対する行政による勧告、命令、立入検査、業務停止、登録取消、告発件数（都道府県・指定都市・中核市） [PDF 71KB] |
| council/h25/900434838.pdf | https://www.env.go.jp/council/14animal/ext/900434838.pdf | 200 | （１）犬・猫の引取り及び負傷動物の収容状況（全国統計） [PDF 37KB] |
| council/h25/900434839.pdf | https://www.env.go.jp/council/14animal/ext/900434839.pdf | 200 | （２）参考：犬・猫の引取り及び負傷動物の収容状況（全国計：昭和49年度～平成17年度） [PDF 36KB] |
| council/h25/900434840.pdf | https://www.env.go.jp/council/14animal/ext/900434840.pdf | 200 | （３）犬・猫の引取り及び負傷動物の収容状況（都道府県・指定都市・中核市別） [PDF 105KB] |
| council/h25/900434842.pdf | https://www.env.go.jp/council/14animal/ext/900434842.pdf | 200 | 犬の登録頭数と予防注射頭数等の年次別推移（全国計：昭和35年～平成24年度）【厚生労働省衛生行政報告例より】 [PDF 37KB] |
| council/h25/900434844.pdf | https://www.env.go.jp/council/14animal/ext/900434844.pdf | 200 | 犬・猫の引取り等手数料及び不妊・去勢手術助成金 [PDF 189KB] |
| council/y140-27_ext.html | https://www.env.go.jp/council/14animal/y140-27/ext.html | 200 |  |
| council/y140-29_ext.html | https://www.env.go.jp/council/14animal/y140-29/ext.html | 200 |  |
| council/y140-36_ext.html | https://www.env.go.jp/council/14animal/y140-36/ext.html | 200 |  |
| council/y140-41_ext.html | https://www.env.go.jp/council/14animal/y140-41/ext.html | 200 |  |
| dog-cat.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/dog-cat.html | 200 |  |
| dog-cat/2_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_4_3a.pdf | 200 |  |
| dog-cat/2_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_4_3b.pdf | 200 |  |
| dog-cat/bunrui.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/bunrui.pdf | 200 |  |
| gyosei-jimu_h26.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_h26.html | 200 |  |
| gyosei-jimu_h27.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_h27.html | 200 |  |
| gyosei-jimu_h28.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_h28.html | 200 |  |
| gyosei-jimu_h29.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_h29.html | 200 |  |
| gyosei-jimu_h30.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_h30.html | 200 |  |
| gyosei-jimu_r01.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_r01.html | 200 |  |
| gyosei-jimu_r02.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_r02.html | 200 |  |
| gyosei-jimu_r03.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_r03.html | 200 |  |
| gyosei-jimu_r04.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_r04.html | 200 |  |
| gyosei-jimu_r05.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_r05.html | 200 |  |
| gyosei-jimu_r06.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_r06.html | 200 |  |
| gyosei-jimu_r07.html | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/gyosei-jimu_r07.html | 200 |  |
| h26/h26_2_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_2_2_1.pdf | 200 |  |
| h26/h26_2_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_2_2_2.pdf | 200 |  |
| h26/h26_3_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_3_1_1.pdf | 200 |  |
| h26/h26_3_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_3_1_2.pdf | 200 |  |
| h26/h26_3_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_3_1_3.pdf | 200 |  |
| h26/h26_3_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_3_4_1.pdf | 200 |  |
| h26/h26_3_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_3_4_2.pdf | 200 |  |
| h26/h26_3_4_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_3_4_3.pdf | 200 |  |
| h26/h26_3_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_3_6.pdf | 200 |  |
| h26/h26_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h26_4_2.pdf | 200 |  |
| h27/h27_2_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_2_2_1.pdf | 200 |  |
| h27/h27_2_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_2_2_2.pdf | 200 |  |
| h27/h27_3_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_1_1.pdf | 200 |  |
| h27/h27_3_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_1_2.pdf | 200 |  |
| h27/h27_3_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_1_3.pdf | 200 |  |
| h27/h27_3_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_4_1.pdf | 200 |  |
| h27/h27_3_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_4_2.pdf | 200 |  |
| h27/h27_3_4_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_4_3.pdf | 200 |  |
| h27/h27_3_4_4.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_4_4.pdf | 200 |  |
| h27/h27_3_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_3_6.pdf | 200 |  |
| h27/h27_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h27_4_2.pdf | 200 |  |
| h28/h28_2_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_2_2_1.pdf | 200 |  |
| h28/h28_2_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_2_2_2.pdf | 200 |  |
| h28/h28_3_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_1_1.pdf | 200 |  |
| h28/h28_3_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_1_2.pdf | 200 |  |
| h28/h28_3_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_1_3.pdf | 200 |  |
| h28/h28_3_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_4_1.pdf | 200 |  |
| h28/h28_3_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_4_2.pdf | 200 |  |
| h28/h28_3_4_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_4_3.pdf | 200 |  |
| h28/h28_3_4_4.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_4_4.pdf | 200 |  |
| h28/h28_3_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_3_6.pdf | 200 |  |
| h28/h28_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h28_4_2.pdf | 200 |  |
| h29/h29_2_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_2_2_1.pdf | 200 |  |
| h29/h29_2_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_2_2_2.pdf | 200 |  |
| h29/h29_3_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_3_1_1.pdf | 200 |  |
| h29/h29_3_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_3_1_2.pdf | 200 |  |
| h29/h29_3_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_3_1_3.pdf | 200 |  |
| h29/h29_3_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_3_4_1.pdf | 200 |  |
| h29/h29_3_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_3_4_2.pdf | 200 |  |
| h29/h29_3_4_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_3_4_3.pdf | 200 |  |
| h29/h29_3_4_4.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_3_4_4.pdf | 200 |  |
| h29/h29_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h29_4_2.pdf | 200 |  |
| h30/h30_2_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_2_2_1.pdf | 200 |  |
| h30/h30_2_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_2_2_2.pdf | 200 |  |
| h30/h30_3_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_3_1_1.pdf | 200 |  |
| h30/h30_3_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_3_1_2.pdf | 200 |  |
| h30/h30_3_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_3_1_3.pdf | 200 |  |
| h30/h30_3_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_3_4_1.pdf | 200 |  |
| h30/h30_3_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_3_4_2.pdf | 200 |  |
| h30/h30_3_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_3_4_3a.pdf | 200 |  |
| h30/h30_3_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_3_4_3b.pdf | 200 |  |
| h30/h30_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/h30_4_2.pdf | 200 |  |
| r01/r01_2_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_2_2_1.pdf | 200 |  |
| r01/r01_2_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_2_2_2.pdf | 200 |  |
| r01/r01_3_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_1_1.pdf | 200 |  |
| r01/r01_3_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_1_2.pdf | 200 |  |
| r01/r01_3_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_1_3.pdf | 200 |  |
| r01/r01_3_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_4_1.pdf | 200 |  |
| r01/r01_3_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_4_2.pdf | 200 |  |
| r01/r01_3_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_4_3a.pdf | 200 |  |
| r01/r01_3_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_4_3b.pdf | 200 |  |
| r01/r01_3_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_3_6.pdf | 200 |  |
| r01/r01_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r01_4_2.pdf | 200 |  |
| r02/1_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/1_2_1.pdf | 200 |  |
| r02/1_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/1_2_2.pdf | 200 |  |
| r02/2_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_1_1.pdf | 200 |  |
| r02/2_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_1_2.pdf | 200 |  |
| r02/2_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_1_3.pdf | 200 |  |
| r02/2_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_4_1.pdf | 200 |  |
| r02/2_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_4_2.pdf | 200 |  |
| r02/2_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_4_3a.pdf | 200 |  |
| r02/2_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_4_3b.pdf | 200 |  |
| r02/2_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/2_6.pdf | 200 |  |
| r02/3_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r02/3_3.pdf | 200 |  |
| r03/1_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/1_2_1.pdf | 200 |  |
| r03/1_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/1_2_2.pdf | 200 |  |
| r03/2_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_1_1.pdf | 200 |  |
| r03/2_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_1_2.pdf | 200 |  |
| r03/2_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_1_3.pdf | 200 |  |
| r03/2_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_4_1.pdf | 200 |  |
| r03/2_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_4_2.pdf | 200 |  |
| r03/2_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_4_3a.pdf | 200 |  |
| r03/2_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_4_3b.pdf | 200 |  |
| r03/2_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/2_6.pdf | 200 |  |
| r03/3_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r03/3_3.pdf | 200 |  |
| r04/1_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/1_2_1.pdf | 200 |  |
| r04/1_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/1_2_2.pdf | 200 |  |
| r04/2_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_1_1.pdf | 200 |  |
| r04/2_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_1_2.pdf | 200 |  |
| r04/2_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_1_3.pdf | 200 |  |
| r04/2_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_4_1.pdf | 200 |  |
| r04/2_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_4_2.pdf | 200 |  |
| r04/2_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_4_3a.pdf | 200 |  |
| r04/2_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_4_3b.pdf | 200 |  |
| r04/2_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/2_6.pdf | 200 |  |
| r04/3_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r04/3_3.pdf | 200 |  |
| r05/1_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/1_2_1.pdf | 200 |  |
| r05/1_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/1_2_2.pdf | 200 |  |
| r05/2_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_1_1.pdf | 200 |  |
| r05/2_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_1_2.pdf | 200 |  |
| r05/2_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_1_3.pdf | 200 |  |
| r05/2_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_4_1.pdf | 200 |  |
| r05/2_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_4_2.pdf | 200 |  |
| r05/2_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_4_3a.pdf | 200 |  |
| r05/2_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_4_3b.pdf | 200 |  |
| r05/2_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/2_6.pdf | 200 |  |
| r05/3_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r05/3_3.pdf | 200 |  |
| r06/1_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/1_2_1.pdf | 200 |  |
| r06/1_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/1_2_2.pdf | 200 |  |
| r06/2_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_1_1.pdf | 200 |  |
| r06/2_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_1_2.pdf | 200 |  |
| r06/2_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_1_3.pdf | 200 |  |
| r06/2_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_4_1.pdf | 200 |  |
| r06/2_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_4_2.pdf | 200 |  |
| r06/2_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_4_3a.pdf | 200 |  |
| r06/2_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_4_3b.pdf | 200 |  |
| r06/2_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_6.pdf | 200 |  |
| r06/2_7_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_7_1.pdf | 200 |  |
| r06/2_7_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_7_2.pdf | 200 |  |
| r06/2_7_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/2_7_3.pdf | 200 |  |
| r06/3_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r06/3_3.pdf | 200 |  |
| r07/1_2_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/1_2_1.pdf | 200 |  |
| r07/1_2_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/1_2_2.pdf | 200 |  |
| r07/2_1_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_1_1.pdf | 200 |  |
| r07/2_1_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_1_2.pdf | 200 |  |
| r07/2_1_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_1_3.pdf | 200 |  |
| r07/2_4_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_4_1.pdf | 200 |  |
| r07/2_4_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_4_2.pdf | 200 |  |
| r07/2_4_3a.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_4_3a.pdf | 200 |  |
| r07/2_4_3b.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_4_3b.pdf | 200 |  |
| r07/2_6.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_6.pdf | 200 |  |
| r07/2_7.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_7.pdf | 200 |  |
| r07/2_7_1.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_7_1.pdf | 200 |  |
| r07/2_7_2.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_7_2.pdf | 200 |  |
| r07/3_3.pdf | https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/3_3.pdf | 200 |  |

### 取れなかったもの

| 対象 | 分類 | 内容 |
|---|---|---|
| 事務提要 H21年度版以前（FY2008以前データ）の版別PDF | 存在しない（Web上に掲載なし） | env.go.jp の統計ページ・中環審資料ページ(y140-1〜50)を探索、WebSearch でも見つからず。web.archive.org は接続不可 |
| 令和8年度版（FY2025データ、2026年4月1日登録数） | 存在しない（未公開） | gyosei-jimu_r08.html, files/r08/* は 404 |
| FY2005〜2008 の引取り内訳（飼い主から/所有者不明、成熟/幼齢）・返還と譲渡の別 | 存在しない（該当版が非掲載） | 全国合計（引取り・返還譲渡・殺処分）のみ参考表で取得 |
| FY2009 の飼い主から/所有者不明の別 | 存在しない | H22年度版の表は成熟/幼齢と返還・譲渡（合算）のみ |
| 殺処分①②③ の全国公表値（FY2019〜2023） | 存在しない（PDFは①②③なし。HTMLは最新年度のみ） | 都道府県表の自治体合計で算出（区分=計算）。FY2024 は HTML 実測値と一致を確認 |
| 負傷動物の①②③（FY2023以前）、都道府県別 負傷動物表 | 未取得（R07版 2_4_3b は raw に保存のみ、未CSV化） | 全国の負傷動物 収容・返還・譲渡・殺処分は各年度取得済み |
| 行政処分 FY2008以前 | 存在しない（該当版が非掲載） | |
| 立入検査件数 FY2009〜2011 | 存在しない（表に欄なし） | H22〜H24年度版の表には立入検査欄がない |
| 動物取扱業 都道府県別 2006〜2009年 | 存在しない（該当版が非掲載） | 2010年4月1日以降のみ |
| マイクロチップ 新規登録数（年度フロー） | 存在しない（事務提要は年度末累積のみ） | 累積差（純増）を区分=計算で併記 |

---

# Phase 2（狂犬病・ペットフード協会・業者定期報告）

## Phase 2 出典一覧（取得日はすべて 2026-11-02）

各 raw ファイルの隣に `.meta.txt`（URL / 取得日 / HTTPステータス）あり。

### 3-2 狂犬病予防法
| URL | 保存先 | 結果 |
|---|---|---|
| https://www.mhlw.go.jp/bunya/kenkou/kekkaku-kansenshou10/02.html | raw/mhlw/02.html | 200 取得（昭和35年〜令和6年度） |
| https://www.e-stat.go.jp/stat-search/files?…toukei=00450027&query=狂犬病 等（検索） | — | 一覧取得（raw/mhlw/estat/list.tsv） |
| https://www.e-stat.go.jp/stat-search/file-download?statInfId=…&fileKind=1（22本） | raw/mhlw/estat/{年}_{statInfId}.csv | 200 取得: 1996, 1997(1-3月), 2005-2025年度 |
| e-Stat 1997〜2004年度の同表 | — | **取得失敗**（サイト検索で該当表が見つからない） |
| e-Stat API | — | 未使用（appId なし） |

### 3-3 ペットフード協会
| URL | 保存先 | 結果 |
|---|---|---|
| https://petfood.or.jp/data/ , https://petfood.or.jp/data-chart/ | raw/petfood/data_index.html, data-chart.html | 200（2024・2025年版のみリンク） |
| https://petfood.or.jp/pdf/data/2023/{1-13}.pdf | raw/petfood/2023/ | 200 |
| https://petfood.or.jp/pdf/data/2024/{1-13}.pdf | raw/petfood/2024/ | 200 |
| https://petfood.or.jp/pdf/data/2025/{1-16}.pdf | raw/petfood/2025/ | 200（テキスト抽出不可→画像目視） |
| https://petfood.or.jp/pdf/data/{2013-2022}/{1,2}.pdf, 2023/14-15, 2024/14-15, 2025/17-18, 2026/1-2 | raw/petfood/{年}/*.notfound.meta.txt | 404 → **存在しない（削除済み）** |
| https://petfood.or.jp/data/chart{2013,2017,2019,2020,2022}/… → /data-chart/chart{年}/… | — | 302→404 **削除済み** |
| https://petfood.or.jp/pdf/data/{2020-2025}/comment.pdf, {2020-2022}/data.pdf | raw/petfood/industry_survey/ | 200（別調査「ペットフード産業実態調査」、CSV対象外） |
| https://petfood.or.jp/topics/img/221226.pdf | raw/petfood/topics_221226.pdf(.meta) | 404 |
| https://jvma-vet.jp/mag/07612/a1.pdf | raw/petfood/secondary/jvma_07612_a1.pdf | 200（2008年 旧式 1,310万/1,089万、推計方法の変遷） |
| https://www.env.go.jp/council/14animal/y140-46/mat03.pdf | raw/petfood/secondary/env_y140-46_mat03.pdf | 200（頭数記載なし、参考） |
| 旧式値の二次出典（WebFetch/WebSearchで確認、HTML未保存）: | | |
| https://www.daily.co.jp/society/life/2017/07/20/0010388793.shtml | — | 2016年 犬987万8000・猫984万7000（WebFetch） |
| https://life.oricon.co.jp/rank_pet/news/2108002/ | — | 2017年 犬892万・猫952万6000（WebFetch） |
| https://www.nippon.com/ja/features/h00311/ | — | 2017年 前年比 −43万6000/+21万7000（WebFetch） |
| https://www.nippon.com/ja/japan-data/h00457/ | — | 2018年 犬890万3000・猫964万9000（WebFetch） |
| https://gentosha-go.com/articles/-/33598 | — | 2017-2020年 旧式値（WebFetch） |
| https://toyokeizai.net/articles/-/99906 | — | 2014・2015年 旧式値（WebFetch） |
| https://toyokeizai.net/articles/-/61018 | — | 2013年 旧式値（WebSearch 要約のみ、有料部分） |
| https://www.j-cast.com/2011/05/28092282.html | — | 2010年 旧式値（WebSearch 要約のみ） |
| https://newswitch.jp/p/28337 | — | 2020年 旧式 新規飼育 犬46.2万・猫48.3万（WebSearch 要約のみ） |
| 2009, 2011, 2012年の旧式値 | — | **取得失敗**（信頼できる出典を発見できず） |

### 3-4 業者定期報告
| URL | 保存先 | 結果 |
|---|---|---|
| https://www.pref.saitama.lg.jp/e1601/gikai-gaiyou/h2812/h080.html | raw/dealer_reports/saitama_h2812_h080.html | 200（2014年度 全国値、議会録） |
| https://www.env.go.jp/council/14animal/y140-42/900435217.pdf | raw/dealer_reports/env_y140-42_900435217.pdf | 200（2014年度 平均死亡率、環境省） |
| https://news.yahoo.co.jp/expert/articles/0769b337904858017be9497d2e7cb6cbaa0c9e40 | raw/dealer_reports/yahoo_0769b337.html | **404（記事削除）** |
| https://news.yahoo.co.jp/expert/articles/b48c0b8af86b5235ba432ac6ef387501cfb08a9b | raw/dealer_reports/yahoo_b48c0b8a.html | **404（記事削除）** |
| https://news.yahoo.co.jp/expert/authors/ohtamasahiko | raw/dealer_reports/yahoo_ohta_authors.html | **404** |
| https://eleminist.com/article/1127 | raw/dealer_reports/eleminist_1127.html | 200（2018年度 猫 約19.9万） |
| https://shueisha.online/articles/-/251539（p1-3） | raw/dealer_reports/shueisha_251539*.html | 200（14→22年度 猫89%増、回収率100%） |
| https://shueisha.online/articles/-/251540, 251542（p1-3） | raw/dealer_reports/shueisha_25154{0,2}_p*.html | 200（数値なし） |
| https://www.mimosa-ah.com/cat_topics/300/ | raw/dealer_reports/mimosa_300.html | 200（2015年度、朝日記事転載） |
| https://ameblo.jp/alma-soulmate/entry-12242393946.html | raw/dealer_reports/ameblo_12242393946.html | 200（同上 転載） |
| https://ameblo.jp/tintinpapa/entry-12586399125.html | raw/dealer_reports/ameblo_tintinpapa_12586399125.html | 200（2018年度 約2.6万、5年12万） |
| https://ameblo.jp/aidog2014/entry-12874241008.html | raw/dealer_reports/ameblo_aidog2014_12874241008.html | 200（9年累計 223,118、22年度提出率84.6%、AERA dot. 2024-11-06 転載） |
| https://takashisawaki.hatenablog.com/entry/2018/08/29/125628 | raw/dealer_reports/sawaki_20180829.html | 200（重複計上の指摘、数値なし） |
| https://pet-shop-sakura.com/dog_trivia/dog-and-cat-distribution-of-pet-industry.html | raw/dealer_reports/petshopsakura.html | 200（2014年度 約75万・2万3千、参考） |
| https://note.com/petzik_breeder_/n/n33b5c1113668 | raw/dealer_reports/note_petzik.html | 200（参考） |
| 2016年度 死亡 犬18,687・猫5,556 | — | WebSearch 要約のみ（出典記事削除）→ CSV に【未検証】で記載 |
| 2016年度 販売数、2017年度 全項目、2018年度 犬流通量、2019年度以降の犬 | — | 2016-2018: **取得失敗**／2019年度以降の犬: **存在しない**（環境省非公表、報道でも単年値なし） |

---

# Phase 3（オークション・繁殖・保護・チェーン）

## Phase 3 出典一覧（取得日はすべて 2026-11-02）

### 使用した出典
| テーマ | URL | 保存先 | 状態 |
|---|---|---|---|
| オークション | https://www.env.go.jp/press/press_02760.html | raw/auction/env_press_02760.html | 200 |
| オークション | https://www.env.go.jp/content/000199032.pdf（別添1 曜日分布） | raw/auction/env_000199032.pdf | 200 |
| オークション | https://www.env.go.jp/content/000199030.pdf（別添2 体重） | raw/auction/env_000199030.pdf | 200 |
| オークション | https://www.env.go.jp/content/000199031.pdf（参考 保険会社） | raw/auction/env_000199031.pdf | 200 |
| オークション | https://noranecolumn.com/nationalpetauction/ | raw/auction/noranecolumn_nationalpetauction.html | 200（二次） |
| オークション | https://enkara.jp/type3/ | raw/auction/enkara_type3.html | 200（二次） |
| オークション | https://www.petauction.jp/ ・ /companyprofile/ ・ /faq/ | raw/auction/petauction_*.html | 200 |
| 繁殖 | https://digitalpr.jp/r/41597 | raw/breeding/digitalpr_41597.html | 200 |
| 繁殖 | https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/210601oshirase_2 | raw/breeding/tokyo_210601oshirase_2.pdf | 200 |
| 繁殖 | https://eutils.ncbi.nlm.nih.gov/...efetch...id=28402063（犬 PubMed 抄録） | raw/breeding/pubmed_28402063_dog.txt | 200（IVIS代替） |
| 繁殖 | https://eutils.ncbi.nlm.nih.gov/...efetch...id=27807902（猫 PubMed 抄録） | raw/breeding/pubmed_27807902_cat.txt | 200（Royal Canin代替） |
| 繁殖 | https://www.env.go.jp/nature/dobutsu/aigo/2_data/pamph/rep_h1503/04.pdf | raw/breeding/env_rep_h1503_04.pdf | 200 |
| 繁殖 | https://www.dailyshincho.jp/article/2023/08301152/?all=1（**22.5%の出典**） | raw/breeding/dailyshincho_2023_08301152_all.html | 200 |
| 繁殖 | https://www.dailyshincho.jp/article/2023/10280601/?all=1 | raw/breeding/dailyshincho_2023_10280601_all.html | 200（参考） |
| 繁殖 | https://www.dailyshincho.jp/spe/petshop/ | raw/breeding/dailyshincho_spe_petshop.html | 200（記事一覧） |
| 繁殖 | https://news.livedoor.com/article/detail/24893106/ | raw/breeding/livedoor_24893106_shincho.html | 200（転載、本文削除済み） |
| 繁殖 | https://www.pet-coo.com/news/20231013/（Coo&RIKU 声明） | raw/breeding/petcoo_news_20231013.html | 200 |
| 繁殖 | https://svepm.org.uk/wp-content/uploads/2023/04/Mila.pdf | raw/breeding/svepm_Mila.pdf | 200（未使用） |
| 保護 | https://www.animaldonation.org/anidone/wp-content/uploads/2026/04/044b747ae93b88cdcd18b99b85b2a26d.pdf | raw/rescue/anidone_hakusho2025.pdf | 200 |
| 保護 | https://corp.inuneko-seikatsu.co.jp/report/report2026/ | raw/rescue/inuneko_report2026.html | 200 |
| 保護 | 同 白書PDF（corp.inuneko-seikatsu.co.jp/inunkeko_cms/wp-content/uploads/2026/09/全国-犬猫保護活動-実態白書2026_0908.pdf） | raw/rescue/inuneko_hakusho2026.pdf | 200 |
| 保護 | https://peace-winds.org/wp-content/themes/pwj2023/assets/pdf/PWJ_FY2024jp.pdf | raw/rescue/PWJ_FY2024jp.pdf | 200 |
| 保護 | https://prtimes.jp/main/html/rd/p/000000067.000064020.html | raw/rescue/prtimes_petsfirst_67.html | 200 |
| 保護 | https://www.zaikei.co.jp/releases/3200145/ | raw/rescue/zaikei_3200145.html | 200 |
| 保護 | https://www.pref.okayama.jp/uploaded/life/728325_6658346_misc.pdf | raw/rescue/okayama_728325.pdf | 200 |
| 保護 | https://www.pref.hiroshima.lg.jp/uploaded/attachment/588059.pdf（団体譲渡割合 H20〜H25） | raw/rescue/hiroshima_588059.pdf | 200（追加） |
| チェーン | https://kenseisha.com/petshop-rank/ | raw/chains/kenseisha_petshop_rank.html | 200（二次） |
| チェーン | https://japan-wanderer.com/pet-shop-chain-ranking/ | raw/chains/japanwanderer_ranking.html | 200（二次） |
| チェーン | https://www.pet-coo.com/company/ ・ /company/csr | raw/chains/cooriku_company.html, cooriku_csr.html | 200 |
| チェーン | https://report.pet-coo.com/ ・ /archives/487 ・ /archives/941（＋画像3点） | raw/chains/cooriku_report*.html/.png | 200 |
| チェーン | https://www.aeonpet.com/company/ ・ about-us/data/ ・ about-us/overview/ ・ sustainability/doubutsuaigo.html | raw/chains/aeonpet_*.html | 200 |
| チェーン | https://www.ahb.jpn.com/ ・ /company/profile ・ /company/animalwelfare | raw/chains/ahb_*.html | 200 |
| チェーン | https://pfirst.jp/company/ | raw/chains/pfirst_company.html | 200 |
| チェーン | https://job.mynavi.jp/27/pc/search/corp222914/outline.html（アミーゴ） | raw/chains/mynavi_amigo_outline.html | 200（二次） |

### 取れなかったもの
| 対象 | URL | 分類 | 内容 |
|---|---|---|---|
| 関東・B&Bペットパーク 会社概要 | https://www.kantobbpetpark.com/summary.html | 取得失敗 | curl: TLS 証明書検証エラー（http→https 301）。WebFetch: 503。検証無効化はしていない。二次値で代替 |
| 関東・B&Bペットパーク Q&A | https://kantobbpetpark.com/qa.html | 取得失敗 | 同上 |
| IVIS 講演要旨（犬 20万頭） | https://www.ivis.org/library/evc/evc-voorjaarsdagen-hague-2017/mortality-kennels-what-we-learnt-from-a-study-on-200000-puppies | 取得失敗 | Cloudflare チャレンジ 403（curl/WebFetch とも）。PubMed 抄録で代替 |
| Royal Canin Academy（猫） | https://academy.royalcanin.com/en/veterinary/epidemiological-analysis-of-reproductive-performance-and-kitten-mortality-rates | 取得失敗（保存のみ） | curl 403。WebFetch では閲覧でき数値一致を確認。保存は PubMed 抄録 |
| HAL（犬論文） | https://hal.archives-ouvertes.fr/hal-01600796 | 取得失敗 | Anubis ボット対策ページ |
| 団体譲渡の割合 記事 | https://fukushimagazine.com/?p=383 | 取得失敗 | プロキシ CONNECT 502／WebFetch DNS 解決不可（許可ドメイン外）。session のネットワーク設定で許可が必要 |
| 広島県 別資料 | https://www.pref.hiroshima.lg.jp/uploaded/attachment/130893.pdf | 存在しない | 404 |
| オークション落札価格 | — | 非公開 | 主催者・環境省とも公表なし |
| ペットの専門店コジマ 公式 | https://pets-kojima.com/ | 取得失敗 | 403 |
| ワンラブ 公式 | — | 取得失敗 | 公式ドメイン特定できず（one-love.co.jp は無関係のホスティング初期ページ） |
| かねだい 公式 | — | 取得失敗 | 公式ドメイン特定できず（kanedai.co.jp は同名の食器会社） |
| アミーゴ 公式 | https://www.amigo-pet.co.jp/ | 取得失敗 | メンテナンス中 |
| AHB 売上 | https://www.ahb.jpn.com/company/profile | 非公開 | 会社概要に記載なし |
| イオンペット 生体販売頭数・死亡率 | https://www.aeonpet.com/company/about-us/data/ | 非公開 | 記載なし |
| ピースワンコ 年間保護・譲渡頭数 | PWJ 決算書 | 非公開（決算書に無し） | 広報ページの累計値（5,700頭以上等）はPR目的のため不採用 |
| 環境省通知 2016-01-05（海外死亡率の原典） | — | 取得失敗（未探索） | Coo&RIKU 声明経由の二次値のみ |
| 犬猫生活白書2026 の犬猫別内訳 | raw/rescue/inuneko_hakusho2026.pdf | 取得失敗 | PDF の数字グリフが化けて読めない |

### 「クーリク内部資料 死亡率22.5%」の出典
- デイリー新潮 2023年8月30日配信「元従業員が告発 ペットショップ『クーアンドリク』の『ゴキブリだらけの繁殖場』で死んでいく子犬たち」（週刊新潮 2023年9月7日号）
  https://www.dailyshincho.jp/article/2023/08301152/
  本文：「21年10月のD犬率は20・2％、11月34・8％、12月30・1％。年平均22・5％とあった」
- 会社側反論：https://www.pet-coo.com/news/20231013/（資料の存在は否定、ただし当該施設で記事と同水準の月があったことは認める）

---

# Phase 4（店頭価格）

## Phase 4 sources（店頭価格）

取得日: 2026-11-02（全件）。User-Agent: `Mozilla/5.0 (research; contact via site)`。同一サイトへのリクエスト間隔 2.5 秒。

### 使ったURL

| サイト | URL | 用途 | 結果 |
|---|---|---|---|
| ペットミー | https://petmi.jp/robots.txt | クロール可否確認 | 200。Disallow は /api/, /pvt/, /shop-admin/ のみ → raw/prices/petmi_robots.txt |
| ペットミー | https://petmi.jp/terms/ | 利用規約確認 | 200。第4条（禁止事項）にクローリング/スクレイピング禁止の明記なし（「本サイトの運営を阻害する行為」等のみ）→ raw/prices/petmi_terms.html |
| ペットミー | https://petmi.jp/dog/ , https://petmi.jp/cat/ | 犬種/猫種 kind ID の確認 | 200 |
| ペットミー | https://petmi.jp/{dog,cat}/kind-{ID}/?page=N | 全国一覧（都道府県を絞らない）全ページ | 下表。全438ページ HTTP 200。サンプル4ページ（dog kind-64/95, cat kind-92/99 の1ページ目）を raw/prices/petmi_*_p1.html + .meta.txt に保存。全カードは raw/prices/petmi_listings.jsonl、ページごとのステータスは raw/prices/petmi_fetchlog.tsv |
| ブリーダーナビ | https://www.breeder-navi.jp/robots.txt（依頼者確認済み）, https://www.breeder-navi.jp/ | 構造確認（トップ1回のみ） | 200（Inertia.js アプリ） |
| ブリーダーナビ | https://www.breeder-navi.jp/term | 利用規約確認（Playwright で描画） | 200。**禁止事項に「当社コンテンツを、クローリング、スクレイピング等の自動化された手段を用いてデータ収集、抽出、加工、解析または蓄積等をする行為」「データマイニング…」「事前の許可を得ずに…子犬・成犬の情報…をコピー、転載」** → 取得しない。証跡 raw/prices/breedernavi_term_rendered.txt |

### kind ID 対応（ペットミー）

親カテゴリ（例 kind-64 トイプードル）は子カテゴリ（トイ/タイニー/ティーカップ等）を含むことを件数比較で確認（kind-64=2,223 > kind-224 トイプードル(トイ)=2,012）。

| 依頼上の品種 | URL |
|---|---|
| トイ・プードル | https://petmi.jp/dog/kind-64/ |
| チワワ | https://petmi.jp/dog/kind-5/ |
| ミニチュア・ダックスフンド | https://petmi.jp/dog/kind-56/ |
| ポメラニアン | https://petmi.jp/dog/kind-127/ |
| 柴犬 | https://petmi.jp/dog/kind-166/ |
| ミニチュア・シュナウザー | https://petmi.jp/dog/kind-19/ |
| フレンチ・ブルドッグ | https://petmi.jp/dog/kind-47/ |
| ヨークシャー・テリア | https://petmi.jp/dog/kind-102/ |
| マルチーズ | https://petmi.jp/dog/kind-55/ |
| シー・ズー | https://petmi.jp/dog/kind-33/ |
| ゴールデン・レトリーバー | https://petmi.jp/dog/kind-140/ |
| MIX（ハーフ） | https://petmi.jp/dog/kind-95/ （ハーフ犬・ミックス犬） |
| スコティッシュ・フォールド | https://petmi.jp/cat/kind-92/ |
| マンチカン | https://petmi.jp/cat/kind-138/ |
| ラグドール | https://petmi.jp/cat/kind-177/ |
| ブリティッシュ・ショートヘア | https://petmi.jp/cat/kind-22/ |
| ミヌエット | https://petmi.jp/cat/kind-51/ |
| アメリカン・ショートヘア | https://petmi.jp/cat/kind-91/ |
| エキゾチック | https://petmi.jp/cat/kind-99/ |
| ノルウェージャン | https://petmi.jp/cat/kind-24/ （ノルウェージャンフォレストキャット） |

### 取れなかったもの

| 対象 | 分類 | 理由 |
|---|---|---|
| ブリーダーナビ 子犬の価格一覧 | 取得失敗（規約上取得せず） | 利用規約でスクレイピング等の自動収集を明示的に禁止。技術的にはブロックされていない。許諾を得れば取得可能 |
| ブリーダーナビ 猫 | 存在しない | 同サイトは犬のみ（トップ/ナビゲーションに猫カテゴリなし） |
| ペットミー ブリーダー直販の掲載 | 存在しない（今回の一覧範囲では） | 取得カードの店舗ラベルは全件「店舗：」（ペットショップ） |
