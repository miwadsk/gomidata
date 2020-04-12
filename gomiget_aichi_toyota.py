#!/usr/bin/env python3

import re
import sys
from gomiget_base import GomigetBase, GomigetParameter

class GomigetAichiToyota(GomigetBase):
    def __init__(self):
        parameter = GomigetParameter()
        parameter.prefecture_name = "愛知県"
        parameter.municipality_name = "豊田市"
        parameter.data_source_url = "https://manage.delight-system.com/threeR/web/bunbetsu?menu=bunbetsu&jichitaiId=toyotashi&lang=ja"
        parameter.target_url_base = "https://manage.delight-system.com/threeR/web/bunbetsu?menu=bunbetsu&jichitaiId=toyotashi&lang=ja"
        parameter.target_pages = [ "" ]
        parameter.datetime_selector = None
        parameter.datetime_pattern = None
        parameter.article_row_selector = "div.panel-heading"
        parameter.article_column_selector = "a.panel-title, div.panel-body"
        parameter.text_to_category_id = {
            "燃やすごみ": "burnable",
            "埋めるごみ": "unburnable",
            "粗大ごみ": "oversized",
            "資源（ガラスびん・飲料缶・ペットボトル・有害ごみ・危険ごみ）": "recyclable.other",
            "プラスチック製容器包装": "recyclable.plasticpackaging",
            "金属ごみ": "recyclable.metal",
            "古布類": "pointcollection.cloth",
            "古紙類": "pointcollection.paper",
            "家電４品目（市では収集しないもの）": "legalrecycling",
            "禁止（市では収集しないもの）": "uncollectible"
        }
        parameter.note_to_category_id = None
        parameter.local_category_definition = {
            "burnable": {
                "name": "燃やすごみ"
            },
            "unburnable": {
                "name": "埋めるごみ"
            },
            "recyclable": {
                "name": "資源・金属ごみ・プラ容器包装",
                "subCategories": {
                    "recyclable.plasticpackaging": { "name": "プラ容器包装" },
                    "recyclable.metal": { "name": "金属ごみ" },
                    "recyclable.other": { "name": "資源" }
                }
            },
            "pointcollection": {
                "name": "リサイクルステーション",
                "subCategories": {
                    "pointcollection.cloth": { "name": "古布類" },
                    "pointcollection.paper": { "name": "古紙類" },
                }
            }
        }
        super(GomigetAichiToyota, self).__init__(parameter)

def main(args):
    print(GomigetAichiToyota().as_json())

if __name__ == "__main__":
    main(sys.argv)
