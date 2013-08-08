"""
Copies all pages from a namespace to another namespace

Command-line arguments:
* old: The old namespace (required)
* new: The new namespace (required)
* overwrite: If present, overwrites all extisting pages (optional)
* prepend: Text to prepend to new pages (optional)
* prepend-overwrite: Text to prepend to overwritten pages, in addition to
    'prepend' (optional)
* summary: Edit summary (optional)
"""

import wikibot

class NSMigrateTask(wikibot.bot.Task):
    def __init__(self, user, old, new, summary='Migrating namespace {0} to {1}',
                 overwrite=False, prepend='', prepend_overwrite=''):
        summary = summary.format(old, new, old=old, new=new)
        super(NSMigrateTask, self).__init__(user, NSMigrateJob)
        self.old, self.new, self.summary = old, new, summary
        self.overwrite, self.prepend, self.prepend_overwrite = \
            overwrite, prepend, prepend_overwrite

class NSMigrateJob(wikibot.bot.Job):
    def run(self):
        pass
    

def run():
    user = wikibot.cred.get_user()
    args = wikibot.command_line.parse_args()
    prepend = args['prepend'] if 'prepend' in args else ''
    prepend_o = args['prepend-overwrite'] if 'prepend-overwrite' in args else ''
    overwrite = bool(args['overwrite']) if 'overwrite' in args else False
    old = args['old'] if 'old' in args else wikibot.util.input('Old namespace: ')
    new = args['new'] if 'new' in args else wikibot.util.input('New namespace: ')
    if old == new:
        raise ValueError('Old and new namespaces must be different!')
    