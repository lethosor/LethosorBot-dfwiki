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
def log(text, color='black'):
    wikibot.util.logf('<{0}>{1: <80}\r'.format(color, text))

try:
    while 1:
        try:
            if len(user.api_request({'list':'recentchanges', 'rcprop':'user', 'rclimit':1, 'rcshow': '!patrolled'}, auto_filter=0)['query']['recentchanges']):
                log('New changes!', 'green')
            else:
                log('No new changes.', 'red')
        except Exception as e:
            log('Check failed: %s' % e, 'yellow')
        time.sleep(60)
        log('Checking...')
except:
    wikibot.util.log('')
