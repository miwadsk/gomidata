#!/usr/bin/env python3

import re
import sys
from gomiget import GomigetBase, GomigetSetting

class GomigetAichiToyokawaShi(GomigetBase):
    def __init__(self):
        setting = GomigetSetting()
        setting.prefecture_name = "愛知県"
        setting.municipality_name = "豊川市"
        setting.data_source_url = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
        setting.target_url_base = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
        setting.target_pages = [ "agyo.html", "kagyo.html", "sagyo.html", "tagyo.html", "nagyo.html", "hagyo.html", "magyo.html", "yagyo.html", "ragyo.html", "wagyo.html" ]
        setting.datetime_selector = "p.update"
        setting.datetime_pattern = "更新日:%Y年%m月%d日"
        setting.article_row_selector = "caption ~ tr"
        setting.article_column_selector = "td"
        setting.text_to_category_id = {
            "可燃ごみ": "burnable",
            "不燃ごみ": "unburnable",
            "資源": "recyclable",
            "危険ごみ": "hazardous",
            "粗大ごみ": "oversized",
            "家電リサイクル法対象品目": "legalrecycling",
            "市で処理できません。": "uncollectible"
        }
        setting.note_to_category_id = None
        setting.local_category_definition = None
        super(GomigetAichiToyokawaShi, self).__init__(setting)

def main(args):
    print(GomigetAichiToyokawaShi().as_json())

if __name__ == "__main__":
    main(sys.argv)
