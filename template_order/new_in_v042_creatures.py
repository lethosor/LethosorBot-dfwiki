import os

import mwclient
import mwclient.ex

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'credentials.py')
site = mwclient.ex.ConfiguredSite(config_path)

old_pattern = '{{creaturedesc}}\n{{new in v0.42}}'
new_pattern = '{{new in v0.42}}\n{{creaturedesc}}'

template = site.Pages['Template:New in v0.42']
for page in template.embeddedin(namespace='DF2014', filterredir='nonredirects'):
    text = page.text()
    if old_pattern in text:
        print('Fixing {}'.format(page.page_title))
        text = text.replace(old_pattern, new_pattern)
        page.save(text, summary='Fixing template order: {{new in v0.42}} before {{creaturedesc}}', minor=True)
