#!/usr/bin/env python3

import re
import sys
import json
from typing import List, NamedTuple
import gomireader_util as util
from datetime import datetime
from bs4 import BeautifulSoup

def overrides(super_class):
    def overrider(method):
        assert(method.__name__ in dir(super_class))
        return method
    return overrider

class PatternValuePair(object):
    def __init__(self, pattern: str, value: object):
            if pattern[:1] == "/" and pattern[-1:] == "/":
                self.__re = re.compile(pattern[1:-1])
            else:
                self.__re = re.compile("^" + re.sub(r"[\\^$.*+?()[\]{}|]", r"\\$&", pattern) + "$")
            self.__value = value

    def try_get_value(self, text: str) -> object:
        return self.__value if self.__re.fullmatch(text) else None

class GomiArticle(NamedTuple):
    name: str
    category: str
    note: str

class GomiPage(NamedTuple):
    articles: List[GomiArticle]
    updated_at: datetime

class GomiReader(object):
    def __init__(self):
        # 市区町村コード
        self.municipality_id: str = None
        # 自治体名
        self.municipality_name: str = None
        # データ取得元URL
        self.datasource_url: str = None
        # データ取得先URL
        self.target_url_base: str = None
        self.target_pages: str = []
        # 更新日取得
        self.datetime_selector: str = None
        self.datetime_pattern: str = None
        # 品目取得
        self.article_row_selector: str = None
        self.article_column_selector: str = None
        # 分類文字列から分類IDへ変換
        # PatternValueのリスト
        self.category_to_category_id: str = []
        # 備考文字列から分類IDへ変換(分類不明のものが適用対象)(任意)
        # PatternValueのリスト
        self.note_to_category_id: str = None
        # 自治体固有分類定義(任意)
        self.category_definitions: str = None

    def to_json(self) -> str:
        return json.dumps(self.__get_gomidata(), indent=2, ensure_ascii=False)

    def get_gomipage(self, url: str) -> GomiPage:
        """ウェブページの内容からGomiPageを取得します。
        必要に応じてオーバーライドして下さい。"""
        text = util.get_textcontent(url)
        bsoup = BeautifulSoup(text, "html.parser")
        gomipage = GomiPage(
            updated_at=self.get_datetime(bsoup),
            articles=self.get_articles(bsoup)
        )
        return gomipage

    def get_articles(self, bsoup: BeautifulSoup) -> List[GomiArticle]:
        """ウェブページの内容からGomiArticleのリストを取得します。
        必要に応じてオーバーライドして下さい。"""
        articles = []
        for row in bsoup.select(self.article_row_selector):
            cols = row.select(self.article_column_selector)
            texts = list(map(lambda col: col.get_text(strip=True), cols))
            article = self.get_article_from_texts(texts)
            if article:
                articles.append(article)
        return articles

    def get_article_from_texts(self, texts: List[str]):
        """指定の文字列リストからGomiArticleを取得します。
        必要に応じてオーバーライドして下さい。"""
        article = None
        if 2 <= len(texts) and texts[0]:
            article = GomiArticle(
                name=texts[0],
                category=texts[1],
                note=texts[2] if 3 <= len(texts) else None
            )
        return article

    def get_datetime(self, bsoup: BeautifulSoup) -> datetime:
        """ウェブページの内容から更新日時を取得します。
        必要に応じてオーバーライドして下さい。"""
        date = None
        try:
            text = bsoup.select_one(self.datetime_selector).get_text()
            date = util.strptime(text, self.datetime_pattern)
        except:
            pass
        return date

    def get_category_id(self, category: str, note: str) -> str:
        """分類文字列または備考文字列から分類IDを取得します。
        必要に応じてオーバーライドして下さい。"""
        category_id = self.try_get_value_in_patterns(self.category_to_category_id, category)
        if not category_id and self.note_to_category_id:
            # 備考文字列からの特定を試みる
            category_id = self.try_get_value_in_patterns(self.note_to_category_id, note)
        return category_id or "unknown"

    def __get_target_urls(self) -> List[str]:
        """データ取得対象URLのリストを取得します。"""
        return list(map(lambda page: self.target_url_base + page, self.target_pages))

    def __get_gomidata(self) -> dict:
        """辞書形式のごみ分別データを取得します。"""
        urls = self.__get_target_urls()
        gomipages = list(map(lambda url: self.__get_gomipage(url), urls))
        return self.__get_gomidata_from_gomipages(gomipages)

    def __get_gomipage(self, url: str) -> GomiPage:
        """ウェブページの内容から作成したGomiPageを取得します。"""
        print(url, file=sys.stderr, end="")
        gomipage = self.get_gomipage(url)
        if gomipage:
            print(f" -> OK ({len(gomipage.articles)})", file=sys.stderr)
        else:
            print(" -> ERROR", file=sys.stderr)
        return gomipage

    def __get_gomidata_from_gomipages(self, gomipages: List[GomiPage]) -> dict:
        """GomiPageのリストから辞書形式のごみ分別データを取得します。"""
        updated_at = datetime.min
        article_entries = []
        for gomipage in gomipages:
            updated_at = max(updated_at, gomipage.updated_at or datetime.min)
            for page_article in gomipage.articles:
                article_entry = {}
                article_entry["name"] = util.normalized(page_article.name)
                article_entry["nameKana"] = util.to_hiragana(page_article.name)
                article_entry["categoryId"] = self.get_category_id(page_article.category, page_article.note)
                if page_article.note:
                    article_entry["note"] = page_article.note
                article_entries.append(article_entry)
        gomidata = {}
        gomidata["municipalityId"] = self.municipality_id
        gomidata["municipalityName"] = self.municipality_name
        if self.datasource_url:
            gomidata["datasourceUrl"] = self.datasource_url
        if updated_at != datetime.min:
            gomidata["updatedAt"] = updated_at.strftime("%Y-%m-%d")
        if self.category_definitions:
            gomidata["categoryDefinitions"] = self.category_definitions
        gomidata["articles"] = article_entries
        return gomidata

    def try_get_value_in_patterns(self, patterns: List[PatternValuePair], text: str) -> object:
        for pattern in patterns:
            value = pattern.try_get_value(text)
            if value:
                return value
        return None

def test():
    reader = GomiReader()
    reader.municipality_id = "9999"
    reader.municipality_name = "test"
    reader.datasource_url = ""
    reader.target_url_base = "file:./"
    reader.target_pages = [ "test.html" ]
    reader.datetime_selector = "p.update"
    reader.datetime_pattern = "更新日:%Y年%m月%d日"
    reader.article_row_selector = "caption ~ tr"
    reader.article_column_selector = "td"
    reader.category_to_category_id = [
        PatternValuePair("可燃ごみ", "burnable"),
        PatternValuePair("不燃ごみ", "unburnable"),
        PatternValuePair("資源", "recyclable"),
        PatternValuePair("危険ごみ", "hazardous"),
        PatternValuePair("粗大ごみ", "oversized"),
        PatternValuePair("家電リサイクル法対象品目", "legalrecycling"),
        PatternValuePair("市で処理できません。", "uncollectible")
    ]
    print(reader.to_json())

if __name__ == "__main__":
    test()
