#!/usr/bin/env python
# Use the output of the GOV.UK API to find spend>25k
import collections
import csv
import json
import os

import header_help as helper

ROOT = os.path.abspath('./data/csv/')


def find_headers(reader):
    headers = []
    while True:
        try:
            headers = reader.__next__()
        except StopIteration:
            break
        except csv.Error:
            break

        if len(headers) > 5:
            break

    if not headers:
        return []

    return headers

def is_treasury(filename):
    with open(filename, 'r',encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)

        headers = find_headers(reader)
        if not headers:
            print(f"No headers in {filename}")
            return False

        matches = sum([1 for h in headers if helper.is_treasury_header(h)])

        return matches > 4



if __name__ == '__main__':
    valid = collections.defaultdict(list)
    total = 0
    true_count = 0
    for (dirpath, dirnames, filenames) in os.walk(ROOT):
        for f in filenames:
            filename = os.sep.join([dirpath, f])
            org = filename.split('/')[-2]
            name = '/'.join(filename.split('/')[-2:])

            total += 1
            if is_treasury(filename):
                true_count += 1
                valid[org].append(filename)

            #matches = is_treasury(filename)
    print(f'{true_count} out of {total} are treasury formatted-ish')
    with open('validfiles.json', 'w') as f:
        json.dump(valid, f)

