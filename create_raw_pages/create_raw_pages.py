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

templates = {
    'std': """\
    <noinclude>{{raw header|{% data[2] %}|{% data[4] %}}}</noinclude>\
    {{raw|{% data[1] %}|{% data[3] %}|{% data[4] %}}}\
    <noinclude>{{raw footer|{% data[2] %}|{% data[4] %}}}</noinclude>
    """.replace('  ', ''),
    'var': """\
    <noinclude>{{raw header|{% data[2] %}|{% data[4] %}}}</noinclude>\
    {{variation raw|{% data[1] %}|{% data[3] %}|{% data[4] %}|{{{1|}}}|\
    {% data[5] %}}}\
    <noinclude>{{raw footer|{% data[2] %}|{% data[4] %}}}</noinclude>
    """.replace('  ', '')
}

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
                wikibot.util.log('Could not open file.')
            except Exception:
                return
            else:
                break
    else:
        try:
            f = open(args['file'])
        except Exception as e:
            util.log(e)
            return
    contents = f.read();
    f.close()
    contents = contents.replace('\r', '')
    array = []
    lines = contents.split('\n')
    lines.remove('')
    for line in lines:
        array.append(line.split('\t'))
    
    pages = []
    data = {}
    for d in array:
        pages.append(d[0])
        template = templates['var'] if len(d) > 5 else templates['std']
        data[d[0]] = {}
        data[d[0]]['text'] = wikibot.util.str_format(template, data=d)
    

if __name__ == '__main__':
    run()
