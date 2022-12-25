"""
Recent changes tracker
"""

import sys, time
import wikibot
import wikibot.util as util
try:
    user = wikibot.cred.get_user()
except wikibot.user.UserError as e:
    wikibot.util.die('Could not log in:', e)

timestamp = user.api_request({'list':'recentchanges', 'rclimit':1}, query_continue=False)['query-continue']['recentchanges']['rccontinue'].split('|')[0]
print(timestamp)
while 1:
    util.logf('\rfetching')
    rc = user.api_request({'list':'recentchanges', 'rclimit': 500, 'rcstart': timestamp})
    print(rc)
    time.sleep(2)
