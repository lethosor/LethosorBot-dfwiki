"""
Creates DF raw pages

File format: (These values on one line, tab-separated)
* Page name
* File (with namespace)
* Category type (creature, inorganic, etc.)
* Object type (CREATURE, INORGANIC, etc.)
* Object ID (e.g. BIRD_BLUEJAY)
* Creature variation files (optional, pipe-separated)

Required command-line arguments (will be prompted if left blank):
* file: Path to file (described above)
* namespace: Namespace to create pages in
Optional (will not be prompted):
* overwrite: If present, overwrites existing pages
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
    def __init__(self, user, page_list, text, summary='Creating raw page ({0}/{1})',
                 data=None, overwrite=False):
        if data is None:
            data = {}
        super(CreateRawTask, self).__init__(user, CreateRawJob, data)
        self.text, self.summary, self.overwrite = text, summary, overwrite
        self.page_names = page_list

class CreateRawJob(wikibot.bot.Job):
    def run(self):
        if self.page.text != "" and not self.task.overwrite:
            return False
        self.page.text = self.format(self.task.text)
        return True
    
    def save(self):
        self.page.save(
            summary=self.task.summary.format(*self.count),
            bot=1
        )

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
    if not 'namespace' in args:
        namespace = wikibot.util.input('Namespace (blank for main): ')
    else:
        namespace = args['namespace']
    overwrite = 'overwrite' in args
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
        page_name = namespace + ':' + d[0] + '/raw'
        pages.append(page_name)
        template = templates['var'] if len(d) > 5 else templates['std']
        data[page_name] = {}
        data[page_name]['text'] = wikibot.util.str_format(template, data=d)
    
    task = CreateRawTask(user, pages, '{% data[text] %}', data=data, overwrite=overwrite)
    task.run_all()

if __name__ == '__main__':
    run()
