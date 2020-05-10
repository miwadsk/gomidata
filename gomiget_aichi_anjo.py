#!/usr/bin/env python3

import sys
from gomiget_main import Gomiget, PatternValue

def main(argv):
    gomiget = Gomiget()
    gomiget.municipality_id = "232122"
    gomiget.municipality_name = "愛知県安城市"
    gomiget.datasource_url = "https://www.city.anjo.aichi.jp/kurasu/gomi/gomidashi/gomidasu/index.html"
    gomiget.target_url_base = "https://www.city.anjo.aichi.jp/kurasu/gomi/gomidashi/gomidasu/"
    gomiget.target_pages = [
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
    gomiget.datetime_selector = "p#tmp_update"
    gomiget.datetime_pattern = "更新日：%Y年%m月%d日"
    gomiget.article_row_selector = "p ~ table > tbody > tr"
    gomiget.article_column_selector = "td"
    gomiget.category_to_category_id = [
        PatternValue("燃やせるごみ", "burnable"),
        PatternValue("燃やせないごみ", "unburnable"),
        PatternValue("プラスチック製容器包装", "plasticpackaging"),
        PatternValue(r"/拠点.*品目/", "pointcollection"),
        PatternValue(r"/資源ごみ（(びん|缶類|びん・缶類)）/", "grassbottle"),
        PatternValue("資源ごみ（破砕困難ごみ・危険ごみ）", "hazardous"),
        PatternValue("資源ごみ（古着）", "cloth"),
        PatternValue("資源ごみ（古紙）", "paper"),
        PatternValue("粗大ごみ", "oversized"),
        PatternValue("持ち込みごみ", "oversized")
    ]
    gomiget.note_to_category_id = {
        PatternValue(r"/家電リサイクル法対象品目です.*/", "legalrecycling"),
        PatternValue(r"/.*/", "uncollectible")
    }
    gomiget.category_definitions = {
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
    print(gomiget.to_json())

if __name__ == "__main__":
    main(sys.argv)
