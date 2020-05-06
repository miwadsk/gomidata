#!/usr/bin/env python3

import sys
from gomiget_main import Gomiget, PatternValue

def main(argv):
    gomiget = Gomiget()
    gomiget.municipality_id = "232033"
    gomiget.municipality_name = "愛知県一宮市"
    gomiget.datasource_url = "https://www.city.ichinomiya.aichi.jp/kurashi/gomi/1000388/1000167/index.html"
    gomiget.target_url_base = "https://www.city.ichinomiya.aichi.jp/kurashi/gomi/1000388/1000167/"
    gomiget.target_pages = [ "1001702.html", "1001703.html", "1001700.html", "1001701.html", "1001698.html", "1001699.html", "1001696.html", "1001697.html", "1001694.html", "1001695.html" ]
    gomiget.datetime_selector = "p.update"
    gomiget.datetime_pattern = "更新日\r\n%Y年%m月%d日"
    gomiget.article_row_selector = "tbody > tr"
    gomiget.article_column_selector = "td"
    gomiget.category_to_category_id = {
        PatternValue(r"/可燃ごみ.*/", "burnable"),
        PatternValue(r"/不燃ごみ.*/", "unburnable"),
        PatternValue(r"/粗大ごみ.*/", "oversized"),
        PatternValue(r"/空き缶・金属類.*/", "metal"),
        PatternValue(r"/プラスチック製容器包装.*/", "plasticpackaging"),
        PatternValue("ペットボトル", "petbottle"),
        PatternValue(r"/町内回収資源.*/", "localcollection"),
        PatternValue("戸別収集", "housecollection"),
        PatternValue(r"/市では収集.*できません.*/", "uncollectible")
    }
    gomiget.note_to_category_id = [
        PatternValue(r"/家電リサイクル法対象品目.*/", "legalrecycling")
    ]
    gomiget.category_definitions = {
        "burnable": { "name": "可燃ごみ" },
        "unburnable": { "name": "不燃ごみ" },
        "oversized": { "name": "粗大ごみ" },
        "metal": { "name": "金属ごみ" },
        "plasticpackaging": { "name": "プラ容器包装" },
        "petbottle": { "name": "ペットボトル" },
        "localcollection": { "name": "町内回収資源" },
        "housecollection": { "name": "戸別回収" },
        "legalrecycling": { "name": "家電リサイクル法対象品" },
        "uncollectible": { "name": "回収できません" }
    }
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
