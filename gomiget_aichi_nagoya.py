#!/usr/bin/env python3

import sys
from gomiget_main import Gomiget, PatternValue

def main(argv):
    gomiget = Gomiget()
    gomiget.municipality_id = "231002"
    gomiget.municipality_name = "愛知県名古屋市"
    gomiget.datasource_url = "http://www.city.nagoya.jp/kurashi/category/5-6-22-0-0-0-0-0-0-0.html"
    gomiget.target_url_base = "http://www.city.nagoya.jp/kankyo/page/"
    gomiget.target_pages = [ "0000066278.html", "0000066280.html", "0000066282.html", "0000066283.html", "0000066302.html", "0000066303.html", "0000066305.html", "0000066307.html", "0000066308.html", "0000066309.html" ]
    gomiget.datetime_selector = "span.syosai_hiduke"
    gomiget.datetime_pattern = "最終更新日：%Y年%m月%d日"
    gomiget.article_row_selector = "tbody > tr"
    gomiget.article_column_selector = "td"
    gomiget.category_to_category_id = [
        PatternValue("可燃ごみ", "burnable"),
        PatternValue("不燃ごみ", "unburnable"),
        PatternValue("粗大ごみ", "oversized"),
        PatternValue("発火性危険物", "hazardous"),
        PatternValue("紙製容器包装", "paperpackaging"),
        PatternValue("プラ容器包装", "plasticpackaging"),
        PatternValue("ペットボトル", "petbottle"),
        PatternValue("空きびん", "grassbottle"),
        PatternValue("空き缶", "can"),
        PatternValue("紙パック", "beveragepack"),
        PatternValue("食用油", "pointcollection.edibleoil"),
        PatternValue("小型家電", "pointcollection.smallappliances")
    ]
    gomiget.note_to_category_id = [
        PatternValue(r"/.*処理して可燃ごみへ/", "burnable"),
        PatternValue(r"/.*家電リサイクル法対象.*/", "legalrecycling"),
        PatternValue(r"/.*集団資源回収.*/", "localcollection"),
        PatternValue(r"/.*小型家電回収ボックス.*/", "pointcollection.smallappliances"),
        PatternValue(r"/.*(環境事業所|協力店|販売店|消火器|病院・診療所|ご相談ください).*/", "uncollectible")
    ]
    gomiget.category_definitions = {
        "burnable": { "name": "可燃ごみ" },
        "unburnable": { "name": "不燃ごみ" },
        "oversized": { "name": "粗大ごみ" },
        "hazardous": { "name": "発火性危険物" },
        "paperpackaging": { "name": "紙製容器包装" },
        "plasticpackaging": { "name": "プラ容器包装" },
        "beveragepack": { "name": "紙パック" },
        "petbottle": { "name": "ペットボトル" },
        "grassbottle": { "name": "空きびん" },
        "can": { "name": "空き缶" },
        "legalrecycling": { "name": "集団資源回収" },
        "pointcollection": { "name": "回収ボックス" },
        "pointcollection.edibleoil": { "name": "回収ボックス(食用油)" },
        "pointcollection.smallappliances": { "name": "回収ボックス(小型家電)" },
        "localcollection": { "name": "集団資源回収" },
        "legalrecycling": { "name": "家電リサイクル法対象" },
        "uncollectible": { "name": "回収できません" }
    }
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
