#!/usr/bin/env python3

import sys
from typing import List
from gomireader import GomiReader, GomiPage, GomiArticle, PatternValuePair, overrides
import gomireader_util as util
import csv
from bs4 import BeautifulSoup

class AichiSetoGomiReader(GomiReader):
    @overrides(GomiReader)
    def get_gomipage(self, url: str) -> GomiPage:
        text = util.get_textcontent(url)
        if url.endswith(".csv"):
            rows = csv.reader(text.splitlines(), delimiter=",")
            next(rows)
            gomipage = GomiPage(
                updated_at=None,
                articles=self.get_articles_csv(rows)
            )
        else:
            bsoup = BeautifulSoup(text, "html.parser")
            gomipage = GomiPage(
                updated_at=self.get_datetime(bsoup),
                articles=[]
            )
        return gomipage

    def get_articles_csv(self, rows) -> List[GomiArticle]:
        articles = []
        for row in rows:
            article = self.get_article_from_texts_csv(row)
            if article:
                articles.append(article)
        return articles

    def get_article_from_texts_csv(self, texts):
        article = None
        if 7 <= len(texts):
            article = GomiArticle(
                name=texts[3],
                category=texts[5],
                note=texts[6]
            )
        return article

def main(argv):
    reader = AichiSetoGomiReader()
    reader.municipality_id = "232041"
    reader.municipality_name = "愛知県瀬戸市"
    reader.datasource_url = "http://www.city.seto.aichi.jp/docs/2010111003558/"
    reader.target_url_base = ""
    # 1つ目は更新日取得のためだけに指定
    reader.target_pages = [ "http://www.city.seto.aichi.jp/docs/2010111003558/", "http://bunbetsu.setogomi.com/gomi_dic.csv" ]
    reader.datetime_selector = "div.publishedAt"
    reader.datetime_pattern = "ページ更新日：%Y年%m月%d日"
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
