#!/usr/bin/env python3

import re
import sys
from gomiget import GomigetBase, GomigetSetting

class GomigetAichiNagoyaShi(GomigetBase):
    def __init__(self):
        setting = GomigetSetting()
        setting.prefecture_name = "愛知県"
        setting.municipality_name = "名古屋市"
        setting.data_source_url = "http://www.city.nagoya.jp/kurashi/category/5-6-22-0-0-0-0-0-0-0.html"
        setting.target_url_base = "http://www.city.nagoya.jp/kankyo/page/"
        setting.target_pages = [ "0000066278.html", "0000066280.html", "0000066282.html", "0000066283.html", "0000066302.html", "0000066303.html", "0000066305.html", "0000066307.html", "0000066308.html", "0000066309.html" ]
        setting.datetime_selector = "span.syosai_hiduke"
        setting.datetime_pattern = "最終更新日：%Y年%m月%d日"
        setting.article_row_selector = "tbody > tr"
        setting.article_column_selector = "td"
        setting.text_to_category_id = {
            "可燃ごみ": "burnable",
            "不燃ごみ": "unburnable",
            "粗大ごみ": "oversized",
            "発火性危険物": "hazardous",
            "紙製容器包装": "paperpackaging",
            "プラ容器包装": "plasticpackaging",
            "空きびん": "grassbottole",
            "空き缶": "can",
            "紙パック": "beveragepack",
            "食用油": "edibleoil",
            "小型家電": "smallappliances"
        }
        setting.note_to_category_id = [
            { "pattern": re.compile(".*家電リサイクル法対象.*"), "category_id": "legalrecycling" },
            { "pattern": re.compile(".*集団資源回収.*"), "category_id": "localcollection" },
            { "pattern": re.compile(".*ご相談ください.*"), "category_id": "uncollectible" }
        ]
        setting.local_category_definition = {
            "hazardous": {
                "name": "発火性危険物"
            },
            "recyclable": {
                "name": "資源ステーション",
                "subCategories": {
                    "paperpackaging": { "name": "紙製容器包装" },
                    "plasticpackaging": { "name": "プラ容器包装" },
                    "grassbottole": { "name": "空きびん" },
                    "can": { "name": "空き缶" }
                }
            },
            "pointcollection": {
                "name": "回収ボックス",
                "subCategories": {
                    "beveragepack": { "name": "紙パック" },
                    "petbottle": { "name": "ペットボトル" },
                    "edibleoil": { "name": "食用油" },
                    "smallappliances": { "name": "小型家電" }
                }
            }
        }
        super(GomigetAichiNagoyaShi, self).__init__(setting)

def main(args):
    print(GomigetAichiNagoyaShi().as_json())

if __name__ == "__main__":
    main(sys.argv)
