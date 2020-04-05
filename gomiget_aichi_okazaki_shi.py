#!/usr/bin/env python3

import re
import sys
from gomiget_base import GomigetBase, GomigetParameter

class GomigetAichiOkazakiShi(GomigetBase):
    def __init__(self):
        parameter = GomigetParameter()
        parameter.prefecture_name = "愛知県"
        parameter.municipality_name = "岡崎市"
        parameter.data_source_url = "https://www.city.okazaki.lg.jp/1100/1108/1151/p003039.html"
        parameter.target_url_base = "https://www.city.okazaki.lg.jp/1100/1108/1151/"
        parameter.target_pages = [ "p003041.html", "p003042.html", "p003043.html", "p003044.html", "p003045.html", "p003046.html", "p003047.html", "p003048.html", "p003049.html", "p003050.html" ]
        parameter.datetime_selector = "span.date"
        parameter.datetime_pattern = "最終更新日%Y年%m月%d日"
        parameter.article_row_selector = "tbody > tr"
        parameter.article_column_selector = "td"
        parameter.text_to_category_id = {
            "可燃ごみ": "burnable",
            "（可燃ごみ）": "burnable",
            "不燃ごみ": "unburnable",
            "粗大ごみ": "oversized",
            "有害ごみ": "hazardous.harmful",
            "発火性危険ごみ": "hazardous.ignitable",
            "紙製容器包装": "recyclable.paperpackaging",
            "プラスチック製容器包装": "recyclable.plasticpackaging",
            "プラスチック製容器装": "recyclable.plasticpackaging",
            "ペットボトル": "recyclable.petbottole",
            "空き缶": "recyclable.can",
            "生きびん": "recyclable.reusebottole",
            "空きびん": "recyclable.grassbottole",
            "処理困難物": "uncollectible.difficult",
            "リサイクル料金が必要。製造メーカーの電話受付窓口へ": "uncollectible.makercollection",
            "家電4品目 リサイクル料金が必要": "legalrecycling",
            "家電4品目　リサイクル料金が必要": "legalrecycling"
        }
        parameter.note_to_category_id = [
            { "pattern": re.compile(r"資源回収または拠点回収へ"), "category_id": "localcollection" },
            { "pattern": re.compile(r".*回収協力店へ.*"), "category_id": "pointcollection" },
            { "pattern": re.compile(r".*販売店へ.*"), "category_id": "uncollectible.sellercollection" },
            { "pattern": re.compile(r".*自主回収へ.*"), "category_id": "uncollectible.sellercollection" },
            { "pattern": re.compile(r".*青色のコンテナへ"), "category_id": "recyclable.can" },
            { "pattern": re.compile(r".*白色のコンテナへ"), "category_id": "recyclable.reusebottole" }
        ]
        parameter.local_category_definition = {
            "hazardous": {
                "subCategories": {
                    "hazardous.ignitable": { "name": "発火性危険ごみ" },
                    "hazardous.harmful": { "name": "有害ごみ" }
                }
            },
            "recyclable": {
                "subCategories": {
                    "recyclable.paperpackaging": { "name": "紙製容器包装" },
                    "recyclable.plasticpackaging": { "name": "プラ容器包装" },
                    "recyclable.petbottole": { "name": "ペットボトル" },
                    "recyclable.reusebottole": { "name": "生きびん" },
                    "recyclable.grassbottole": { "name": "空きびん" },
                    "recyclable.can": { "name": "空き缶" }
                }
            },
            "uncollectible": {
                "subCategories": {
                    "uncollectible.difficult": { },
                    "uncollectible.sellercollection": { },
                    "uncollectible.makercollection": { }
                }
            }
        }
        super(GomigetAichiOkazakiShi, self).__init__(parameter)

def main(args):
    print(GomigetAichiOkazakiShi().as_json())

if __name__ == "__main__":
    main(sys.argv)
