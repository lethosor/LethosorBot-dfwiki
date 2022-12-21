from __future__ import print_function

import argparse
import json
import re

import mwclient

import dfwikibot_util

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', '--site-config', dest='site_config', required=True)
parser.add_argument('-l', '--log', '--log-file', dest='log_file', required=True)
parser.add_argument('-n', '--dry-run', action='store_true')
parser.add_argument('-s', '--start', default='')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-x', '--limit', type=int, default=0)
args = parser.parse_args()

log = open(args.log_file, 'a')

if args.verbose:
    print('Connecting...')

site = dfwikibot_util.make_site(args.site_config)
ns_main = 0

if args.verbose:
    print('Connected. namespace=%i' % ns_main)
    print('Building list...')

pages = list(site.allpages(namespace=ns_main, start=args.start))
num_pages = len(pages)
for page_index, page in enumerate(pages):
    args.limit -= 1
    if args.verbose and (page_index % 100 == 0 or args.limit == 0):
        print('Progress: page %i/%i: %r' % (page_index, num_pages, page.name))
    if args.limit == 0:
        break

    flagged = False
    log_msg = {'i': page_index, 'page': page.name}

    summary = 'Tagging v50 page (%i/%i)' % (page_index + 1, num_pages)

    text = page.text()
    old_text = text
    added_braces = 0
    if '{{av}}' in text.lower():
        text = '{{migrated article}}\n' + text
        added_braces += 2

    text = re.sub(r'\{\{quality.*?\}\}', '{{Quality|Unrated}}', text, flags=re.IGNORECASE | re.MULTILINE)

    if (text.count('{') != old_text.count('{') + added_braces) or (text.count('}') != old_text.count('}') + added_braces):
        print('BRACE MISMATCH:', page.name)
        flagged = True
        log_msg.update({'error': 'brace_mismatch', 'new_text': text})

    changed = (text != old_text)

    log_msg.update({
        'flagged': flagged,
        'summary': summary,
        'changed': changed,
    })
    log.write(json.dumps(log_msg) + '\n')
    log.flush()

    if (not flagged) and changed:
        if args.dry_run:
            print('would edit: %r' % (page.name))
            if args.verbose:
                print('%r: %r' % (summary, text))
        else:
            page.edit(text, summary=summary)
