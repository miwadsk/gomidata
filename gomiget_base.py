#!/usr/bin/env python3

import re
import sys
import json
import gomiget_util as gu
from datetime import datetime
from bs4 import BeautifulSoup

class GomigetParameter(object):
    prefecture_name = None
    municipality_name = None
    data_source_url = None
    target_url_base = None
    target_pages = None
    datetime_selector = None
    datetime_pattern = None
    article_row_selector = None
    article_column_selector = None
    text_to_category_id = None
    note_to_category_id = None
    local_category_definition = None

class GomiEntry(object):
    article_name = None
    category_id = None
    note = None

class GomigetBase(object):
    def __init__(self, parameter):
        self.__parameter = parameter

    def as_json(self) -> str:
        data = self.__get_data()
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def __get_data(self) -> dict:
        updated_at = datetime.min
        articles = []
        for page in self.__parameter.target_pages:
            url = self.__parameter.target_url_base + page
            print(url, file=sys.stderr)
            bsoup = gu.get_bsoup(url)
            if bsoup:
                articles.extend(self.__get_articles(bsoup))
                updated_at = max(updated_at, self.__get_datetime(bsoup))

        data = {}
        data["prefectureName"] = self.__parameter.prefecture_name
        data["municipalityName"] = self.__parameter.municipality_name
        if self.__parameter.data_source_url:
            data["dataSourceUrl"] = self.__parameter.data_source_url
        if updated_at != datetime.min:
            data["updatedAt"] = updated_at.strftime("%Y-%m-%d")
        if self.__parameter.local_category_definition:
            data["localCategoryDefinition"] = self.__parameter.local_category_definition
        data["articles"] = articles

        return data

    def __get_articles(self, bsoup) -> list:
        articles = []
        rows = bsoup.select(self.__parameter.article_row_selector)
        for row in rows:
            columns = row.select(self.__parameter.article_column_selector)
            column_texts = list(map(lambda col: col.get_text(strip=True), columns))
            gomientry = self.__get_gomientry(column_texts)
            if gomientry:
                name = gu.normalized(gomientry.article_name)
                article = {
                    "name": name,
                    "nameKana": gu.to_hiragana(name),
                    "categoryId": gomientry.category_id
                }
                if gomientry.note:
                    article["note"] = gomientry.note
                articles.append(article)
        return articles
    
    def __get_gomientry(self, texts) -> GomiEntry:
        if 2 <= len(texts):
            gomientry = GomiEntry()
            gomientry.article_name = texts[0]
            gomientry.note = texts[2] if 3 <= len(texts) else None
            gomientry.category_id = self.__get_category_id(texts[1], gomientry.note)
            return gomientry
        else:
            return None

    def __get_category_id(self, text, note) -> str:
        category_id = self.__parameter.text_to_category_id.get(text, "unknown")
        if category_id == "unknown" and self.__parameter.note_to_category_id:
            for entry in self.__parameter.note_to_category_id:
                if note and re.fullmatch(entry["pattern"], note):
                    category_id = entry["category_id"]
                    break
        return category_id

    def __get_datetime(self, bsoup) -> datetime:
        try:
            text = bsoup.select_one(self.__parameter.datetime_selector).get_text()
            return gu.strptime(text, self.__parameter.datetime_pattern)
        except:
            return datetime.min

def main(args):
    print(Gomiget().get_json())

if __name__ == "__main__":
    main(sys.argv)
