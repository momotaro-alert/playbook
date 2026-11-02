# Phase 4 sources（店頭価格）

取得日: 2026-11-02（全件）。User-Agent: `Mozilla/5.0 (research; contact via site)`。同一サイトへのリクエスト間隔 2.5 秒。

## 使ったURL

| サイト | URL | 用途 | 結果 |
|---|---|---|---|
| ペットミー | https://petmi.jp/robots.txt | クロール可否確認 | 200。Disallow は /api/, /pvt/, /shop-admin/ のみ → raw/prices/petmi_robots.txt |
| ペットミー | https://petmi.jp/terms/ | 利用規約確認 | 200。第4条（禁止事項）にクローリング/スクレイピング禁止の明記なし（「本サイトの運営を阻害する行為」等のみ）→ raw/prices/petmi_terms.html |
| ペットミー | https://petmi.jp/dog/ , https://petmi.jp/cat/ | 犬種/猫種 kind ID の確認 | 200 |
| ペットミー | https://petmi.jp/{dog,cat}/kind-{ID}/?page=N | 全国一覧（都道府県を絞らない）全ページ | 下表。全438ページ HTTP 200。サンプル4ページ（dog kind-64/95, cat kind-92/99 の1ページ目）を raw/prices/petmi_*_p1.html + .meta.txt に保存。全カードは raw/prices/petmi_listings.jsonl、ページごとのステータスは raw/prices/petmi_fetchlog.tsv |
| ブリーダーナビ | https://www.breeder-navi.jp/robots.txt（依頼者確認済み）, https://www.breeder-navi.jp/ | 構造確認（トップ1回のみ） | 200（Inertia.js アプリ） |
| ブリーダーナビ | https://www.breeder-navi.jp/term | 利用規約確認（Playwright で描画） | 200。**禁止事項に「当社コンテンツを、クローリング、スクレイピング等の自動化された手段を用いてデータ収集、抽出、加工、解析または蓄積等をする行為」「データマイニング…」「事前の許可を得ずに…子犬・成犬の情報…をコピー、転載」** → 取得しない。証跡 raw/prices/breedernavi_term_rendered.txt |

## kind ID 対応（ペットミー）

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

## 取れなかったもの

| 対象 | 分類 | 理由 |
|---|---|---|
| ブリーダーナビ 子犬の価格一覧 | 取得失敗（規約上取得せず） | 利用規約でスクレイピング等の自動収集を明示的に禁止。技術的にはブロックされていない。許諾を得れば取得可能 |
| ブリーダーナビ 猫 | 存在しない | 同サイトは犬のみ（トップ/ナビゲーションに猫カテゴリなし） |
| ペットミー ブリーダー直販の掲載 | 存在しない（今回の一覧範囲では） | 取得カードの店舗ラベルは全件「店舗：」（ペットショップ） |
