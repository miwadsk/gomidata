#!/usr/bin/env python3

import re
import sys
from gomiget_base import GomigetBase, GomigetParameter

class GomigetAichiNagoyaShi(GomigetBase):
    def __init__(self):
        parameter = GomigetParameter()
        parameter.prefecture_name = "愛知県"
        parameter.municipality_name = "名古屋市"
        parameter.data_source_url = "http://www.city.nagoya.jp/kurashi/category/5-6-22-0-0-0-0-0-0-0.html"
        parameter.target_url_base = "http://www.city.nagoya.jp/kankyo/page/"
        parameter.target_pages = [ "0000066278.html", "0000066280.html", "0000066282.html", "0000066283.html", "0000066302.html", "0000066303.html", "0000066305.html", "0000066307.html", "0000066308.html", "0000066309.html" ]
        parameter.datetime_selector = "span.syosai_hiduke"
        parameter.datetime_pattern = "最終更新日：%Y年%m月%d日"
        parameter.article_row_selector = "tbody > tr"
        parameter.article_column_selector = "td"
        parameter.text_to_category_id = {
            "可燃ごみ": "burnable",
            "不燃ごみ": "unburnable",
            "粗大ごみ": "oversized",
            "発火性危険物": "hazardous",
            "紙製容器包装": "recyclable.paperpackaging",
            "プラ容器包装": "recyclable.plasticpackaging",
            "空きびん": "recyclable.grassbottole",
            "空き缶": "recyclable.can",
            "紙パック": "pointcollection.beveragepack",
            "食用油": "pointcollection.edibleoil",
            "小型家電": "pointcollection.smallappliances"
        }
        parameter.note_to_category_id = [
            { "pattern": re.compile(r".*家電リサイクル法対象.*"), "category_id": "legalrecycling" },
            { "pattern": re.compile(r".*集団資源回収.*"), "category_id": "localcollection" },
            { "pattern": re.compile(r".*ご相談ください.*"), "category_id": "uncollectible" }
        ]
        parameter.local_category_definition = {
            "hazardous": {
                "name": "発火性危険物"
            },
            "recyclable": {
                "subCategories": {
                    "recyclable.paperpackaging": { "name": "紙製容器包装" },
                    "recyclable.plasticpackaging": { "name": "プラ容器包装" },
                    "recyclable.grassbottole": { "name": "空きびん" },
                    "recyclable.can": { "name": "空き缶" }
                }
            },
            "pointcollection": {
                "name": "回収ボックス",
                "subCategories": {
                    "pointcollection.beveragepack": { "name": "紙パック({categoryName})" },
                    "pointcollection.petbottle": { "name": "ペットボトル({categoryName})" },
                    "pointcollection.edibleoil": { "name": "食用油({categoryName})" },
                    "pointcollection.smallappliances": { "name": "小型家電({categoryName})" }
                }
            }
        }
        super(GomigetAichiNagoyaShi, self).__init__(parameter)

def main(args):
    print(GomigetAichiNagoyaShi().as_json())

if __name__ == "__main__":
    main(sys.argv)
