import os

import mwclient
import mwclient.ex

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'credentials.py')
site = mwclient.ex.ConfiguredSite(config_path)

def run(generator, old_pattern, new_pattern, summary, dry_run=False):
    empty = True
    fixed = False
    for page in generator:
        empty = False
        text = page.text()
        if old_pattern in text:
            fixed = True
            print('{0} {1}'.format('Fixing' if not dry_run else 'Would fix', page.name))
            if dry_run:
                continue
            text = text.replace(old_pattern, new_pattern)
            page.save(text, summary=summary, minor=True)
    if empty:
        print('No pages found in list')
    elif not fixed:
        print('No pages in list were fixed')
