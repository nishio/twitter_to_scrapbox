# -*- coding: utf-8 -*-
import json
import os
import csv
import re
from collections import defaultdict
import datetime
import codecs

pages = []
def add_page(title, lines):
    page = dict(
        title=title, 
        lines=[title] + lines)
    pages.append(page)    

ymd_to_tweet = defaultdict(list)
ym_to_ymd = defaultdict(set)
y_to_ym = defaultdict(set)

INFILE = "tweets.csv"
pages = []
reader = csv.reader(open(INFILE, encoding="utf-8"))

for row in reader:
    tid = row[0]
    s_datetime = row[3]
    text = row[5]
    if s_datetime == "timestamp": continue  # first line
    
    dt = datetime.datetime.strptime(s_datetime, "%Y-%m-%d %H:%M:%S %z")
    ymd = dt.strftime("%Y-%m-%d")
    ym = dt.strftime("%Y-%m")
    y = dt.strftime("%Y")
    url = "https://twitter.com/nishio/status/{}".format(tid)
    link_to_tweet = "[T {}]".format(url)

    ymd_to_tweet[ymd].append(" {} {}".format(text, link_to_tweet))
    ym_to_ymd[ym].add(ymd)
    y_to_ym[y].add(ym)


for y in y_to_ym:
    add_page(
        title=y, 
        lines=["[%s]" % ym for ym in sorted(y_to_ym[y])])

for ym in ym_to_ymd:
    add_page(
        title=ym,
        lines=["[%s]" % ymd for ymd in sorted(ym_to_ymd[ym])])

for ymd in sorted(ymd_to_tweet):
    add_page(
        title=ymd,
        lines=list(reversed(ymd_to_tweet[ymd])))

json.dump(dict(pages=pages), codecs.open('to_scrapbox.json', 'w', encoding="utf-8"), ensure_ascii=False, indent=2)


