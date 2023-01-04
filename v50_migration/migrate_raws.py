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
ns_main = [k for k, v in site.namespaces.items() if v == ''][0]
ns_df2014 = [k for k, v in site.namespaces.items() if v.lower() == 'df2014'][0]

if args.verbose:
    print('Connected. namespace=%i -> %i' % (ns_df2014, ns_main))

pages = list(p for p in site.allpages(namespace=ns_df2014)
            if p.name.endswith('/raw') and '.txt' not in p.name)
num_pages = len(pages)

for page_index, df2014_page in enumerate(pages):
    args.limit -= 1
    if args.verbose and (page_index % 100 == 0 or args.limit == 0):
        print('Progress: page %i/%i: %r' % (page_index, num_pages, df2014_page.name))
    if args.limit == 0:
        break

    main_page = site.pages[df2014_page.name.removeprefix('DF2014:')]
    log_msg = {'i': page_index, 'page': df2014_page.name, 'new_page': main_page.name}
    skipped = False
    overwritten = False
    new_text = None

    df2014_text = df2014_page.text()
    if '{{raw' not in df2014_text:
        skipped = True
        log_msg['error'] = 'not_raw'
        print('NOT RAW:', df2014_page.name)
    else:
        new_text = df2014_text.replace('DF2014:', 'v50:')
        if main_page.exists and new_text.strip() != main_page.text().strip():
            print('OVERWRITING:', main_page.name)
            overwritten = True
        summary = 'Creating v50 raw page (%i/%i)' % (page_index + 1, num_pages)
        log_msg['summary'] = summary


    log_msg.update({
        'skipped': skipped,
        'overwritten': overwritten,
    })
    log.write(json.dumps(log_msg) + '\n')
    log.flush()

    if new_text is not None:
        if not args.dry_run:
            main_page.edit(new_text, summary=summary)
