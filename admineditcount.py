#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywikibot
from datetime import date
import requests
import json

urlparams = {
    "format": "json",
    "action": "query",
    "list": "allusers",
    "augroup": "sysop",
    "aulimit": "200",
    "auprop": "editcount|groups"
}
resp = requests.get("https://no.wikipedia.org/w/api.php", params=urlparams).json()

users = []
for user in resp["query"]["allusers"]:
    usergroup = "admin"
    editcount = user["editcount"]
    username = user["name"]
    if "bureaucrat" in user["groups"]:
        usergroup = "byråkrat"
    if not username == "Redigeringsfilter":
        users.append((editcount, usergroup, username))
users.sort(key=lambda tup: tup[0], reverse=True)

result = "<!-- Automatisk oppdatert av JhsBot {0} -->\n".format(date.today())
template = "*<!-- {0} --> {{{{{1}|{2}}}}}\n"
for user in users:
    result += template.format(user[0], user[1], user[2])
site = pywikibot.Site()
page = pywikibot.Page(site, u"Wikipedia:Administratorer/liste/bidrag/automatisk")
page.text = result
page.save(u"bot: Oppdaterer statistikk")
