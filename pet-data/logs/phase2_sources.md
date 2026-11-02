# Phase 2 出典一覧（取得日はすべて 2026-11-02）

各 raw ファイルの隣に `.meta.txt`（URL / 取得日 / HTTPステータス）あり。

## 3-2 狂犬病予防法
| URL | 保存先 | 結果 |
|---|---|---|
| https://www.mhlw.go.jp/bunya/kenkou/kekkaku-kansenshou10/02.html | raw/mhlw/02.html | 200 取得（昭和35年〜令和6年度） |
| https://www.e-stat.go.jp/stat-search/files?…toukei=00450027&query=狂犬病 等（検索） | — | 一覧取得（raw/mhlw/estat/list.tsv） |
| https://www.e-stat.go.jp/stat-search/file-download?statInfId=…&fileKind=1（22本） | raw/mhlw/estat/{年}_{statInfId}.csv | 200 取得: 1996, 1997(1-3月), 2005-2025年度 |
| e-Stat 1997〜2004年度の同表 | — | **取得失敗**（サイト検索で該当表が見つからない） |
| e-Stat API | — | 未使用（appId なし） |

## 3-3 ペットフード協会
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

## 3-4 業者定期報告
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
