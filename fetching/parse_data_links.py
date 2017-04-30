#!/usr/bin/env python
# Parse all of the HTML files, and per-organisation generate a
# JSON file with the list of CSV links so we can download them.
import collections
import json
import os

from lxml.html import fromstring

def get_org_directories():
    root = os.path.abspath('./data/html')
    for f in os.listdir(root):
        p = os.path.join(root, f)
        if not os.path.isfile(f):
            yield (f, p)

def get_org_html_files(organisation_path):
    for f in os.listdir(organisation_path):
        p = os.path.join(organisation_path, f)
        if os.path.isfile(p):
            yield p

def parse_file(path):
    links = []
    with open(path, 'r') as f:
        doc = fromstring(f.read())
        links = [a.get('href')
                 for a in doc.cssselect('a')
                 if a.get('href').lower().endswith('.csv')]

    return links


def parse_files(page_generator):
    """ Parse all of the HTML files from the generator and then
        return a list of all the CSV links """
    results = []
    for page in page_generator:
        results.extend(parse_file(page))

    return results

if __name__ == '__main__':

    csv_links = collections.defaultdict(list)

    for org, org_path in get_org_directories():
        html_files = get_org_html_files(org_path)
        csv_links[org] = parse_files(html_files)

    with open('csvlinks.json', 'w') as f:
        json.dump(csv_links, f)
