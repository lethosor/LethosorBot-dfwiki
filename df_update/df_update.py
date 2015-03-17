#! /usr/bin/env python

from __future__ import print_function

import datetime, re, time, traceback, wikibot
util = wikibot.util

wikibot.command_line.parser.add_argument('--dry-run', action='store_true', help='Dry run')
wikibot.command_line.parser.add_argument('--interval', type=int, help='Update interval, in minutes', default=20)
args = wikibot.command_line.parse_args()

user = wikibot.cred.get_user()

version_pattern = re.compile(r'download\s+dwarf\s+fortress\s+([0-9\.]+)\s+\(([^)]+)\)', re.I)

release_notes_template = '''\
{{{{release notes}}}}

: {quote}
:&mdash;Toady One, {date}

{content}
'''

def format_release_notes(html, version):
    html = html.replace('\r', '').replace('\x01', '')
    matches = list(re.finditer(r'<li.*?class=[\'"]dev_progress', html))
    for i, m in enumerate(matches):
        if i == 0 or i + 1 >= len(matches):
            continue
        entry = html[m.start() : matches[i + 1].start()]
        if version in entry and 'hilt' in entry:
            prev_entry = html[matches[i - 1].start() : m.start()]
            prev_entry = prev_entry.lstrip('\n')
            prev_entry = re.sub(r'<br */?>', '', prev_entry)
            date = map(int, re.search('<span.*?date.*?(\d+/\d+/\d+).*?</span>', prev_entry).group(1).split('/'))
            date = datetime.date(date[2], date[0], date[1]).strftime('%B %d, %Y').replace(' 0', ' ')
            prev_entry = re.sub(r'<span.*?date.*?</span>', '', prev_entry)
            prev_entry = re.sub(r'</?ul', lambda m: '\n\x01\n' + m.group(0), prev_entry)
            prev_entry = re.sub(r'<.*?>', '', prev_entry)
            prev_entry = re.sub(r'\n[ \t]*', '\n', prev_entry)
            prev_entry = prev_entry.strip('\n')
            quote, prev_entry = prev_entry.split('\n', 1)
            lines = prev_entry.lstrip('\n').splitlines()
            in_list = False
            for j, line in enumerate(lines):
                if '\x01' in line:
                    in_list = not in_list
                    lines[j] = ''
                elif not line:
                    pass
                else:
                    if in_list:
                        lines[j] = '* ' + line
                    else:
                        lines[j] = '== ' + line.rstrip(' ') + ' =='
            prev_entry = '\n'.join(lines)
            prev_entry = re.sub(r'\n+\=\=', '\n\n==', prev_entry, re.MULTILINE)
            prev_entry = re.sub(r'==\n+', '==\n', prev_entry, re.MULTILINE)
            return {'date': date, 'quote': quote, 'content': prev_entry}

while 1:
    try:
        try:
            if not args.dry_run:
                util.log('Retrieving version information (Bay12)')
                req = wikibot.network.Request('http://www.bay12games.com/dwarves/')
                version, date = version_pattern.search(req.response_text).groups()
                util.log('Retrieving current version (on wiki)')
                version_page = user.get_page('Template:Current/version')
                version_text = version_page.text.split('<')[0]
                date_page = user.get_page('Template:Current/lastupdate')
                date_text = date_page.text.split('<')[0]
            else:
                version, date = '0.34.11', 'June 4, 2012'
        except Exception as e:
            util.log('Unable to retrieve version: %s' % e, type='warn')
            time.sleep(300)
            continue
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
            cat_page = user.get_page('Category:Version %s' % version)
            if not cat_page.exists:
                cat_page.text = '{{vcat}}'
                cat_page.save(summary="Creating version category", bot=1)
                util.log('Created version category', type='info')
            rl_links_page = user.get_page('cv:Release information/List')
            if not version in rl_links_page.text:
                rl_links_page.text = rl_links_page.text.rstrip('\n') + \
                    ('\n{{release notes link|%s}}' % version)
                rl_links_page.save(summary="Adding %s" % version, bot=1)
                util.log('Added link to release notes', type='info')
            rl_page = user.get_page('cv:Release information/%s' % version)
            if not rl_page.exists:
                notes = format_release_notes(req.response_text, version)
                rl_page.text = release_notes_template.format(**notes)
                rl_page.save(summary="Creating release notes for v%s" % version, bot=1)
                util.log('Created release notes', type='info')
        else:
            util.log('No change')
    except Exception as e:
        print('-' * 80)
        traceback.print_exc()
        print('-' * 80)
    time.sleep(60 * args.interval)
