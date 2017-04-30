#!/usr/bin/env python3
import collections
from enum import Enum


class Column(Enum):
    DEPT = 1
    ENTITY = 2
    DATE = 3
    EXPENSE_TYPE = 4
    EXPENSE_AREA = 5
    SUPPLIER = 6
    TRANSACTION = 7
    AMOUNT = 8
    DESCRIPTION = 9
    SUPPLIER_POSTCODE = 10
    SUPPLIER_TYPE = 11
    CONTRACT_NUM = 12
    PROJECT_CODE = 13
    EXPENDITURE_TYPE = 14


TREASURY_HEADERS = {
    'department family': Column.DEPT,
    'department': Column.DEPT,
    'entity': Column.ENTITY,
    'date':  Column.DATE,
    'transaction date': Column.DATE,
    'expense type': Column.EXPENSE_TYPE,
    'expense area': Column.EXPENSE_AREA,
    'supplier': Column.SUPPLIER,
    'transaction number': Column.TRANSACTION,
    'transaction': Column.TRANSACTION,
    'amount': Column.AMOUNT,
    'description': Column.DESCRIPTION,
    'supplier postcode': Column.SUPPLIER_POSTCODE,
    'supplier type': Column.SUPPLIER_TYPE,
    'contract number': Column.CONTRACT_NUM,
    'project code': Column.PROJECT_CODE,
    'expenditure type': Column.EXPENDITURE_TYPE,
}


def is_treasury_header(header):
    return header.lower() in TREASURY_HEADERS


def _get_potential_headers(c):
    poss = []
    for k, v in TREASURY_HEADERS.items():
        if v == c:
            poss.append(k)
    return poss

def guess_indexes(headers):
    """ Takes a list of headers, and returns a dict where the key
    is the column enum, and the value is the index into the headers
    list """
    result = collections.defaultdict(int)
    for column in Column:
        potential = _get_potential_headers(column)
        pos = 0
        for h in headers:
            if h.lower() in potential:
                result[column] = pos
                break
            pos += 1
        if column not in result:
            result[column] = -1

    return result


if __name__ == '__main__':
    # Test
    h = ['department', 'transaction date', 'transaction']
    res = guess_indexes(h)
    assert res[Column.DEPT] == 0
    assert res[Column.DATE] == 1
    assert res[Column.TRANSACTION] == 2

    h = ['department name', 'transaction date', 'transaction']
    res = guess_indexes(h)
    assert res[Column.DEPT] == -1
    assert res[Column.DATE] == 1
    assert res[Column.TRANSACTION] == 2

