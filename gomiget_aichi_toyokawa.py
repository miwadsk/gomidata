#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair

def main(argv):
    reader = GomiReader()
    reader.municipality_id = "232076"
    reader.municipality_name = "愛知県豊川市"
    reader.datasource_url = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
    reader.target_url_base = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
    reader.target_pages = [ "agyo.html", "kagyo.html", "sagyo.html", "tagyo.html", "nagyo.html", "hagyo.html", "magyo.html", "yagyo.html", "ragyo.html", "wagyo.html" ]
    reader.datetime_selector = "p.update"
    reader.datetime_pattern = "更新日:%Y年%m月%d日"
    reader.article_row_selector = "caption ~ tr"
    reader.article_column_selector = "td"
    reader.category_to_category_id = [
        PatternValuePair("可燃ごみ", "burnable"),
        PatternValuePair("不燃ごみ", "unburnable"),
        PatternValuePair("資源", "recyclable"),
        PatternValuePair("危険ごみ", "hazardous"),
        PatternValuePair("粗大ごみ", "oversized"),
        PatternValuePair("家電リサイクル法対象品目", "legalrecycling"),
        PatternValuePair("市で処理できません。", "uncollectible")
    ]
    # reader.note_to_category_id
    reader.category_definitions = {
        "burnable": { "name": "可燃ごみ" },
        "unburnable": { "name": "不燃ごみ" },
        "recyclable": { "name": "資源" },
        "hazardous": { "name": "危険ごみ" },
        "oversized": { "name": "粗大ごみ" },
        "legalrecycling": { "name": "家電リサイクル法対象" },
        "uncollectible": { "name": "回収できません" }
    }
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
