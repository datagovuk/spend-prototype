#!/usr/bin/env python
# Use the output of the GOV.UK API to find spend>25k

import collections
import json
from dotmap import DotMap

if __name__ == '__main__':
    links = collections.defaultdict(list)
    f = open('matches.json', 'r')
    data = json.load(f)

    for result in data['results']:
        record = DotMap(result)
        k = record.organisations[0].slug
        v = record.link

        links[k].append(v)

    urls = 0
    for k, v in links.items():
        urls += len(v)

    print(f"Found {urls} urls to scrape in {len(links.keys())} organisations")

    out = open('links.json', 'w')
    json.dump(links, out)
