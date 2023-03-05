# gomidata

このリポジトリでは、日本国内の各自治体が公開している家庭ごみ・資源の分別例を、  
アプリケーションから容易に利用できるようにすることを目的として、

* 共通データフォーマット仕様の定義
* 分別データ取得プログラムの提供

を行います。

### データフォーマット仕様

[gomidata-spec](gomidata-spec.md)

### データ取得プログラム

対象自治体名   | プログラムファイル名
---------------|------------------------------
愛知県豊川市   | [gomiget_aichi_toyokawa.py](gomiget_aichi_toyokawa.py)
愛知県名古屋市 | [gomiget_aichi_nagoya.py](gomiget_aichi_nagoya.py)
愛知県岡崎市   | [gomiget_aichi_okazaki.py](gomiget_aichi_okazaki.py)
愛知県豊田市   | [gomiget_aichi_toyota.py](gomiget_aichi_toyota.py)
愛知県豊橋市   | [gomiget_aichi_toyohashi.py](gomiget_aichi_toyohashi.py)
愛知県安城市   | [gomiget_aichi_anjo.py](gomiget_aichi_anjo.py)
愛知県瀬戸市   | [gomiget_aichi_seto.py](gomiget_aichi_seto.py)

プログラムの実行には以下のライブラリが必要です。

* requests
* pykakasi (v1.2.0)
* mojimoji
* bs4

### ライセンス

このリポジトリの内容には CC0 を適用します。

[![CC0](https://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](https://creativecommons.org/publicdomain/zero/1.0/deed.ja)

### 関連リポジトリ

* ごみ分別検索ウェブアプリ「Gomipedia」  
https://github.com/suconbu/gomipedia
