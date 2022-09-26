#!/usr/bin/python3.9
r"""
This bot will work on pages that transclude the {{INTERWIKI}}
template on newly created wikis. It will add the page to the
indicated Wikidata item, and then remove the template from the
page.

The only command line parameters that are necessary are
Pywikibot's lang and family parameters.

Usage:

python interwikibot.py -lang:xx -family:xxxx
"""
import pywikibot
from pywikibot import pagegenerators
import requests
import json
import re
from datetime import datetime, timedelta

def main(**kwargs: str) -> None:
    local_args = pywikibot.handle_args(kwargs)
    wdsite = pywikibot.Site('wikidata', 'wikidata')
    wdtoken = wdsite.get_tokens(['csrf'], True)
    site = pywikibot.Site()
    iwtemplateregex = r"\n?\{\{\s*(IW|INTERWIKI)\s*\|\s*(Q[1-9]\d*)\s*\}\}"
    gen = pywikibot.Page(site, 'INTERWIKI', ns=10).getReferences(only_template_inclusion=True)
    for page in gen:
        pywikibot.output('\n\n==============\n[[' + page.title() + ']]\n==============\n' )
        pageobj = pywikibot.Page(site, page.title())
        pagetext = pageobj.text
        interwikitemplate = re.search(iwtemplateregex, pagetext)
        if interwikitemplate:
            qid = interwikitemplate.group(2)
            checkparams = {
                'action': 'wbgetentities',
                'format': 'json',
                'ids': qid,
                'props': 'sitelinks'
            }
            addparams = {
                'action': 'wbsetsitelink',
                'id': qid,
                'bot': True,
                'linksite': site.dbName(),
                'linktitle': pageobj.title(),
                'token': wdtoken['csrf']
            }
            try:
                # Check if the item already has a sitelink to the
                # current wiki (it could happen if two pages have
                # the same ID in the template)
                checkquery = wdsite._request(parameters=checkparams).submit()
                existinglinks = checkquery['entities'][qid]['sitelinks']
                if site.dbName() in existinglinks:
                    pywikibot.error('There is already a link to a page on {} in {}.\nSkipping!'.format(site.dbName(), qid))
                    continue
                else:
                    # Add the page to the Wikidata item
                    wdsite._request(parameters=addparams).submit()
                    pywikibot.output('Added [[{}]] to {}.'.format(page.title(), qid))
                    # Remove the template from the page
                    pageobj.text = re.sub(iwtemplateregex, '', pagetext)
                    try:
                        pageobj.save('bot: Removing interwiki template; the page is now connected to [[d:{}]]'.format(qid))
                        pywikibot.output('Removed {{{{INTERWIKI}}}} from [[{}]].'.format(page.title()))
                    except:
                        pywikibot.error('Could not remove INTERWIKI template from [[{}]]!'.format(page.title()))
            except:
                pywikibot.error('Could not add [[{}]] to {}!'.format(page.title(), qid))
        else:
            print("No valid interwiki template here…?")
            continue
    pywikibot.output('\n\n\nFINISHED!\n\n')
    # Check if all instances of the template have been removed.
    # If it is no longer used at all, mark the template and the
    # module for deletion.
    #
    # {{delete}} doesn't technically do anything on module pages,
    # so the message in the template has a large text asking
    # for the module to be deleted as well.
    templatecountparams = {
        'action': 'query',
        'format': 'json',
        'prop': 'transcludedin',
        'titles': 'Template:INTERWIKI'
    }
    tcres = site._request(parameters=templatecountparams).submit()
    templateid = list(tcres['query']['pages'].keys())[0]
    if 'transcludedin' in tcres['query']['pages'][templateid]:
        pywikibot.output('There are still {} pages with the INTERWIKI template. Please check these manually, and then mark the template and module for deletion.'.format(len(tcres['query']['pages'][templateid]['transcludedin'])))
    else:
        template = pywikibot.Page(site, 'Template:INTERWIKI')
        module = pywikibot.Page(site, 'Module:IncubatorInterwiki')
        if template.exists():
            template.text = '{{delete|Please delete this template, it is no longer used.}}\n{{#ifexist:Module:IncubatorInterwiki|<div style="font-size:200%;">Please also delete [[Module:IncubatorInterwiki]]!</div>}}'
            template.save('bot: Requesting deletion of unused template', botflag=False)
            pywikibot.output('Requested deletion of {{INTERWIKI}}.')
        if module.exists():
            module.text = '-- {{delete}} This module is not needed any more. Please delete.'
            module.save('bot: Requesting deletion of unused module', botflag=False)
            pywikibot.output('Requested deletion of [[Module:IncubatorInterwiki]]')
    return

main()