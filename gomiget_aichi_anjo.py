#!/usr/bin/env python3

import sys
from gomireader import GomiReader, PatternValuePair

def main(argv):
    reader = GomiReader()
    reader.municipality_id = "232122"
    reader.municipality_name = "愛知県安城市"
    reader.datasource_url = "https://www.city.anjo.aichi.jp/kurasu/gomi/gomidashi/gomidasu/index.html"
    reader.target_url_base = "https://www.city.anjo.aichi.jp/kurasu/gomi/gomidashi/gomidasu/"
    reader.target_pages = [
        "a.html", "i.html", "u.html", "e.html", "o.html",
        "ka.html", "ki.html", "ku.html", "ke.html", "ko.html",
        "sa.html", "shi.html", "su.html", "se.html", "so.html",
        "ta.html", "chi.html", "tsu.html", "te.html", "to.html",
        "na.html", "ni.html", "nu.html", "ne.html", "no.html",
        "ha.html", "hi.html", "fu.html", "he.html", "ho.html",
        "ma.html", "mi.html", "mu.html", "me.html", "mo.html",
        "ya.html", "yu.html", "yo.html",
        "ra.html", "ri.html", "ru.html", "re.html", "ro.html",
        "wa.html"
    ]
    reader.datetime_selector = "p#tmp_update"
    reader.datetime_pattern = "更新日：%Y年%m月%d日"
    reader.article_row_selector = "p ~ table > tbody > tr"
    reader.article_column_selector = "td"
    reader.category_to_category_id = [
        PatternValuePair("燃やせるごみ", "burnable"),
        PatternValuePair("燃やせないごみ", "unburnable"),
        PatternValuePair("プラスチック製容器包装", "plasticpackaging"),
        PatternValuePair(r"/拠点.*品目/", "pointcollection"),
        PatternValuePair(r"/資源ごみ（(びん|缶類|びん・缶類)）/", "grassbottle"),
        PatternValuePair("資源ごみ（破砕困難ごみ・危険ごみ）", "hazardous"),
        PatternValuePair("資源ごみ（古着）", "cloth"),
        PatternValuePair("資源ごみ（古紙）", "paper"),
        PatternValuePair("粗大ごみ", "oversized"),
        PatternValuePair("持ち込みごみ", "oversized")
    ]
    reader.note_to_category_id = {
        PatternValuePair(r"/家電リサイクル法対象品目です.*/", "legalrecycling"),
        PatternValuePair(r"/.*/", "uncollectible")
    }
    reader.category_definitions = {
        "burnable": { "name": "燃やせるごみ" },
        "unburnable": { "name": "燃やせないごみ" },
        "plasticpackaging": { "name": "プラスチック製容器包装" },
        "pointcollection": { "name": "拠点回収品目" },
        "grassbottle": { "name": "びん・缶類" },
        "hazardous": { "name": "破砕困難ごみ・危険ごみ" },
        "cloth": { "name": "古着" },
        "paper": { "name": "古紙" },
        "oversized": { "name": "粗大ごみ・持ち込みごみ" },
        "legalrecycling": { "name": "家電リサイクル法対象品目" },
        "uncollectible": { "name": "回収できません" }
    }
    print(reader.to_json())

if __name__ == "__main__":
    main(sys.argv)
