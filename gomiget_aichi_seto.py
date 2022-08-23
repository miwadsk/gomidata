#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair

def main(argv):
    reader = GomiReader()
    reader.municipality_id = "232041"
    reader.municipality_name = "愛知県瀬戸市"
    reader.datasource_url = "http://www.city.seto.aichi.jp/docs/2010111003558/"
    reader.target_url_base = ""
    # 1つ目は更新日取得のためだけに指定
    reader.target_pages = [ "http://www.city.seto.aichi.jp/docs/2010111003558/", "http://bunbetsu.setogomi.com/gomi_dic.csv" ]
    reader.datetime_selector = "div.publishedAt"
    reader.datetime_pattern = "ページ更新日：%Y年%m月%d日"
    reader.article_row_selector = None
    reader.article_column_selector = None
    reader.article_index_name = 3
    reader.article_index_category = 5
    reader.article_index_note = 6
    reader.category_to_category_id = [
        PatternValuePair("燃える", "burnable"),
        PatternValuePair("燃えない", "unburnable"),
        PatternValuePair("紙類", "paper"),
        PatternValuePair("缶", "can"),
        PatternValuePair("びん", "grassbottle"),
        PatternValuePair("ペットボトル", "petbottle"),
        PatternValuePair("古布", "cloth"),
        PatternValuePair("粗大", "oversized"),
        PatternValuePair("家電", "legalrecycling"),
        PatternValuePair("水銀", "recyclable.mercury"),
        PatternValuePair("電池類", "recyclable.battery"),
        PatternValuePair("ＰＣ", "uncollectible.computer"),
        PatternValuePair("発火性危険物", "hazardous"),
        PatternValuePair("収集不可", "uncollectible")
    ]
    # reader.note_to_category_id
    reader.category_definitions = {
        "burnable": { "name": "可燃ごみ" },
        "unburnable": { "name": "不燃ごみ" },
        "paper": { "name": "紙類" },
        "can": { "name": "缶" },
        "grassbottle": { "name": "びん" },
        "petbottle": { "name": "ペットボトル" },
        "cloth": { "name": "古布" },
        "oversized": { "name": "粗大ごみ" },
        "legalrecycling": { "name": "家電(家電４品目)" },
        "recyclable": { "name": "資源" },
        "recyclable.mercury": { "name": "資源(水銀)" },
        "recyclable.battery": { "name": "資源(電池類)" },
        "uncollectible.computer": { "name": "収集不可(ＰＣ)" },
        "hazardous": { "name": "発火性危険物" },
        "uncollectible": { "name": "収集不可" }
    }
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
