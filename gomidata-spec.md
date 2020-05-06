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
* "categoryDefinitions" ([自治体固有分類定義](#自治体固有分類定義)) : Object (任意)
  * ([共通分類ID](#共通分類ID) または [自治体固有分類ID](#自治体固有分類ID)) : String
    * "name" (分類名) : String (任意)
    * "note" (備考) : String (任意)
    * "icon" (アイコンURL) : String (任意)
* "articles" (品目情報の並び) : Array
  * "name" (品目名) : String
  * "nameKana" (品目名ひらがな) : String (任意)
  * "categoryId" ([共通分類ID](#共通分類ID) または [自治体固有分類ID](#自治体固有分類ID)) : String
  * "note" (備考) : String (任意)

### 情報更新日

分別例の最終更新日を YYYY-MM-DD 形式の文字列で格納します。  
(情報を取得した日付ではなく分別例の内容が最後に更新された日付)

### 情報取得元URL

分別例情報の取得元としたウェブページへのURLを格納します。

### 自治体固有分類定義

共通分類ID が示す定義内容の上書きあるいは自治体独自の分類の定義を行います。

### 共通分類ID

全ての自治体で共通の分類を識別するIDです。

ID                | 共通分類名
------------------|--------------------------
burnable          | 可燃ごみ
unburnable        | 不燃ごみ
oversized         | 粗大ごみ
hazardous         | 危険ごみ
recyclable        | 資源
can               | 空き缶
metal             | 金属
petbottle         | ペットボトル
grassbottle       | 空きびん
reusebottle       | 再利用びん
beveragepack      | 紙パック
paperpackaging    | 紙製容器包装
plasticpackaging  | プラ容器包装
legalrecycling    | 家電リサイクル法対象品
pointcollection   | 拠点回収
localcollection   | 集団回収
uncollectible     | 回収できません
unknown           | 分類不明

### 自治体固有分類ID

自治体固有の分類を識別するIDです。  
[共通分類ID](#共通分類ID) と重複してはいけません。  
IDに使用できる文字は英小文字/数字/ハイフン/ピリオドです。  

# 3. データ定義例

```json
{
  "municipalityId": "232076",
  "municipalityName": "愛知県豊川市",
  "datasourceUrl": "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/index.html",
  "updatedAt": "2020-03-01",
  "categoryDefinitions": {
    "paperpackaging": {
      "name": "紙製容器包装",
      "icon": "paperpackaging"
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
