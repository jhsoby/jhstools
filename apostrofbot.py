#!/usr/bin/python3.9
import pywikibot
from pywikibot import pagegenerators
import requests
import json
import re
from datetime import datetime, timedelta

site = pywikibot.Site()

def check_if_page_exists(page):
    matrix = {
        'title': page,
        'exists': False,
        'redirect': False,
        'redirecttarget': False,
        'nomove': False
    }
    urlparams = {
        'format': 'json',
        'action': 'query',
        'redirects': 1,
        'titles': page
    }
    resp = requests.get('https://no.wikipedia.org/w/api.php', params=urlparams).json()
    resp_query = resp["query"]
    resp_pages = resp_query["pages"]
    resp_key = list(resp_pages.keys())[0]
    if resp_key == "-1":
        return matrix
    else:
        if "redirects" in resp_query:
            matrix["exists"] = True
            matrix["redirect"] = True
            matrix["redirecttarget"] = resp_query["redirects"][0]["to"]
            return matrix
        else:
            matrix["exists"] = True
            return matrix

def add_to_problematic(page1, page2, reason):
    print("[[{0}]] and [[{1}]] added to list of problematic pages because {2}".format(page1, page2, reason))
    page = pywikibot.Page(site, "Bruker:JhsBot/Apostrof/Problematisk")
    page.text = page.text + "\n# [[{}]] og [[{}]]".format(page1, page2)
    page.save("bot: Legger til [[{}]] og [[{}]]".format(page1, page2))
    
def create_redirect(page1, page2):
    print("Creating redirect from [[{0}]] to [[{1}]]".format(page1, page2))
    page = pywikibot.Page(site, page1)
    page.text = "#omdirigering [[%s]]\n{{O fra apostrof}}" % page2
    page.save("bot: Omdirigerer til [[%s]]" % page2)
    
def move_page(movefrom, moveto):
    print("Moving [[{0}]] to [[{1}]]".format(movefrom, moveto))
    lhurlparams = {
        'format': 'json',
        'action': 'query',
        'prop': 'linkshere',
        'lhnamespace': 10,
        'lhlimit': 'max',
        'titles': movefrom
    }
    resp = requests.get('https://no.wikipedia.org/w/api.php', params=lhurlparams).json()
    resp_pages = resp["query"]["pages"]
    resp_key = list(resp_pages.keys())[0]
    wikipage = pywikibot.Page(site, movefrom)
    wikipage.move(moveto, reason="bot: Flytter til tittel med [[Bruker:JhsBot/Apostrof|riktig apostrof]]")
    movedfrompage = pywikibot.Page(site, movefrom)
    movedfrompage.text = movedfrompage.text + "\n{{O fra apostrof}}"
    movedfrompage.save("bot: Legger til {{O fra apostrof}}")
    movedtopage = pywikibot.Page(site, moveto)
    if re.search(r"\{\{(DISPLAYTITLE|VISTITTEL):\s*" + movefrom + r"\s*\}\}", movedtopage.text):
        movedtopage.text = re.sub(r"\{\{(DISPLAYTITLE|VISTITTEL):\s*(" + movefrom + r")\s*\}\}", "{{\\1:" + moveto + "}}", movedtopage.text)
        movedtopage.save("bot: Endrer DISPLAYTITLE for flytta side")
    if "linkshere" in resp_pages[resp_key]:
        linkshere = resp_pages[resp_key]["linkshere"]
        for page in linkshere:
            title = page["title"]
            template = pywikibot.Page(site, title)
            templatetext = template.text
            templatetext = re.sub(r"(?<=\[\[)" + movefrom + r"(?<!\||\])", moveto, templatetext)
            template.text = templatetext
            template.save("bot: Endrer lenke til side som har blitt flytta")   


timeformat = "%Y-%m-%dT02:00:00"
rcparams = {
    'format': 'json',
    'action': 'query',
    'list': 'recentchanges',
    'rcstart': datetime.now().strftime(timeformat),
    'rcend': (datetime.now() - timedelta(days=1)).strftime(timeformat),
    'rcdir': 'older',
    'rclimit': 5000,
    'rctype': 'new',
    'rcnamespace': 0,
    'rcprop': 'title|redirect'
}
rcresp = requests.get('https://no.wikipedia.org/w/api.php', params=rcparams).json()
rcresp_query = rcresp["query"]["recentchanges"]
for item in rcresp_query:
    title = item["title"]
    if ("redirect" in item) or (not re.search(r"['’]", title)):
        continue
    else:
        thisurlparams = {
            'format': 'json',
            'action': 'query',
            'prop': 'templates',
            'redirects': 1,
            'tlnamespace': 10,
            'tltemplates': 'Mal:Riktig apostrof brukes',
            'titles': title
        }
        resp = requests.get('https://no.wikipedia.org/w/api.php', params=thisurlparams).json()
        resp_pages = resp["query"]["pages"]
        resp_key = list(resp_pages.keys())[0]
        if ("redirects" in resp["query"]) or ("templates" in resp_pages[resp_key]):
            continue
        if "’" in title:
            what = check_if_page_exists(title.replace("’", "'"))
            if what["exists"]:
                if what["redirecttarget"] == title:
                    print("Nothing needs to be done with {}".format(title))
                    continue
                else:
                    add_to_problematic(title, what["title"], "both pages exist, neither is redirect")
            else:
                create_redirect(what["title"], title)
        elif "'" in title:
            what = check_if_page_exists(title.replace("'", "’"))
            if what["exists"]:
                if what["redirect"]:
                    if what["redirecttarget"] == title:
                        try:
                            move_page(title, what["title"])
                        except:
                            add_to_problematic(title, what["title"], "can't move for some reason")
                    else:
                        add_to_problematic(title, what["title"], "differing redirect target")
                else:
                    add_to_problematic(title, what["title"], "both pages exist, neither is redirect")
            else:
                move_page(title, what["title"])
        else:
            continue