#!/usr/bin/env python3

import sys
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pykakasi
import mojimoji

CATEGORY_MAP = {
    "可燃ごみ": "burnable",
    "不燃ごみ": "unburnable",
    "粗大ごみ": "oversized",
    "発火性危険物": "hazardous",
    "紙製容器包装": "recyclable-paperpack",
    "プラ容器包装": "recyclable-plasticpack",
    "空きびん": "recyclable-bottole",
    "空き缶": "recyclable-can",
    "紙パック": "selfcarrying",
    "食用油": "selfcarrying",
    "小型家電": "selfcarrying"
}

SOURCE_URI = "http://www.city.nagoya.jp/kurashi/category/5-6-22-0-0-0-0-0-0-0.html"
BASE_URI = "http://www.city.nagoya.jp/kankyo/page/"
TARGET_PAGES = [ "0000066278.html", "0000066280.html", "0000066282.html", "0000066283.html", "0000066302.html", "0000066303.html", "0000066305.html", "0000066307.html", "0000066308.html", "0000066309.html" ]
ROMAN_TO_KANA = { "a": "えー", "b": "びー", "c": "しー", "d": "でぃー", "e": "いー", "f": "えふ", "g": "じー", "h": "えいち", "i": "あい", "j": "じぇー", "k": "けー", "l": "える", "m": "えむ", "n": "えぬ", "o": "おー", "p": "ぴー", "q": "きゅー", "r": "あーる", "s": "えす", "t": "てぃー", "u": "ゆー", "v": "ぶい", "w": "だぶりゅ", "x": "えっくす", "y": "わい", "z": "ぜっと" }

def get_page_text(uri):
    try:
        response = requests.get(uri)
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return None

def roman_to_kana(text):
    return "".join(map(lambda c: ROMAN_TO_KANA.get(c, c), text.lower()))

def get_articles(bsoup):
    kaka = pykakasi.kakasi()
    kaka.setMode("K", "H")
    kaka.setMode("J", "H")
    converter = kaka.getConverter()
    articles = []
    rows = bsoup.select("tbody > tr")
    for row in rows:
        cols = row.select("td")
        if len(cols) == 3:
            t = list(map(lambda col: col.get_text(strip=True), cols))
            name = mojimoji.zen_to_han(t[0], kana=False)
            name_kana = roman_to_kana(converter.do(name))
            category = CATEGORY_MAP.get(t[1], "unknown")
            note = t[2]

            if category == "unknown":
                if "家電リサイクル法対象" in note:
                    category = "legalrecycling"
                elif "ご相談ください" in note:
                    category = "uncollectible"

            article = {
                "name": name,
                "nameKana": name_kana,
                "category": category
            }
            if note:
                article["note"] = note

            articles.append(article)
    return articles

def get_updated_at(bsoup):
    try:
        s = bsoup.select_one("span.syosai_hiduke").get_text()
        return datetime.strptime(s, "最終更新日：%Y年%m月%d日")
    except:
        return None

def main(args):
    last_updated_at = datetime.min
    articles = []
    for page in TARGET_PAGES:
        uri = BASE_URI + page
        page_text = get_page_text(uri)
        if page_text:
            bsoup = BeautifulSoup(page_text, "html.parser")
            articles.extend(get_articles(bsoup))
            updated_at = get_updated_at(bsoup)
            if updated_at and last_updated_at < updated_at:
                last_updated_at = updated_at
    result = {
         "municipality": "名古屋市",
         "updatedAt": last_updated_at.strftime("%Y-%m-%d"),
         "sourceUrl": SOURCE_URI,
         "articles": articles
    }
    json_text = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_text)

if __name__ == "__main__":
    main(sys.argv)
