#!/usr/bin/env python3

import sys
import requests
import pykakasi
import mojimoji
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
        response = requests.get(uri)
        response.encoding = response.apparent_encoding
        return BeautifulSoup(response.text, "html.parser")
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
    t = hiragana_converter.do(text)
    return "".join(map(lambda c: ALPHABET_TO_HIRAGANA.get(c, c), t.lower()))

# 漢字かな英字まじり文字列をローマ字(ヘボン式)に変換します
def to_roman(text) -> str:
    return roman_converter.do(text).lower()

def test():
    try:
        bs = get_bsoup("https://www.google.com/")
        assert(bs != None)
        title = bs.select_one("title").get_text()
        assert(title == "Google")
        hiragana = text_to_hiragana("ひラ仮Na")
        assert(hiragana == "ひらかりえぬえー")
        roman = text_to_roman("ひラ仮Ｎa")
        assert(roman == "hirakarina")
        print("Success")
    except Exception as ex:
        print("Failed at", sys.exc_info()[2].tb_lineno)

if __name__ == "__main__":
    test()
