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
    "資源": "recyclable",
    "危険ごみ": "hazardous",
    "粗大ごみ": "oversized",
    "家電リサイクル法対象品目": "legalrecycling",
    "市で処理できません。": "uncollectible"
}

SOURCE_URI = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
TARGET_URI_BASE = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
TARGET_PAGES = ["agyo.html", "kagyo.html", "sagyo.html", "tagyo.html", "nagyo.html", "hagyo.html", "magyo.html", "yagyo.html", "ragyo.html", "wagyo.html"]
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
    kakaHira = pykakasi.kakasi()
    kakaHira.setMode("K", "H")
    kakaHira.setMode("J", "H")
    converterHira = kakaHira.getConverter()
    kakaRoman = pykakasi.kakasi()
    kakaRoman.setMode("H", "a")
    kakaRoman.setMode("K", "a")
    kakaRoman.setMode("J", "a")
    converterRoman = kakaRoman.getConverter()
    articles = []
    rows = bsoup.select("caption ~ tr")
    for row in rows:
        cols = row.select("td")
        if len(cols) == 3:
            t = list(map(lambda col: col.get_text(strip=True), cols))
            name = mojimoji.zen_to_han(t[0], kana=False)
            name_kana = roman_to_kana(converterHira.do(name))
            name_roman = converterRoman.do(name)
            categoryId = CATEGORY_MAP.get(t[1], "unknown")
            note = t[2]
            article = {
                "name": name,
                "nameKana": name_kana,
                "nameRoman": name_roman,
                "categoryId": categoryId
            }
            if note:
                article["note"] = note

            articles.append(article)
    return articles

def get_updated_at(bsoup):
    try:
        s = bsoup.select_one("p.update").get_text()
        return datetime.strptime(s, "更新日:%Y年%m月%d日")
    except:
        return None

def main(args):
    last_updated_at = datetime.min
    articles = []
    for page in TARGET_PAGES:
        uri = TARGET_URI_BASE + page
        page_text = get_page_text(uri)
        if page_text:
            bsoup = BeautifulSoup(page_text, "html.parser")
            articles.extend(get_articles(bsoup))
            updated_at = get_updated_at(bsoup)
            if last_updated_at < updated_at:
                last_updated_at = updated_at
    result = {
         "municipality": "豊川市",
         "updatedAt": last_updated_at.strftime("%Y-%m-%d"),
         "sourceUrl": SOURCE_URI,
         "articles": articles
    }
    json_text = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_text)

if __name__ == "__main__":
    main(sys.argv)
