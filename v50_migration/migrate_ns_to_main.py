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
ns_df2014 = [k for k, v in site.namespaces.items() if v == 'DF2014'][0]

if args.verbose:
    print('Connected. namespace=%i' % ns_df2014)
    print('Building list...')

pages = site.allpages(namespace=ns_df2014, start=args.start)
num_pages = len(list(site.allpages(namespace=ns_df2014, start=args.start)))
for page_index, df2014_page in enumerate(pages):
    args.limit -= 1
    if args.verbose and (page_index % 100 == 0 or args.limit == 0):
        print('Progress: page %i/%i: %r' % (page_index, num_pages, df2014_page.name))
    if args.limit == 0:
        break
    if df2014_page.name.endswith('/raw'):
        continue
    if df2014_page.name.startswith('DF2014:Release information/0'):
        continue

    flagged = False
    log_msg = {'i': page_index, 'page': df2014_page.name}
    do_log_content = False
    do_content_edit = False
    do_content_move = False

    summary = 'Migrating v50 page (%i/%i)' % (page_index, num_pages)

    df2014_text_old = df2014_page.text()
    df2014_text_new = df2014_text_old

    main_page = site.pages[df2014_page.name.removeprefix('DF2014:')]
    main_text_old = main_page.text()
    main_text_new = main_text_old

    log_msg['df2014_was_redirect'] = df2014_page.redirect
    log_msg['main_existed'] = main_page.exists
    if df2014_page.redirect:
        log_msg['type'] = 'redirect'
        if df2014_text_old.count(':') <= 1:
            main_text_new = re.sub(r'\[\[(.*):', '[[', df2014_text_old)
            df2014_text_new = re.sub(r'\[\[(.*):', '[[DF2014:', df2014_text_old)
            do_log_content = True
            do_content_edit = True
        else:
            log_msg['error'] = 'unhandled_redirect_format'
            flagged = True
    elif main_page.redirect:
        if main_page.redirects_to().name == df2014_page.name:
            # normal move
            log_msg['type'] = 'content'
            do_content_move = True
        else:
            log_msg['type'] = 'unknown'
            print('BAD REDIRECT:', main_page.name, main_page.redirects_to().name)
            log_msg['error'] = 'bad_redirect'
            flagged = True
    elif not main_page.exists:
        log_msg['type'] = 'content'
        do_content_move = True
    else:
        log_msg['type'] = 'unknown'
        print('BOTH CONTENT:', main_page.name)
        log_msg['error'] = 'both_content'
        flagged = True

    summary += ' (%s)' % log_msg['type']

    if do_log_content:
        log_msg.update({
            'df2014_text_old': df2014_text_old,
            'df2014_text_new': df2014_text_new,
            'main_text_old': main_text_old,
            'main_text_new': main_text_new,
        })

    log_msg['summary'] = summary
    log_msg['flagged'] = flagged

    log.write(json.dumps(log_msg) + '\n')
    log.flush()

    if not args.dry_run:
        if do_content_edit:
            pass # TODO
        elif do_content_move:
            pass # TODO
