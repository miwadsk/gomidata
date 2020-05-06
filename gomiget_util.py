#!/usr/bin/env python3

import re
import sys
import requests
import pykakasi
import mojimoji
from datetime import datetime
from bs4 import BeautifulSoup

ALPHABET_TO_HIRAGANA = {
    "a": "えー", "b": "びー", "c": "しー", "d": "でぃー", "e": "いー",
    "f": "えふ", "g": "じー", "h": "えいち", "i": "あい", "j": "じぇー",
    "k": "けー", "l": "える", "m": "えむ", "n": "えぬ", "o": "おー",
    "p": "ぴー", "q": "きゅー", "r": "あーる", "s": "えす", "t": "てぃー",
    "u": "ゆー", "v": "ぶい", "w": "だぶりゅ", "x": "えっくす", "y": "わい",
    "z": "ぜっと"
}

kakasi_hiragana = pykakasi.kakasi()
kakasi_hiragana.setMode("K", "H")
kakasi_hiragana.setMode("J", "H")
hiragana_converter = kakasi_hiragana.getConverter()

kakasi_roman = pykakasi.kakasi()
kakasi_roman.setMode("H", "a")
kakasi_roman.setMode("K", "a")
kakasi_roman.setMode("J", "a")
roman_converter = kakasi_roman.getConverter()

def get_bsoup(uri) -> BeautifulSoup:
    try:
        text = None
        if uri.startswith("file:"):
            with open(uri[5:], "r", encoding="utf-8") as f:
                text = f.read()
        else:
            response = requests.get(uri)
            response.encoding = response.apparent_encoding
            text = response.text
        return BeautifulSoup(text, "html.parser")
    except:
        return None

def to_halfwidth(text, digit, ascii, kana) -> str:
    return mojimoji.zen_to_han(text, digit=digit, ascii=ascii, kana=kana)

def to_fullwidth(text, digit, ascii, kana) -> str:
    return mojimoji.han_to_zen(text, digit=digit, ascii=ascii, kana=kana)

# 数字/英字は半角、カタカナは全角に揃えます
def normalized(text) -> str:
    t = to_fullwidth(text, digit=False, ascii=False, kana=True)
    t = to_halfwidth(text, digit=True, ascii=True, kana=False)
    return t

# 漢字かな英字まじり文字列をひらがなに変換します
def to_hiragana(text) -> str:
    t = hiragana_converter.do(normalized(text))
    return "".join(map(lambda c: ALPHABET_TO_HIRAGANA.get(c, c), t.lower()))

# 漢字かな英字まじり文字列をローマ字(ヘボン式)に変換します
def to_roman(text) -> str:
    return roman_converter.do(normalized(text)).lower()

def on_matched(match) -> str:
    jeras = {"昭和": 1926 - 1, "平成": 1989 - 1, "令和": 2019 - 1}
    year = jeras.get(match.group(1))
    return str(year + int(match.group(2))) if year else match.group()

def strptime(text, pattern) -> datetime:
    text = re.sub(r"(\S\S)\s*(\d+)", on_matched, text)
    return datetime.strptime(text, pattern)

def test():
    bs = get_bsoup("https://www.google.com/")
    assert(bs != None)
    title = bs.select_one("title").get_text()
    assert(title == "Google")
    hiragana = to_hiragana("ひラ仮Na")
    assert(hiragana == "ひらかりえぬえー")
    roman = to_roman("ひラ仮Ｎa")
    assert(roman == "hirakarina")
    date = strptime("最終更新日平成25年11月21日", "最終更新日%Y年%m月%d日")
    assert(date.strftime("%Y-%m-%d") == "2013-11-21")
    date = strptime("最終更新日2025年11月21日", "最終更新日%Y年%m月%d日")
    assert(date.strftime("%Y-%m-%d") == "2025-11-21")
    print("Success")

if __name__ == "__main__":
    test()
