#! /usr/bin/env python
import re, time, wikibot
util = wikibot.util

wikibot.command_line.parser.add_argument('--dry-run', action='store_true', help='Dry run')
args = wikibot.command_line.parse_args()

user = wikibot.cred.get_user()

version_pattern = re.compile(r'download\s+dwarf\s+fortress\s+([0-9\.]+)\s+\(([^)]+)\)', re.I)

while 1:
    try:
        if not args.dry_run:
            req = wikibot.network.Request('http://www.bay12games.com/dwarves/')
            version, date = version_pattern.search(req.response_text).groups()
        else:
            version, date = '0.34.11', 'June 4, 2012'
    except Exception as e:
        util.log('Unable to retrieve version: %s' % e, type='warn')
        time.sleep(60)
        continue
    util.log('Retrieving current version...')
    version_page = user.get_page('Template:Current/version')
    version_text = version_page.text.split('<')[0]
    date_page = user.get_page('Template:Current/lastupdate')
    date_text = date_page.text.split('<')[0]
    summary = 'Updating to version %s (Released %s)' % (version, date)
    util.log('Current: %s: %s | Wiki: %s: %s' % (version, date, version_text, date_text))
    updated = False
    if version_text != version:
        if not args.dry_run:
            version_page.text = version + '<' + version_page.text.split('<', 1)[1]
            version_page.save(summary=summary, bot=1)
        updated = True
    if date_text != date:
        if not args.dry_run:
            date_page.text = date + '<' + date_page.text.split('<', 1)[1]
            date_page.save(summary=summary, bot=1)
        updated = True
    if updated:
        util.log('<green>New version!!!!')
    else:
        util.log('No change')

    time.sleep(3600)
