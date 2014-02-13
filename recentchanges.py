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
    wikibot.util.logf('<{0}>{1: <50}\r'.format(color, text))

try:
    while 1:
        if len(user.api_request({'list':'recentchanges', 'rcprop':'user', 'rclimit':1, 'rcshow': '!patrolled'}, auto_filter=0)['query']['recentchanges']):
            log('New changes!', 'green')
        else:
            log('No new changes.', 'red')
        time.sleep(60)
        log('Checking...')
except Exception as e:
    wikibot.util.log('\n<bold,red>Error:<red> ' + str(e))
except:
    wikibot.util.log('')
