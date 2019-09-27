# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import configparser
import urllib.request as rq
import re

config = configparser.ConfigParser()
config.read('inf.ini')

USER = config['DEFAULT']['USER']
PASS = config['DEFAULT']['PASS']
URL = f'{config["DEFAULT"]["URL"]}record000/'

pass_mgr = rq.HTTPPasswordMgrWithDefaultRealm()
pass_mgr.add_password(realm=None, uri=URL, user=USER, passwd=PASS)
auth_handler = rq.HTTPBasicAuthHandler(pass_mgr)
opener = rq.build_opener(auth_handler)
rq.install_opener(opener)

html = rq.urlopen(URL).read()
soup = BeautifulSoup(html, 'html.parser')

for tr in soup.find_all('tr'):
    a = tr.find('a')
    file_name = re.findall("P[0-9]{6}_[0-9]{6}_[0-9]{6}.265", str(a))
    if len(file_name) > 0:
        path = f'./{file_name[0]}'
        url = f'{URL}{file_name[0]}'
        print('url:', url)
        rq.urlretrieve(url, path)
