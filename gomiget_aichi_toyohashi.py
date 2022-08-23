#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair

def main(argv):
    reader = GomiReader()
    reader.municipality_id = "232017"
    reader.municipality_name = "愛知県豊橋市"
    reader.datasource_url = "https://www.city.toyohashi.lg.jp/36806.htm"
    reader.target_url_base = ""
    reader.target_pages = [ "https://www.city.toyohashi.lg.jp/secure/60355/3r-bunbetsu.csv" ]
    reader.datetime_selector = None
    reader.datetime_pattern = None
    reader.article_row_selector = None
    reader.article_column_selector = None
    reader.article_index_name = 1
    reader.article_index_category = 2
    reader.article_index_note = 3
    reader.category_to_category_id = {
        PatternValuePair("生ごみ", "foodscraps"),
        PatternValuePair("もやすごみ", "burnable"),
        PatternValuePair("こわすごみ", "crushable"),
        PatternValuePair("危険ごみ", "hazardous"),
        PatternValuePair("うめるごみ", "unburnable"),
        PatternValuePair("大きなごみ", "oversized"),
        PatternValuePair("びん・カン", "grassbottle"),
        PatternValuePair("ペットボトル", "petbottle"),
        PatternValuePair("プラマークごみ", "plasticpackaging"),
        PatternValuePair("布類", "cloth"),
        PatternValuePair("古紙", "localcollection.paper"),
        PatternValuePair("家電4品目", "legalrecycling"),
        PatternValuePair("―", "uncollectible"),
        PatternValuePair("パソコン", "uncollectible"),
        PatternValuePair("収集しません", "uncollectible")
    }
    # reader.note_to_category_id
    reader.category_definitions = {
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
        "legalrecycling": { "name": "家電4品目" },
        "uncollectible": { "name": "収集しません" }
    }
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
