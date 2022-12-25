from __future__ import print_function

import argparse
import json
import re

import mwclient

import dfwikibot_util

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', '--site-config', dest='site_config', required=True)
parser.add_argument('-n', '--dry-run', action='store_true')
parser.add_argument('-s', '--namespace', required=True)
parser.add_argument('-o', '--output-file', required=True)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

if args.verbose:
    print('Connecting...')

site = dfwikibot_util.make_site(args.site_config)
ns_id = [k for k, v in site.namespaces.items() if v.lower() == args.namespace.lower()][0]

if args.verbose:
    print('Connected. namespace=%i' % ns_id)
    print('Building list...')

pages = list(p for p in site.allpages(namespace=ns_id)
            if p.name.endswith('/raw'))
num_pages = len(pages)

if args.dry_run:
    print('Would download %i pages' % num_pages)
    exit(0)

with open(args.output_file, 'w') as out_file:
    output = {}
    for page_index, page in enumerate(pages):
        if args.verbose and (page_index % 100 == 0):
            print('Progress: page %i/%i: %r' % (page_index, num_pages, page.name))
        output[page.name] = page.text()
    json.dump(output, out_file, indent=1)
