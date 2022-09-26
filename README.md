# jhstools
**jhstools** is a collection of small scripts run by me (Jon Harald Søby). All
of these scripts are currently (2021) run by cron on Wikimedia's [Toolforge.org](https://toolforge.org/).

## admineditcount.py
This script updates the page [\[\[w:no:Wikipedia:Administratorer/liste/bidrag/automatisk\]\]](https://no.wikipedia.org/wiki/Wikipedia:Administratorer/liste/bidrag/automatisk), which is
a list of all administrators on the Norwegian Bokmål Wikipedia listed by number
of edits. It is set to run once a week.

## apostrofbot.py
This script finds new pages in the Norwegian Bokmål Wikipedia that have a straigt
(typewriter) apostrophe in the title, and moves it to the typographically correct
apostrophe (&rsquo;), unless the template `{{riktig apostrof brukes}}` is present
on the page in question. It leaves behind a redirect, which it marks with the
template `{{O for apostrof}}`.

Additionally, the script finds pages that are created with the typographically
correct apostrophe and creates a redirect from the straight apostrophe version if
one doesn't already exist.

If the bot is not able to move a page for some reason, it will instead list the page
on the page [\[\[w:no:Bruker:JhsBot/Apostrof/Problematisk\]\]](https://no.wikipedia.org/wiki/Bruker:JhsBot/Apostrof/Problematisk).

The script is set to run every night at 03:30 UTC, and will check pages that have
been created within the last 24 hours.

## move_timed_text.py
This script checks the page move log on Wikimedia Commons, and if an audio or video
file has been moved, it checks whether that file has corresponding pages in the
TimedText namespace (i.e. subtitles). If there are any pages, the script will move
them to the page name corresponding to the new file.

This script is set to run once an hour on Wikimedia Commons.

## interwikibot.py
This script adds sitelinks to Wikidata for newly created wikis that use the
{{INTERWIKI}} template from the Wikimedia Incubator. Once the sitelink has been
added, it will remove the template from the wiki in question.

This is run manually after new wikis are created and content is imported and
Wikidata support for the site has been enabled (which can some times take several
days after the wiki was created).