# 目次

* [1. 基本事項](#1-基本事項)
* [2. データ構成](#2-データ構成)
* [3. データ定義例](#3-データ定義例)

# 1. 基本事項

* JSON形式を使用します。
* ひとつの自治体につきひとつのファイルを構成します。

# 2. データ構成

※ (任意) は設定が必須ではない項目を示します。

* "municipalityId" (市区町村コード) : String
* "municipalityName" (自治体名) : String
* "datasourceUrl" ([情報取得元URL](#情報取得元URL)) : String (任意)
* "updatedAt" ([情報更新日](#情報更新日)) : String (任意)
* "categoryDefinitions" (分類定義) : Object
  * [分類ID](#分類ID) : String
    * "name" (分類名) : String
    * "note" (備考) : String (任意)
    * "icon" ([アイコンURL](#アイコンURL)) : String (任意)
* "articles" (品目情報の並び) : Array
  * "name" (品目名) : String
  * "nameKana" (品目名ひらがな) : String (任意)
  * "categoryId" ([分類ID](#分類ID)) : String
  * "note" (備考) : String (任意)

### 情報更新日

分別例の最終更新日を `YYYY-MM-DD` 形式の文字列で格納します。  
(情報を取得した日付ではなく分別例の内容が最後に更新された日付)

### 情報取得元URL

分別例情報の取得元としたウェブページへのURLを格納します。

### 分類ID

ごみの分類を識別するIDです。  
IDに使用できる文字は英小文字/数字/ハイフン/ピリオドです。  

### アイコンURL

分類を表すアイコン画像のURLを指定できます。  
省略した場合は `img/{分類ID}.png` が指定されたものとします。

# 3. データ定義例

```json
{
  "municipalityId": "12345",
  "municipalityName": "五味県志源市",
  "datasourceUrl": "https://www.gomishigen.lg.jp/index.html",
  "updatedAt": "2020-01-01",
  "categoryDefinitions": {
    "burnable": {
      "name": "可燃ごみ",
      "note": "赤の指定袋に入れる",
      "icon": "img/fire.png"
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
