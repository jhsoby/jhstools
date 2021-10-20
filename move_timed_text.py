#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywikibot
import requests
import json
from datetime import datetime, timedelta

site = pywikibot.Site('commons', 'commons')

def get_prefixindex_timedtext(filename):
    urlparams = {
        'format': 'json',
        'action': 'query',
        'list': 'prefixsearch',
        'pssearch': 'TimedText:' + filename,
        'pslimit': 500
    }
    resp = requests.get('https://commons.wikimedia.org/w/api.php', params=urlparams).json()
    if len(resp['query']['prefixsearch']) != 0:
        pages = []
        for page in resp['query']['prefixsearch']:
            pages.append(page['title'])
        return pages

def move_timedtext_page(old_pagename, new_pagename, lang_and_ext):
    old_timedtext = "TimedText:" + old_pagename + "." + lang_and_ext
    new_timedtext = "TimedText:" + new_pagename + "." + lang_and_ext
    wikipage = pywikibot.Page(site, old_timedtext)
    wikipage.move(new_timedtext, reason="Moved because the [[File:{}|file it belongs to]] was moved".format(new_pagename), noredirect=True)
    print("Moved {} to {} ...".format(old_timedtext, new_timedtext))

def main():
    file_extensions = ["mp3", "mid", "ogg", "spx", "opus", "flac", "wav", "ogv", "webm", "mpg", "mpeg"]
    timeformat = "%Y-%m-%dT%H:%M:%SZ"
    urlparams = {
        'format': 'json',
        'action': 'query',
        'list': 'logevents',
        'letype': 'move',
        'lestart': datetime.now().strftime(timeformat),
        'leend': (datetime.now() - timedelta(hours=2)).strftime(timeformat),
        'lelimit': 500,
        'lenamespace': 6,
        'ledir': 'older'
    }
    resp = requests.get('https://commons.wikimedia.org/w/api.php', params=urlparams).json()
    for item in resp["query"]["logevents"]:
        if item["title"].split(".")[-1].lower() not in file_extensions:
            continue
        else:
            old_filename = item["title"][5:]
            new_filename = item["params"]["target_title"][5:]
            timedtextpages = get_prefixindex_timedtext(old_filename)
            if not timedtextpages:
                continue
            else:
                for page in timedtextpages:
                    lang_and_ext = ".".join(page.split(".")[-2:])
                    move_timedtext_page(old_filename, new_filename, lang_and_ext)

main()