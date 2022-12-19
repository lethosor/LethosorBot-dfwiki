import configparser

import mwclient

def make_site(config_filepath):
    c = configparser.ConfigParser()
    c.read(config_filepath)
    site = mwclient.Site(c['site']['domain'], path=c['site'].get('path'))
    site.login(c['site']['username'], c['site']['password'])
    return site
