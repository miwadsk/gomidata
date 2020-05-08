#!/usr/bin/env python3

import re
import sys
import json

class Result(object):
    def __init__(self):
        self.category_count = 0
        self.article_count = 0
        self.unknown_count = 0
        self.errors = []

    def output(self, title):
        print(title)
        print(f"Category: {self.category_count}", end=" | ")
        print(f"Article: {self.article_count}", end=" | ")
        print(f"Unknown: {self.unknown_count}")
        if 0 < len(self.errors):
            print(f"ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(error)

def verify_gomidata(json):
    result = Result()
    if not json.get("municipalityId"):
        result.errors.append("'municipalityId' is missing")
    if not json.get("municipalityName"):
        result.errors.append("'municipalityName' is missing")

    category_definitions = json.get("categoryDefinitions")
    if not category_definitions:
        result.errors.append("'categoryDefinitions' is missing")
    else:
        result.category_count = len(category_definitions)

    articles = json.get("articles")
    if not articles:
        result.errors.append("'articles' is missing")
    else:
        result.article_count = len(articles)
        result.unknown_count = len(list(filter(lambda article: article["categoryId"] == "unknown", articles)))

    defined_categories = category_definitions.keys()
    for index, article in enumerate(articles):
        if article["categoryId"] not in defined_categories:
            result.errors.append(f"'{article['categoryId']}' is undefined category (articles[{index}])")
    return result

def main(args):
    total_unknown_count = 0
    total_error_count = 0
    print()
    for path in args[1:]:
        with open(path, "r") as f:
            result = verify_gomidata(json.load(f))
            result.output(path)
            print()
            total_unknown_count += result.unknown_count
            total_error_count += len(result.errors)
    print("-" * 40)
    print()
    print(f"Total unknown: {total_unknown_count} | Total errors: {total_error_count}")
    print()

if __name__ == "__main__":
    main(sys.argv)
