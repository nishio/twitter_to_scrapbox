# -*- coding: utf-8 -*-
import json
import os
import re
import unicodecsv as csv
import codecs

def wakati(s):
    import MeCab
    tagger = MeCab.Tagger("-Owakati")
    words = tagger.parse(s.encode('utf-8')).strip().decode("utf-8").split()
    return words

INFILE = "tweets_20170403.csv"
TITLE_PREFIX = ""
KEYWORDS = u"KJ法 生産性 川喜田 外山".split()
pages = []
fo = file("text.txt", "w")
reader = csv.reader(file(INFILE), encoding="utf-8")
for row in reader:
    tid = row[0]
    datetime = row[3]
    text = row[5]
    lines = []
    #title = u"{prefix}{}".format(tid, prefix=TITLE_PREFIX)
    title = u"{prefix}{}".format(text, prefix=TITLE_PREFIX)
    lines.append(title)
    lines.append(text)

    lines.append("https://twitter.com/nishio/status/{}".format(tid))
    lines.append(datetime)
    date = datetime.split()[0]
    ks = [date]
    for k in KEYWORDS:
        if k in text:
            ks.append(k)
    lines.append(" ".join(u"[%s]" % k for k in ks))
    page = dict(title=title, lines=lines)
    pages.append(page)

    text = re.sub(u"@\w+", u" ", text)
    text = re.sub(u"http[\w:./]+", u" ", text)
    text = text.replace("_", "UNDERSCORE")
    text = text.replace(" ", "_")
    #text = u" ".join(text)
    text = u" ".join(wakati(text))

    fo.write(text.encode("utf8"))
    fo.write("\n")

json.dump(dict(pages=pages), codecs.open('to_scrapbox.json', 'w', encoding="utf-8"), ensure_ascii=False, indent=2)
