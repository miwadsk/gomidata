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
  * "nameRoman" (品目名ローマ字) : String (任意)
  * "categoryId" ([共通分類ID](#共通分類ID) または [自治体固有分類ID](#自治体固有分類ID)) : String
  * "note" (備考) : String (任意)
* "localCategories" ([自治体固有分類定義の並び](#自治体固有分類定義の並び)) : Array (任意)
  * "localCategoryId" ([自治体固有分類ID](#自治体固有分類ID)) : String
  * "commonCategoryId" ([共通分類ID](#共通分類ID)) : String
  * "name" (分類表示名) : String

### 情報更新日

分別例の最終更新日を YYYY-MM-DD 形式の文字列で格納します。  
(情報を取得した日付ではなく分別例の内容が最後に更新された日付)

### 情報取得元URL

分別例情報の取得元としたウェブページへの URL を格納します。

### 共通分類ID

全ての自治体で共通の分類を定義した ID です。

ID               | 分類名
-----------------|--------------------------
burnable         | 可燃ごみ
unburnable       | 不燃ごみ
oversized        | 粗大ごみ
hazardous        | 危険ごみ
recyclable       | 資源
legalrecycling   | 家電リサイクル法対象品
pointcollection  | 拠点回収
localcollection  | 集団回収
uncollectible    | 回収できません
unknown          | 分類不明

### 自治体固有分類ID

共通分類ID では分類できない、あるいは独自の分類名を持つ当該自治体固有の分類を示す ID です。  
[自治体固有分類定義の並び](#自治体固有分類定義の並び) で定義する必要があります。  
ID は '#' で始まり使用できる文字は英小文字、数字、ピリオド、ハイフンです。

### 自治体固有分類定義の並び

自治体固有分類ID と 共通分類ID との紐づけ、および表示名の定義をします。

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
      "categoryId": "unburnable",
      "note": "先端にセロテープなどを巻きつけて刺さらないようにしてください。"
    },
    {
      "name": "アイスまくら",
      "nameKana": "あいすまくら",
      "categoryId": "burnable"
    },
    ...
  ],
  "localCategories": [
    {
      "localId": "#ignitablehazardous",
      "commonId": "hazardous",
      "name": "発火性危険物"
    },
    ...
  ]
}
```
