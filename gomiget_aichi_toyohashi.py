#!/usr/bin/env python3

import sys
from gomiget_main import Gomiget, PatternValue, ArticleRow, overrides

class GomigetToyohashi(Gomiget):
    @overrides(Gomiget)
    def get_article_row(self, texts):
        if len(texts) < 5:
            return None
        row = ArticleRow()
        row.name = texts[0]
        row.category = texts[3]
        row.note = texts[-1:][0]
        return row

def main(argv):
    gomiget = GomigetToyohashi()
    gomiget.municipality_id = "232017"
    gomiget.municipality_name = "愛知県豊橋市"
    gomiget.datasource_url = "http://www2.city.toyohashi.aichi.jp/kankyo/dictionary/index.html"
    gomiget.target_url_base = "http://www2.city.toyohashi.aichi.jp/kankyo/dictionary/search.cgi?mode=index&key="
    gomiget.target_pages = [ "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
    gomiget.datetime_selector = None
    gomiget.datetime_pattern = None
    gomiget.article_row_selector = "form > table > tr > td > table > tr > td > table > tr"
    gomiget.article_column_selector = "td"
    gomiget.category_to_category_id = {
        PatternValue("生ごみ", "foodscraps"),
        PatternValue("もやすごみ", "burnable"),
        PatternValue("こわすごみ", "crushable"),
        PatternValue("危険ごみ", "hazardous"),
        PatternValue("うめるごみ", "unburnable"),
        PatternValue("大きなごみ", "oversized"),
        PatternValue("びん・カン", "grassbottle"),
        PatternValue("ペットボトル", "petbottle"),
        PatternValue("プラマークごみ", "plasticpackaging"),
        PatternValue("布類", "cloth"),
        PatternValue("古紙", "localcollection.paper"),
        PatternValue("家電４品目", "legalrecycling"),
        PatternValue("―", "uncollectible"),
        PatternValue("パソコン", "uncollectible"),
        PatternValue("収集しません", "uncollectible")
    }
    # gomiget.note_to_category_id
    gomiget.category_definitions = {
        "burnable": { "name": "もやすごみ", "note": "週2回／指定ごみ袋" },
        "foodscraps": { "name": "生ごみ", "note": "週2回／指定ごみ袋" },
        "plasticpackaging": { "name": "プラマークごみ", "note": "水曜日／透明又は半透明の袋" },
        "crushable": { "name": "こわすごみ", "note": "月曜日又は火曜日（４週に１回）／指定ごみ袋" },
        "unburnable": { "name": "うめるごみ", "note": "月曜日又は火曜日（８週に１回）／透明又は半透明の袋" },
        "grassbottle": { "name": "びん・カン", "note": "木曜日又は金曜日／透明又は半透明の袋" },
        "petbottle": { "name": "ペットボトル", "note": "水曜日／透明又は半透明の袋" },
        "localcollection": { "name": "地域資源回収" },
        "localcollection.paper": { "name": "地域資源回収(古紙)" },
        "cloth": { "name": "布類", "note": "月曜日又は火曜日（８週に１回）／透明又は半透明の袋" },
        "hazardous": { "name": "危険ごみ", "note": "水曜日（４週に１回）／透明又は半透明の袋" },
        "oversized": { "name": "大きなごみ", "note": "戸別有料収集又は資源化センターへの自己搬入" },
        "legalrecycling": { "name": "家電４品目" },
        "uncollectible": { "name": "収集しません" }
    }
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
