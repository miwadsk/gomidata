#!/usr/bin/env python3

import re
import sys
import json
import gomiget_util as gu
from datetime import datetime
from bs4 import BeautifulSoup

class GomigetSetting(object):
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
    def __init__(self, setting):
        self.__setting = setting
        self.__data = None

    def as_json(self) -> str:
        self.__data = self.__data or self.__get_data()
        return json.dumps(self.__data, indent=2, ensure_ascii=False)
    
    def __get_data(self) -> dict:
        updated_at = datetime.min
        articles = []
        for page in self.__setting.target_pages:
            url = self.__setting.target_url_base + page
            print(url, file=sys.stderr)
            bsoup = gu.get_bsoup(url)
            if bsoup:
                articles.extend(self.__get_articles(bsoup))
                updated_at = max(updated_at, self.__get_updated_datetime(bsoup))

        data = {}
        data["prefectureName"] = self.__setting.prefecture_name
        data["municipalityName"] = self.__setting.municipality_name
        if self.__setting.data_source_url:
            data["dataSourceUrl"] = self.__setting.data_source_url
        if updated_at != datetime.min:
            data["updatedAt"] = updated_at.strftime("%Y-%m-%d")
        if self.__setting.local_category_definition:
            data["localCategoryDefinition"] = self.__setting.local_category_definition
        data["articles"] = articles

        return data

    def __get_articles(self, bsoup) -> list:
        articles = []
        rows = bsoup.select(self.__setting.article_row_selector)
        for row in rows:
            columns = row.select(self.__setting.article_column_selector)
            column_texts = list(map(lambda col: col.get_text(strip=True), columns))
            gomientry = self.__get_gomientry(column_texts)
            if gomientry:
                name = gu.normalized(gomientry.article_name)
                article = {
                    "name": name,
                    "nameKana": gu.to_hiragana(name),
                    "nameRoman": gu.to_roman(name),
                    "categoryId": gomientry.category_id
                }
                if gomientry.note:
                    article["note"] = gomientry.note
                articles.append(article)
        return articles
    
    def __get_gomientry(self, texts) -> dict:
        if 3 <= len(texts):
            gomientry = GomiEntry()
            gomientry.article_name = texts[0]
            gomientry.category_id = self.__get_category_id(texts[1], texts[2])
            gomientry.note = texts[2]
            return gomientry
        else:
            return None

    def __get_category_id(self, text, note) -> str:
        category_id = self.__setting.text_to_category_id.get(text, "unknown")
        if category_id == "unknown" and self.__setting.note_to_category_id:
            for entry in self.__setting.note_to_category_id:
                if re.fullmatch(entry["pattern"], note):
                    category_id = entry["category_id"]
                    break
        return category_id

    def __get_updated_datetime(self, bsoup) -> str:
        try:
            text = bsoup.select_one(self.__setting.datetime_selector).get_text()
            return datetime.strptime(text, self.__setting.datetime_pattern)
        except:
            return None

def main(args):
    print(Gomiget().get_json())

if __name__ == "__main__":
    main(sys.argv)
