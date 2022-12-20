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
ns_template = [k for k, v in site.namespaces.items() if v == 'Template'][0]

if args.verbose:
    print('Connected. namespace=%i' % ns_template)

pages = list(site.allpages(namespace=ns_template, prefix='DF2014 ', start=args.start))
num_pages = len(pages)
for page_index, df2014_page in enumerate(pages):
    args.limit -= 1
    if args.verbose and (page_index % 100 == 0 or args.limit == 0):
        print('Progress: page %i/%i: %r' % (page_index, num_pages, df2014_page.name))
    if args.limit == 0:
        break

    flagged = False
    v50_page = site.pages[df2014_page.name.replace('DF2014', 'v50')]
    log_msg = {'i': page_index, 'page': df2014_page.name, 'new_page': v50_page.name}

    categories = [c.name for c in df2014_page.categories()]

    if v50_page.name == df2014_page.name:
        flagged = True
        log_msg['error'] = 'bad_name'
        print('BAD NAME:', df2014_page.name)
    elif v50_page.exists:
        flagged = True
        log_msg['error'] = 'already_exists'
        print('ALREADY EXISTS:', v50_page.name)
    elif 'Category:Navigation templates' not in categories:
        flagged= True
        log_msg['error'] = 'bad_category'
        print('BAD CATEGORY:', v50_page.name, categories)

    new_text = df2014_page.text().replace('DF2014', 'v50')
    summary = 'Migrating v50 template (%i/%i)' % (page_index + 1, num_pages)

    log_msg.update({
        'flagged': flagged,
        'summary': summary,
    })
    log.write(json.dumps(log_msg) + '\n')
    log.flush()

    if not flagged:
        if args.verbose:
            print('Copy %r to %r' % (df2014_page.name, v50_page.name))
        if not args.dry_run:
            v50_page.edit(new_text, summary=summary)
