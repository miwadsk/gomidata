#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair, GomiArticle, overrides

class AichiToyohashiGomiReader(GomiReader):
    @overrides(GomiReader)
    def get_article_from_texts(self, texts):
        article = None
        if 5 <= len(texts):
            article = GomiArticle(
                name=texts[0],
                category=texts[3],
                note=texts[-1:][0]
            )
        return article

def main(argv):
    reader = AichiToyohashiGomiReader()
    reader.municipality_id = "232017"
    reader.municipality_name = "愛知県豊橋市"
    reader.datasource_url = "http://www2.city.toyohashi.aichi.jp/kankyo/dictionary/index.html"
    reader.target_url_base = "http://www2.city.toyohashi.aichi.jp/kankyo/dictionary/search.cgi?mode=index&key="
    reader.target_pages = [ "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
    reader.datetime_selector = None
    reader.datetime_pattern = None
    reader.article_row_selector = "form > table > tr > td > table > tr > td > table > tr"
    reader.article_column_selector = "td"
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
        PatternValuePair("家電４品目", "legalrecycling"),
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
        "legalrecycling": { "name": "家電４品目" },
        "uncollectible": { "name": "収集しません" }
    }
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
