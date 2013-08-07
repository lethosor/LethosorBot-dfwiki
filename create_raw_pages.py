"""
Creates DF raw pages

File format: (These values on one line, tab-separated)
* Page name
* File (with namespace)
* Category type (creature, inorganic, etc.)
* Object type (CREATURE, INORGANIC, etc.)
* Object ID (e.g. BIRD_BLUEJAY)
* Creature variation files (optional, pipe-separated) 
"""

import wikibot

class CreateRawTask(wikibot.bot.Task):
    pass

class CreateRawJob(wikibot.bot.Job):
    pass

def run():
    """ Runs the script """
    user = wikibot.cred.get_user();
    args = wikibot.command_line.parse_args();
    # Obtain a file
    if not 'file' in args:
        while 1:
            fp = wikibot.util.input('File path: ')
            try:
                f = open(fp)
            except IOError:
                pass
            except Exception:
                return
            else:
                break
        contents = f.read();
        f.close()

if __name__ == '__main__':
    run()
