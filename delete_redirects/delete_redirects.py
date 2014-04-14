"""
Deletes redirects from mainspace pages to their corresponding cv: pages, or
categorizes them if they redirect to different pages.
"""

import re

import wikibot
util = wikibot.util
user = wikibot.cred.get_user()

while True:
    query = user.api_request({
        'list': 'allpages',
        'apnamespace': 0,
        'apfilterredir': 'redirects',  # Only redirects
        'aplimit': 250,
    }, auto_filter=False)
    redirects = [p['title'] for p in query['query']['allpages']]
    if not len(redirects):
        util.log('Done.', type='success')
        break
    print(redirects)
    for title in redirects:
        util.logf('Fetching "%s"... ' % title)
        p = user.get_page(title)
        redirect_title = re.search(r'\[\[([^\]]+)\]\]', p.text)
        if redirect_title:
            redirect_title = redirect_title.groups()[0].replace('_', ' ')
        else:
            util.logf('Not a redirect.\n', type='error')
            continue
        if redirect_title.lower() == 'cv:' + title.lower():
            util.logf('Deleting... ')
            user.api_request({
                'action': 'delete',
                'title': title,
                'reason': 'Batch-deleting unneeded redirects',
                'token': user.edit_token,
            })
            util.logf('Done.\n', type='success')
        else:
            #print('\n%s | %s' % (redirect_title, 'cv:'+title))
            util.logf('Redirects to "%s" instead.\n' % redirect_title, type='warn')
    break
