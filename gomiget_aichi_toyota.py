#!/usr/bin/env python3

import sys
from gomiget_main import Gomiget, PatternValue

def main(argv):
    gomiget = Gomiget()
    gomiget.municipality_id = "232114"
    gomiget.municipality_name = "愛知県豊田市"
    gomiget.datasource_url = "https://manage.delight-system.com/threeR/web/bunbetsu?menu=bunbetsu&jichitaiId=toyotashi&lang=ja"
    gomiget.target_url_base = "https://manage.delight-system.com/threeR/web/bunbetsu?menu=bunbetsu&jichitaiId=toyotashi&lang=ja"
    gomiget.target_pages = [ "" ]
    gomiget.datetime_selector = None
    gomiget.datetime_pattern = None
    gomiget.article_row_selector = "div.panel-heading"
    gomiget.article_column_selector = "a.panel-title, div.panel-body"
    gomiget.category_to_category_id = {
        PatternValue("燃やすごみ", "burnable"),
        PatternValue("埋めるごみ", "unburnable"),
        PatternValue("粗大ごみ", "oversized"),
        PatternValue("資源（ガラスびん・飲料缶・ペットボトル・有害ごみ・危険ごみ）", "recyclable"),
        PatternValue("プラスチック製容器包装", "plasticpackaging"),
        PatternValue("金属ごみ", "metal"),
        PatternValue("古布類", "pointcollection.cloth"),
        PatternValue("古紙類", "pointcollection.paper"),
        PatternValue("家電４品目（市では収集しないもの）", "legalrecycling"),
        PatternValue("禁止（市では収集しないもの）", "uncollectible")
    }
    # gomiget.note_to_category_id
    gomiget.category_definitions = {
        "burnable": { "name": "燃やすごみ" },
        "unburnable": { "name": "埋めるごみ" },
        "oversized": { "name": "粗大ごみ" },
        "plasticpackaging": { "name": "プラ容器包装" },
        "metal": { "name": "金属ごみ" },
        "recyclable": { "name": "資源" },
        "pointcollection.cloth": { "name": "古布類" },
        "pointcollection.paper": { "name": "古紙類" },
        "legalrecycling": { "name": "家電リサイクル法対象" },
        "uncollectible": { "name": "回収できません" }
    }
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
