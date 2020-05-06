#!/usr/bin/env python3

import sys
from gomiget_main import Gomiget, PatternValue

def main(argv):
    # メモ:
    # 市のホームページでは「ビールびん」の分類が「空きびん」と誤記されているので
    # 空きびん・生きびんについては分類ではなく備考により分別するようにした。
    gomiget = Gomiget()
    gomiget.municipality_id = "232025"
    gomiget.municipality_name = "愛知県岡崎市"
    gomiget.datasource_url = "https://www.city.okazaki.lg.jp/1100/1108/1151/p003039.html"
    gomiget.target_url_base = "https://www.city.okazaki.lg.jp/1100/1108/1151/"
    gomiget.target_pages = [ "p003041.html", "p003042.html", "p003043.html", "p003044.html", "p003045.html", "p003046.html", "p003047.html", "p003048.html", "p003049.html", "p003050.html" ]
    gomiget.datetime_selector = "span.date"
    gomiget.datetime_pattern = "最終更新日%Y年%m月%d日"
    gomiget.article_row_selector = "tbody > tr"
    gomiget.article_column_selector = "td"
    gomiget.category_to_category_id = {
        PatternValue(r"/（?可燃ごみ）?/", "burnable"),
        PatternValue("不燃ごみ", "unburnable"),
        PatternValue("粗大ごみ", "oversized"),
        PatternValue("有害ごみ", "hazardous.harmful"),
        PatternValue("発火性危険ごみ", "hazardous.ignitable"),
        PatternValue("紙製容器包装", "paperpackaging"),
        PatternValue(r"/プラスチック製容器包?装/", "plasticpackaging"),
        PatternValue("ペットボトル", "petbottle"),
        PatternValue("空き缶", "can"),
        PatternValue("処理困難物", "uncollectible.difficult"),
        PatternValue("リサイクル料金が必要。製造メーカーの電話受付窓口へ", "uncollectible.makercollection"),
        PatternValue(r"/家電4品目\sリサイクル料金が必要/", "legalrecycling")
    }
    gomiget.note_to_category_id = [
        PatternValue("資源回収または拠点回収へ", "localcollection"),
        PatternValue(r"/.*回収協力店へ.*/", "pointcollection"),
        PatternValue(r"/.*販売店へ.*/", "uncollectible.sellercollection"),
        PatternValue(r"/.*自主回収へ.*/", "uncollectible.sellercollection"),
        PatternValue(r"/.*青色のコンテナへ/", "can"),
        PatternValue(r"/.*茶色のコンテナへ/", "grassbottle"),
        PatternValue(r"/.*白色のコンテナへ/", "reusebottle")
    ]
    gomiget.category_definitions = {
        "burnable": { "name": "可燃ごみ" },
        "unburnable": { "name": "不燃ごみ" },
        "oversized": { "name": "粗大ごみ" },
        "hazardous": { "name": "危険/有害ごみ" },
        "hazardous.ignitable": { "name": "発火性危険ごみ" },
        "hazardous.harmful": { "name": "有害ごみ" },
        "paperpackaging": { "name": "紙製容器包装" },
        "plasticpackaging": { "name": "プラ容器包装" },
        "petbottle": { "name": "ペットボトル" },
        "reusebottle": { "name": "生きびん" },
        "grassbottle": { "name": "空きびん" },
        "can": { "name": "空き缶" },
        "localcollection": { "name": "資源回収/拠点回収" },
        "pointcollection": { "name": "回収ボックス" },
        "legalrecycling": { "name": "家電リサイクル法対象" },
        "uncollectible": { "name": "回収できません" },
        "uncollectible.difficult": { "name": "回収できません(処理困難)" },
        "uncollectible.sellercollection": { "name": "回収できません(販売店回収)" },
        "uncollectible.makercollection": { "name": "回収できません(メーカー回収)" }
    }
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
