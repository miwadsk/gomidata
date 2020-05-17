#!/usr/bin/env python3

import re
import sys
import json
import tabula
# import gomireader_util as util
from gomireader import GomiReader, PatternValuePair, GomiPage, GomiArticle, overrides

class AichiNishioGomiReader(GomiReader):
    @overrides(GomiReader)
    def get_gomipage(self, url: str) -> GomiPage:
        df = tabula.read_pdf(url)
        gomipage = GomiPage(
            updated_at=self.get_datetime(df),
            articles=self.get_articles(df)
        )
        return gomipage

    @overrides(GomiReader)
    def get_datetime(self, df):
        return None

    @overrides(GomiReader)
    def get_articles(self, df):
        # ['あ' 'アイロン' nan '資源物 (小型家電) 資源コンテナに入らないものは粗大ごみ' nan 'す' '炊飯器' '資源物 (小型家電)' nan '内釜は資源物(なべ・かまなどの金物類)']
        left_articles = []
        right_articles = []
        for value in df[0].values:
            # 左側
            tokens = value[3].replace(" (", "(").split(" ", 1)
            article = GomiArticle(
                name=str(value[1]),
                category=tokens[0],
                note=tokens[1] if 2 <= len(tokens) else None
            )
            left_articles.append(article)

            # 右側
            article = GomiArticle(
                name=str(value[6]),
                category=str(value[7]),
                note=str(value[9])
            )
            right_articles.append(article)
        articles = left_articles + right_articles
        return articles

def main(args):
    reader = AichiNishioGomiReader()
    reader.municipality_id = "232131"
    reader.municipality_name = "愛知県西尾市"
    reader.datasource_url = None
    reader.target_url_base = "file:data/nishio/"
    reader.target_pages = [ "20191202-092059.pdf" ]
    # reader.datetime_selector = None
    # reader.datetime_pattern = None
    # reader.article_row_selector = None
    # reader.article_column_selector = None
    reader.category_to_category_id = {
        PatternValuePair("/.*/", "burnable")
    }
    # reader.note_to_category_id
    reader.category_definitions = {
        "burnable": { "name": "もやすごみ" },
    }
    print(reader.to_json())

if __name__ == "__main__":
    # main(sys.argv)
    main(["", "20191202-092059.pdf"])
