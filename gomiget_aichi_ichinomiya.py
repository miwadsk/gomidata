#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair

def main(argv):
    reader = GomiReader()
    reader.municipality_id = "232033"
    reader.municipality_name = "愛知県一宮市"
    reader.datasource_url = "https://www.city.ichinomiya.aichi.jp/kurashi/gomi/1000388/1000167/index.html"
    reader.target_url_base = "https://www.city.ichinomiya.aichi.jp/kurashi/gomi/1000388/1000167/"
    reader.target_pages = [ "1001702.html", "1001703.html", "1001700.html", "1001701.html", "1001698.html", "1001699.html", "1001696.html", "1001697.html", "1001694.html", "1001695.html" ]
    reader.datetime_selector = "p.update"
    reader.datetime_pattern = "更新日\r\n%Y年%m月%d日"
    reader.article_row_selector = "tbody > tr"
    reader.article_column_selector = "td"
    reader.category_to_category_id = {
        PatternValuePair(r"/可燃ごみ.*/", "burnable"),
        PatternValuePair(r"/不燃ごみ.*/", "unburnable"),
        PatternValuePair(r"/粗大ごみ.*/", "oversized"),
        PatternValuePair(r"/空き缶・金属類.*/", "metal"),
        PatternValuePair(r"/プラスチック製容器包装.*/", "plasticpackaging"),
        PatternValuePair("ペットボトル", "petbottle"),
        PatternValuePair(r"/町内回収資源.*/", "localcollection"),
        PatternValuePair("戸別収集", "housecollection"),
        PatternValuePair(r"/市では収集.*できません.*/", "uncollectible")
    }
    reader.note_to_category_id = [
        PatternValuePair(r"/家電リサイクル法対象品目.*/", "legalrecycling")
    ]
    reader.category_definitions = {
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
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
