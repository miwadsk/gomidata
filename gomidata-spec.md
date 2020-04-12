# 目次

* [1. 基本事項](#1-基本事項)
* [2. データ構成](#2-データ構成)
* [3. データ定義例](#3-データ定義例)

# 1. 基本事項

* JSON 形式を使用します。
* ひとつの自治体につきひとつのファイルを構成します。

# 2. データ構成

※ (任意) は設定が必須ではない項目を示します。

* "prefectureName" (都道府県名) : String
* "municipalityName" (自治体名) : String
* "dataSourceUrl" ([情報取得元URL](#情報取得元URL)) : String (任意)
* "updatedAt" ([情報更新日](#情報更新日)) : String (任意)
* "localCategoryDefinition" ([自治体固有分類定義](#自治体固有分類定義)) : Object (任意)
  * ([共通分類ID](#共通分類ID)) : String
    * "name" ([共通分類別名](#共通分類別名)) : String (任意)
    * "subCategories" : Object (任意)
      * [自治体固有分類ID](#自治体固有分類ID) : Object
        * "name" ([自治体固有分類名](#自治体固有分類名)) : String
* "articles" (品目情報の並び) : Array
  * "name" (品目名) : String
  * "nameKana" (品目名ひらがな) : String (任意)
  * "categoryId" ([共通分類ID](#共通分類ID) または [自治体固有分類ID](#自治体固有分類ID)) : String
  * "note" (備考) : String (任意)

### 情報更新日

分別例の最終更新日を YYYY-MM-DD 形式の文字列で格納します。  
(情報を取得した日付ではなく分別例の内容が最後に更新された日付)

### 情報取得元URL

分別例情報の取得元としたウェブページへの URL を格納します。

### 共通分類ID

全ての自治体で共通の分類を定義した ID です。

ID               | 共通分類名
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

共通分類ID を細分化した自治体固有の ID です。  
[自治体固有分類定義](#自治体固有分類定義) で定義する必要があります。  
ID に使用できる文字は英小文字と数字です。

### 自治体固有分類定義

共通分類ID に対する自治体固有の別名の設定、自治体固有分類ID に対する名前を設定します。

### 共通分類別名

共通分類名 に対して自治体固有の別名を指定します。  

### 自治体固有分類名

自治体固有分類IDに対する名前を設定します。  
文字列中には以下の変数を指定できます。

変数                 | 置換後の文字列
---------------------|---------------------
{categoryName}       | [共通分類名](#共通分類名) または [共通分類別名](#共通分類別名)

# 3. データ定義例

```json
{
  "prefectureName": "愛知県",
  "municipalityName": "豊川市",
  "dataSourceUrl": "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/index.html",
  "updatedAt": "2020-03-01",
  "localCategoryDefinition": {
    "recyclable": {
      "name": "資源ステーション",
      "subCategories": {
        "paperpackaging": {
          "name": "紙製容器包装"
        },
        ...
      }
    },
    ...
  },
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
  ]
}
```
