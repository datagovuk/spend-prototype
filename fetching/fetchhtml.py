#!/usr/bin/env python
# Convert the link.json to html files in directories

import collections
import json
import os
import sys
import time

import requests
import requests_cache

requests_cache.install_cache('fetch_cache')

from dotmap import DotMap

def ensure_dir(name):
    p = os.path.abspath(f'data/html/{name}')
    if not os.path.exists(p):
        os.makedirs(p)

def download(url, filename):
    r = requests.get(url)
    if r.status_code != 200:
        print(f'{url} is broken')
        sys.exit(1)

    if not r.from_cache:
        time.sleep(0.3)

    with open(filename, 'w') as f:
        f.write(str(r.content))


if __name__ == '__main__':

    f = open('links.json', 'r')
    data = json.load(f)
    for slug, links in data.items():
        ensure_dir(slug)

        link_count = len(links)
        time_pred = int(link_count / 3)
        print(f'{slug} has {link_count} links and should take ~{time_pred}s')

        for link in links:
            end = link.split('/')[-1]
            filename = os.path.abspath(f'data/html/{slug}/{end}.html')
            full_link = f'https://gov.uk{link}'

            download(full_link, filename)

