"""
Check recent changes periodically
"""

import os, sys, time
import wikibot
user = wikibot.command_line.get_user()
if not user:
    print('no user')
    sys.exit()
os.system('clear')
try:
    while 1:
        if len(user.api_request({'list':'recentchanges', 'rcprop':'user', 'rclimit':1, 'rcshow': '!patrolled'}, auto_filter=0)['query']['recentchanges']):
            wikibot.util.logf('\r<green>New changes!   ')
        else:
            wikibot.util.logf('\r<red>No new changes.')
        time.sleep(60)
except:
    wikibot.util.log('')