#!/usr/bin/python
# -*- coding: utf-8 -*-

r"""
This bot creates new monthly maintenance categories for
categories that have a monthly setup in the Norwegian
Bokmål Wikipedia.
"""
import pywikibot
from pywikibot.page import Page
from datetime import datetime
from datetime import date, timedelta
import pytz

categories = [
	[ "Stubber {}", "{{skjult kategori}}\n\n[[Kategori:Stubber etter tid]]" ],
	[ "Artikler som trenger flere eller bedre referanser {}", "{{skjult kategori}}\n\n[[Kategori:Artikler som trenger flere referanser]]" ],
	[ "Opprydning {}", "{{skjult kategori}}\n\n[[Kategori:Opprydning]]" ],
	[ "Språkvask {}", "{{skjult kategori}}\n\n[[Kategori:Språkvask]]" ]
]

now = datetime.now(pytz.timezone("Europe/Oslo"))
thishoursmonth = now.strftime("%Y-%m")
nexthoursmonth = (now + timedelta(hours=1)).strftime("%Y-%m")

def main(*args: str) -> None:
	local_args = pywikibot.handle_args(args)
	site = pywikibot.Site("wikipedia:no")
	site.throttle.setDelays(delay=0.1, writedelay=0.1)
	for cat in categories:
		catname = "Kategori:" + cat[0].format(nexthoursmonth)
		catcontent = cat[1]
		page = Page(site,catname)
		if not page.exists():
			page.text = catcontent
			page.save("bot: Oppretter månedlig vedlikeholdskategori")

if thishoursmonth != nexthoursmonth:
	main()