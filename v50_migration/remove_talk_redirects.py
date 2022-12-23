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
ns_talk = [k for k, v in site.namespaces.items() if v == 'Talk'][0]
ns_df2014_talk = [k for k, v in site.namespaces.items() if v == 'DF2014 Talk'][0]

if args.verbose:
    print('Connected. namespaces=%i, %i' % (ns_talk, ns_df2014_talk))
    print('Building list...')

pages = list(site.allpages(namespace=ns_talk, start=args.start))
num_pages = len(pages)
for page_index, talk_page in enumerate(pages):
    args.limit -= 1
    if args.verbose and (page_index % 100 == 0 or args.limit == 0):
        print('Progress: page %i/%i: %r' % (page_index, num_pages, talk_page.name))
    if args.limit == 0:
        break

    flagged = False
    log_msg = {'i': page_index, 'page': talk_page.name}
    do_delete = False

    summary = 'Deleting old talk page redirect (%i/%i)' % (page_index + 1, num_pages)

    redirect_target = talk_page.redirects_to()
    if redirect_target is not None:
        log_msg['old_redirect_target'] = redirect_target.name
        if '#REDIRECT' not in talk_page.text().upper():
            print('SANITY:', talk_page.name)
            log_msg['error'] = 'sanity'
            flagged = True
        elif redirect_target.page_title == talk_page.page_title and redirect_target.namespace in (ns_talk, ns_df2014_talk):
            do_delete = True
        else:
            log_msg['error'] = 'skipped'
            # print('skipping', talk_page, redirect_target)

    log_msg.update({
        'flagged': flagged,
        'summary': summary,
        'deleted': do_delete,
    })
    log.write(json.dumps(log_msg) + '\n')
    log.flush()

    if do_delete:
        if not args.dry_run:
            talk_page.delete(reason=summary)
