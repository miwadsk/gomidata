#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair

def main(argv):
    reader = GomiReader()
    reader.municipality_id = "232114"
    reader.municipality_name = "愛知県豊田市"
    reader.datasource_url = "https://manage.delight-system.com/threeR/web/bunbetsu?menu=bunbetsu&jichitaiId=toyotashi&lang=ja"
    reader.target_url_base = "https://manage.delight-system.com/threeR/web/bunbetsu?menu=bunbetsu&jichitaiId=toyotashi&lang=ja"
    reader.target_pages = [ "" ]
    reader.datetime_selector = None
    reader.datetime_pattern = None
    reader.article_row_selector = "div.panel-heading"
    reader.article_column_selector = "a.panel-title, div.panel-body"
    reader.category_to_category_id = {
        PatternValuePair("燃やすごみ", "burnable"),
        PatternValuePair("埋めるごみ", "unburnable"),
        PatternValuePair("粗大ごみ", "oversized"),
        PatternValuePair("資源（ガラスびん・飲料缶・ペットボトル・有害ごみ・危険ごみ）", "recyclable"),
        PatternValuePair("プラスチック製容器包装", "plasticpackaging"),
        PatternValuePair("金属ごみ", "metal"),
        PatternValuePair("古布類", "pointcollection.cloth"),
        PatternValuePair("古紙類", "pointcollection.paper"),
        PatternValuePair("家電４品目（市では収集しないもの）", "legalrecycling"),
        PatternValuePair("禁止（市では収集しないもの）", "uncollectible")
    }
    # reader.note_to_category_id
    reader.category_definitions = {
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
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
