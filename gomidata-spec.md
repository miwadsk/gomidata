# 目次

* [1. 基本事項](#1-基本事項)
* [2. データ構成](#2-データ構成)
* [3. データ定義例](#3-データ定義例)

# 1. 基本事項

* JSON 形式を使用します。
* ひとつの自治体につきひとつのファイルを構成します。

# 2. データ構成

* "municipality" (自治体名) : String
* "updatedAt" ([情報更新日](#情報更新日)) : String (任意)
* "sourceUrl" ([情報取得元URL](#情報取得元URL)) : String (任意)
* "articles" (品目情報の並び) : Array
  * "name" (品目名) : String
  * "nameKana" (品目名仮名) : String (任意)
  * "category" ([品目分類](#品目分類)) : String
  * "note" (品目備考) : String (任意)

### 情報更新日

分別例の最終更新日を YYYY-MM-DD 形式の文字列で格納します。  
(データを取得した日付ではなく、分別例の内容が最後に更新された日付)

### 情報取得元URL

データ取得元としたウェブページ等への URL を格納します。

### 品目分類

当該品目の分類を [共通分類ID](#共通分類ID) にて格納します。

### 共通分類ID

ID                         | 意味
---------------------------|--------------------------
burnable                   | 可燃ごみ
unburnable                 | 不燃ごみ
oversized                  | 粗大ごみ
hazardous                  | 危険ごみ
recyclable                 | 資源
recyclable-paper           | 資源 (紙類)
recyclable-paperpack       | 資源 (紙製容器包装)
recyclable-plasticpack     | 資源 (プラ容器包装)
recyclable-can             | 資源 (空缶)
recyclable-pet             | 資源 (ペットボトル)
recyclable-steel           | 資源 (スチール)
recyclable-alminium        | 資源 (アルミニウム)
recyclable-bottole         | 資源 (びん)
recyclable-reusablebottole | 資源 (再利用びん)
recyclable-clothing        | 資源 (衣類)
legalrecycling             | 家電リサイクル法対象品
selfcarrying               | 拠点回収
uncollectible              | 回収できません
unknown                    | 分類不明

# 3. データ定義例

```json
{
  "municipality": "豊川市",
  "updatedAt": "2020-03-01",
  "sourceUrl": "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/index.html",
  "articles": [
    {
      "name": "アイスピック",
      "nameKana": "あいすぴっく",
      "category": "unburnable",
      "note": "先端にセロテープなどを巻きつけて刺さらないようにしてください。"
    },
    {
      "name": "アイスまくら",
      "nameKana": "あいすまくら",
      "category": "burnable"
    },
    ...
  ],
}
```
