#!/usr/bin/env python3

import re
import sys
from gomiget_base import GomigetBase, GomigetParameter

class GomigetAichiToyokawaShi(GomigetBase):
    def __init__(self):
        parameter = GomigetParameter()
        parameter.prefecture_name = "愛知県"
        parameter.municipality_name = "豊川市"
        parameter.data_source_url = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
        parameter.target_url_base = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
        parameter.target_pages = [ "agyo.html", "kagyo.html", "sagyo.html", "tagyo.html", "nagyo.html", "hagyo.html", "magyo.html", "yagyo.html", "ragyo.html", "wagyo.html" ]
        parameter.datetime_selector = "p.update"
        parameter.datetime_pattern = "更新日:%Y年%m月%d日"
        parameter.article_row_selector = "caption ~ tr"
        parameter.article_column_selector = "td"
        parameter.text_to_category_id = {
            "可燃ごみ": "burnable",
            "不燃ごみ": "unburnable",
            "資源": "recyclable",
            "危険ごみ": "hazardous",
            "粗大ごみ": "oversized",
            "家電リサイクル法対象品目": "legalrecycling",
            "市で処理できません。": "uncollectible"
        }
        parameter.note_to_category_id = None
        parameter.local_category_definition = None
        super(GomigetAichiToyokawaShi, self).__init__(parameter)

def main(args):
    print(GomigetAichiToyokawaShi().as_json())

if __name__ == "__main__":
    main(sys.argv)
