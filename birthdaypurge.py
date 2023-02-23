#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
This bot will purge the no.wikipedia articles for people
who were born on today's date (Norwegian time), in an effort
to make their automatically calculated age in the infobox
correct. It is meant to run just after midnight UTC, so
"today" is technically Toolforge's tomorrow (Norway is
UTC+1/UTC+2).
"""
import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import ExistingPageBot
from datetime import date, timedelta

months = [
    "", # 0
    "januar",
    "februar",
    "mars",
    "april",
    "mai",
    "juni",
    "juli",
    "august",
    "september",
    "oktober",
    "november",
    "desember"
]

# Because the server is on UTC while we want CET/CEST
today = date.today() + timedelta(days=1)
dateno = today.strftime("%-d")
month = today.strftime("%-m")
category = "Fødsler " + str(dateno) + ". " + months[int(month)]

def main(*args: str) -> None:
    local_args = pywikibot.handle_args(args)
    site = pywikibot.Site("wikipedia:no")
    site.throttle.setDelays(delay=0.1, writedelay=0.1)
    cat = pywikibot.Category(site, category)
    gen_factory = pagegenerators.CategorizedPageGenerator(cat)
    for page in gen_factory:
        print("Purging " + page.title())
        page.purge()

main()