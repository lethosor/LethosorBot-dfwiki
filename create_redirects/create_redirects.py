from __future__ import print_function

import argparse
import json

import mwclient
import mwclient.ex

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

site = mwclient.ex.ConfiguredSite(args.site_config)
ns_df2014 = [k for k, v in site.namespaces.items() if v == 'DF2014'][0]

if args.verbose:
    print('Connected. namespace=%i' % ns_df2014)

pages = site.allpages(namespace=ns_df2014, start=args.start)
for page in pages:
    if page.name.endswith('/raw'):
        continue

    if args.verbose:
        print(page.name)
    msg = {"page": page.name}
    mainpage = site.pages[page.page_title]
    msg["main_page"] = mainpage.name
    msg["main_exists"] = mainpage.exists
    msg["created"] = False
    if not mainpage.exists:
        content = msg["main_content"] = "#REDIRECT [[cv:%s]]" % page.page_title
        if not args.dry_run:
            mainpage.save(content, summary="Creating redirect to cv:%s" % page.page_title)
            msg["created"] = True
    log.write(json.dumps(msg) + '\n')

    args.limit -= 1
    if args.limit == 0:
        break
