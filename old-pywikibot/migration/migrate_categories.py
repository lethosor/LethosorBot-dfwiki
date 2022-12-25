
import wikibot
util = wikibot.util
parser = wikibot.command_line.parser
parser.add_argument('--old', help='Old sub-namespace', required=True)
parser.add_argument('--new', help='New sub-namespace', required=True)
args = parser.parse_args()
user = wikibot.cred.get_user()

old_cats = user.api_request({
    'list':'allpages',
    'apnamespace': 14,  # Category
    'apprefix': args.old,
    'aplimit': 500,
})['allpages']

n = 1
for c in old_cats:
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
    if new_page.text:
        util.log('New page has content', type='error')
        continue
    new_page.text = old_page.text
    old_page.text = ''
    summary = 'Migrating versioned category (%i/%i)' % (n, len(old_cats))
    user.api_request({
        'action': 'delete',
        'title': old,
        'reason': summary,
        'token': user.edit_token,
    })
    new_page.save(bot=True, summary=summary)
    util.log('<green>Done.')
    n += 1
