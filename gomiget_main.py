#!/usr/bin/env python3

import re
import sys
import json
import gomiget_util as gu
from datetime import datetime
from bs4 import BeautifulSoup

class PatternValue(object):
    def __init__(self, pattern, value):
            if pattern[:1] == "/" and pattern[-1:] == "/":
                self.__re = re.compile(pattern[1:-1])
            else:
                self.__re = re.compile("^" + re.sub(r"[\\^$.*+?()[\]{}|]", r"\\$&", pattern) + "$")
            self.__value = value

    def try_get_value(self, text) -> object:
        return self.__value if self.__re.fullmatch(text) else None

    @staticmethod
    def try_get_value_in_patterns(patterns, text):
        for pattern in patterns:
            value = pattern.try_get_value(text)
            if value:
                return value
        return None

class Gomiget(object):
    def __init__(self):
        # 市区町村コード
        self.municipality_id = None
        # 自治体名
        self.municipality_name = None
        # データ取得元URL
        self.datasource_url = None
        # データ取得先URL
        self.target_url_base = None
        self.target_pages = []
        # 更新日取得
        self.datetime_selector = None
        self.datetime_pattern = None
        # 品目取得
        self.article_row_selector = None
        self.article_column_selector = None
        # 分類文字列から分類IDへ変換
        # PatternValueのリスト
        self.category_to_category_id = []
        # 備考文字列から分類IDへ変換(分類不明のものが適用対象)(任意)
        # PatternValueのリスト
        self.note_to_category_id = None
        # 自治体固有分類定義(任意)
        self.category_definitions = None

    def to_json(self) -> str:
        gomidata = self.__get_gomidata()
        return json.dumps(gomidata, indent=2, ensure_ascii=False)
    
    def __get_gomidata(self) -> dict:
        """設定されているパラメータを元にごみ分別データを取得します。"""
        updated_at = datetime.min
        articles = []
        for page in self.target_pages:
            url = self.target_url_base + page
            print(url, file=sys.stderr, end="")
            bsoup = gu.get_bsoup(url)
            if bsoup:
                page_articles = self.__get_articles(bsoup)
                articles.extend(page_articles)
                updated_at = max(updated_at, self.__get_datetime(bsoup))
                print(f" -> OK ({len(page_articles)})", file=sys.stderr)
            else:
                print(" -> ERROR", file=sys.stderr)
        gomidata = {}
        gomidata["municipalityId"] = self.municipality_id
        gomidata["municipalityName"] = self.municipality_name
        if self.datasource_url:
            gomidata["datasourceUrl"] = self.datasource_url
        if updated_at != datetime.min:
            gomidata["updatedAt"] = updated_at.strftime("%Y-%m-%d")
        if self.category_definitions:
            gomidata["categoryDefinitions"] = self.category_definitions
        gomidata["articles"] = articles
        return gomidata

    def __get_articles(self, bsoup) -> list:
        """ウェブページの内容から品目情報のリストを取得します。"""
        articles = []
        rows = bsoup.select(self.article_row_selector)
        for row in rows:
            columns = row.select(self.article_column_selector)
            column_texts = list(map(lambda col: col.get_text(strip=True), columns))
            if 2 <= len(column_texts):
                name = column_texts[0]
                category = column_texts[1]
                note = column_texts[2] if 3 <= len(column_texts) else None
                article = {
                    "name": gu.normalized(name),
                    "nameKana": gu.to_hiragana(name),
                    "categoryId": self.__get_category_id(category, note)
                }
                if note:
                    article["note"] = note
                articles.append(article)
        return articles

    def __get_category_id(self, category, note) -> str:
        """分類文字列または備考文字列から分類IDを取得します。"""
        category_id = PatternValue.try_get_value_in_patterns(self.category_to_category_id, category)
        if not category_id and self.note_to_category_id:
            # 備考文字列からの特定を試みる
            category_id = PatternValue.try_get_value_in_patterns(self.note_to_category_id, note)
        return category_id or "unknown"

    def __get_datetime(self, bsoup) -> datetime:
        """ウェブページの内容から更新日時を取得します。"""
        try:
            text = bsoup.select_one(self.datetime_selector).get_text()
            return gu.strptime(text, self.datetime_pattern)
        except:
            return datetime.min

def main(args):
    gomiget = Gomiget()
    gomiget.municipality_id = "9999"
    gomiget.municipality_name = "test"
    gomiget.datasource_url = ""
    gomiget.target_url_base = "file:./"
    gomiget.target_pages = [ "test.html" ]
    gomiget.datetime_selector = "p.update"
    gomiget.datetime_pattern = "更新日:%Y年%m月%d日"
    gomiget.article_row_selector = "caption ~ tr"
    gomiget.article_column_selector = "td"
    gomiget.category_to_category_id = [
        PatternValue("可燃ごみ", "burnable"),
        PatternValue("不燃ごみ", "unburnable"),
        PatternValue("資源", "recyclable"),
        PatternValue("危険ごみ", "hazardous"),
        PatternValue("粗大ごみ", "oversized"),
        PatternValue("家電リサイクル法対象品目", "legalrecycling"),
        PatternValue("市で処理できません。", "uncollectible")
    ]
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
