"""
Clears the sandbox (DF wiki)

Arguments:
--last-line: The beginning of the last line to keep
--sandbox: Title of sandbox; defaults to 'Project:Sandbox'
--no-prompt: If present, do not prompt before saving
"""

import wikibot

def run():
    user = wikibot.cred.get_user()
    args = wikibot.command_line.parse_args()
    
    last_line = args['last-line'] if 'last-line' in args else wikibot.util.input('Last line: ')
    sandbox = args['sandbox'] if 'sandbox' in args else 'Project:Sandbox'
    silent = 'no-prompt' in args
    
    page = user.get_page(sandbox)
    lines = page.text.splitlines()
    text = ''
    for line in lines:
        text += line + '\n'
        if line.startswith(last_line):
            break
    
    if not silent:
        print(text)
        wikibot.util.input('\nEnter to save, Ctrl-C to abort: ')
    page.text = text
    page.save('Emptying sandbox', bot=1)
    wikibot.util.log('Emptied sandbox')

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Aborted')
