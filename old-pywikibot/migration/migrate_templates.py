
import wikibot
util = wikibot.util
parser = wikibot.command_line.parser
parser.add_argument('--old', help='Old prefix', required=True)
parser.add_argument('--new', help='New prefix', required=True)
args = parser.parse_args()
user = wikibot.cred.get_user()

old_pages = user.api_request({
    'list':'allpages',
    'apnamespace': 10,  # Template
    'apprefix': args.old,
    'aplimit': 500,
})['allpages']

n = 1
for c in old_pages:
    old = c['title']
    new = old.replace(args.old, args.new)
    if old == new:
        print('Skipping %s (no change)' % old)
    util.logf('Moving %s to %s... ' % (old, new))
    old_page = user.get_page(old)
    if not old_page.exists:
        util.log('Old page does not exist', type='error')
        continue
    new_page = user.get_page(new)
    if new_page.exists:
        util.log('New page exists', type='error')
        continue
    summary = 'Migrating versioned template (%i/%i)' % (n, len(old_pages))
    user.api_request({
        'action': 'move',
        'from': old,
        'to': new,
        'movetalk': True,
        'reason': summary,
        'token': user.edit_token,
    })
    util.log('<green>Done.')
    n += 1
