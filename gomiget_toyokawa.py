#!/usr/bin/env python3

import sys
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

CATEGORY_MAP = {
    "可燃ごみ": "burnable",
    "不燃ごみ": "nonburnable",
    "資源": "recyclable",
    "危険ごみ": "hazardous",
    "粗大ごみ": "oversized",
    "家電リサイクル法対象品目": "specificrecycling",
    "市で処理できません。": "uncollectible"
}

BASE_URI = "https://www.city.toyokawa.lg.jp/smph/kurashi/gomirecycle/gomihayamihyo/"
TARGET_PAGES = ["agyo.html", "kagyo.html", "sagyo.html", "tagyo.html", "nagyo.html", "hagyo.html", "magyo.html", "yagyo.html", "ragyo.html", "wagyo.html"]

def get_page_text(uri):
    try:
        response = requests.get(uri)
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return None

def get_articles(bsoup):
    articles = []
    rows = bsoup.select("caption ~ tr")
    for row in rows:
        cols = row.select("td")
        if len(cols) == 3:
            t = list(map(lambda col: col.get_text(strip=True), cols))
            article = {
                "name": t[0],
                "category": CATEGORY_MAP.get(t[1], "unknown"),
                "note": t[2]
            }
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
        uri = BASE_URI + page
        page_text = get_page_text(uri)
        if page_text:
            bsoup = BeautifulSoup(page_text, "html.parser")
            articles.extend(get_articles(bsoup))
            updated_at = get_updated_at(bsoup)
            if last_updated_at < updated_at:
                last_updated_at = updated_at
    result = {
         "cityName": "豊川市",
         "updatedAt": last_updated_at.strftime("%Y-%m-%d"),
         "articles": articles
    }
    json_text = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_text)

if __name__ == "__main__":
    main(sys.argv)
