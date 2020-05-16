#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair

def main(argv):
    reader = GomiReader()
    reader.municipality_id = "231002"
    reader.municipality_name = "愛知県名古屋市"
    reader.datasource_url = "http://www.city.nagoya.jp/kurashi/category/5-6-22-0-0-0-0-0-0-0.html"
    reader.target_url_base = "http://www.city.nagoya.jp/kankyo/page/"
    reader.target_pages = [ "0000066278.html", "0000066280.html", "0000066282.html", "0000066283.html", "0000066302.html", "0000066303.html", "0000066305.html", "0000066307.html", "0000066308.html", "0000066309.html" ]
    reader.datetime_selector = "span.syosai_hiduke"
    reader.datetime_pattern = "最終更新日：%Y年%m月%d日"
    reader.article_row_selector = "tbody > tr"
    reader.article_column_selector = "td"
    reader.category_to_category_id = [
        PatternValuePair("可燃ごみ", "burnable"),
        PatternValuePair("不燃ごみ", "unburnable"),
        PatternValuePair("粗大ごみ", "oversized"),
        PatternValuePair("発火性危険物", "hazardous"),
        PatternValuePair("紙製容器包装", "paperpackaging"),
        PatternValuePair("プラ容器包装", "plasticpackaging"),
        PatternValuePair("ペットボトル", "petbottle"),
        PatternValuePair("空きびん", "grassbottle"),
        PatternValuePair("空き缶", "can"),
        PatternValuePair("紙パック", "beveragepack"),
        PatternValuePair("食用油", "pointcollection.edibleoil"),
        PatternValuePair("小型家電", "pointcollection.smallappliances")
    ]
    reader.note_to_category_id = [
        PatternValuePair(r"/.*処理して可燃ごみへ/", "burnable"),
        PatternValuePair(r"/.*家電リサイクル法対象.*/", "legalrecycling"),
        PatternValuePair(r"/.*集団資源回収.*/", "localcollection"),
        PatternValuePair(r"/.*小型家電回収ボックス.*/", "pointcollection.smallappliances"),
        PatternValuePair(r"/.*(環境事業所|協力店|販売店|消火器|病院・診療所|ご相談ください).*/", "uncollectible")
    ]
    reader.category_definitions = {
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
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
