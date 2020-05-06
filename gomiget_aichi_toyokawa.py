#!/usr/bin/env python3

import sys
from gomiget_main import Gomiget, PatternValue

def main(argv):
    gomiget = Gomiget()
    gomiget.municipality_id = "232076"
    gomiget.municipality_name = "愛知県豊川市"
    gomiget.datasource_url = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
    gomiget.target_url_base = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
    gomiget.target_pages = [ "agyo.html", "kagyo.html", "sagyo.html", "tagyo.html", "nagyo.html", "hagyo.html", "magyo.html", "yagyo.html", "ragyo.html", "wagyo.html" ]
    gomiget.datetime_selector = "p.update"
    gomiget.datetime_pattern = "更新日:%Y年%m月%d日"
    gomiget.article_row_selector = "caption ~ tr"
    gomiget.article_column_selector = "td"
    gomiget.category_to_category_id = [
        PatternValue("可燃ごみ", "burnable"),
        PatternValue("不燃ごみ", "unburnable"),
        PatternValue("資源", "recyclable"),
        PatternValue("危険ごみ", "hazardous"),
        PatternValue("粗大ごみ", "oversized"),
        PatternValue("家電リサイクル法対象品目", "legalrecycling"),
        PatternValue("市で処理できません。", "uncollectible")
    ]
    # gomiget.note_to_category_id
    gomiget.category_definitions = {
        "burnable": { "name": "可燃ごみ" },
        "unburnable": { "name": "不燃ごみ" },
        "recyclable": { "name": "資源" },
        "hazardous": { "name": "危険ごみ" },
        "oversized": { "name": "粗大ごみ" },
        "legalrecycling": { "name": "家電リサイクル法対象" },
        "uncollectible": { "name": "回収できません" }
    }
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
