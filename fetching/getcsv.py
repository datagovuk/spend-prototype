#!/usr/bin/env python
# Use the output of the GOV.UK API to find spend>25k

import collections
import json
import os
import time

from dotmap import DotMap
import requests

def ensure_dir(name):
    p = os.path.abspath(f'data/csv/{name}')
    if not os.path.exists(p):
        os.makedirs(p)

def download(url, filename):
    full_url = f'https://gov.uk{url}'
    r = requests.get(full_url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


if __name__ == '__main__':
    counter = 0
    root = os.path.abspath(f'data/csv/')

    data = json.load(open('csvlinks.json', 'r'))
    for k, v in data.items():
        ensure_dir(k)
        l = len(v)
        print(f'{k} has {l} links')

        for link in v:
            filename = link.split('/')[-1]
            target = os.path.join(root, k, filename)

            if os.path.exists(target) and \
                os.stat(target).st_size > 0:
                continue

            if 'nationalarchives.gov.uk' in link:
                continue

            print(f"Writing to {target}")
            download(link, target)
            time.sleep(0.3)


    print(f'That is about {counter} links in total')
    #download('https://gov.uk/government/uploads/system/uploads/attachment_data/file/463723/05._Transparency_Report_Aug_1516_CSV.csv', '/tmp/x.csv')
