#!/usr/bin/env python
import csv
import json
import os

import datetime
from dateutil.parser import parse
from peewee import *

import header_help as h


db = PostgresqlDatabase('spend', user='rossjones')

def minimalist_xldate_as_datetime(xldate, datemode=0):
    # datemode: 0 for 1900-based, 1 for 1904-based
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate + 1462 * datemode)
    ).isoformat()

class SpendRecord(Model):
    department = TextField(index=True)
    entity = TextField()
    date = DateField(index=True)
    expense_type = TextField()
    expense_area = TextField()
    supplier = TextField()
    transaction = TextField()
    amount = DecimalField(decimal_places=2)
    description = TextField()
    supplier_postcode = TextField(null=True)
    supplier_type = TextField(null=True)
    contract_number = TextField(null=True)
    project_code = TextField(null=True)
    expenditure_type = TextField(null=True)

    class Meta:
        database = db # This model uses the "people.db" database.

    def __repr__(self):
        return f'''
            {self.department} - {self.entity}
            {self.date}
            {self.expense_type} - {self.expense_area}
            {self.supplier}
            {self.transaction} - £{self.amount}
            {self.description}
            {self.supplier_postcode} - {self.supplier_type}
            {self.contract_number} - {self.project_code}
            {self.expenditure_type}
        '''

    def from_row(self, row, idx):
        def _get_from_row(column, row, idx):
            i = idx.get(column)
            if i == -1 or i >= len(row):
                return ''
            return row[i] or ''

        self.department = _get_from_row(h.Column.DEPT, row, idx)
        self.entity = _get_from_row(h.Column.ENTITY, row, idx)

        self.expense_type = _get_from_row(h.Column.EXPENSE_TYPE, row, idx)
        self.expense_area = _get_from_row(h.Column.EXPENSE_AREA, row, idx)
        self.supplier = _get_from_row(h.Column.SUPPLIER, row, idx)
        self.transaction = _get_from_row(h.Column.TRANSACTION, row, idx)
        self.description = _get_from_row(h.Column.DESCRIPTION, row, idx)
        self.supplier_postcode = _get_from_row(h.Column.SUPPLIER_POSTCODE, row, idx)
        self.supplier_type = _get_from_row(h.Column.SUPPLIER_TYPE, row, idx)
        self.contract_number = _get_from_row(h.Column.CONTRACT_NUM, row, idx)
        self.project_code = _get_from_row(h.Column.PROJECT_CODE, row, idx)
        self.expenditure_type = _get_from_row(h.Column.EXPENDITURE_TYPE, row, idx)

        # Fix the date ...
        date = _get_from_row(h.Column.DATE, row, idx)
        if not date:
            date = '01/01/2000'  # Unknoqn date
        try:
            self.date = parse(date)
        except:
            try:
                date = minimalist_xldate_as_datetime(int(date))
                self.date = parse(date)
            except:
                print(f"Bad date: {date}")

        if self.date:
            self.date = self.date.isoformat()
        else:
            self.date = datetime.datetime(year=2000, month=1, day=1).isoformat()

        # Fix the amount if it is included.
        amt = _get_from_row(h.Column.AMOUNT, row, idx).replace(',', '')
        if amt:
            try:
                self.amount = float(amt)
            except:
                self.amount = 0.0

        if not self.amount:
            self.amount = 0.0


def chunks_of_50(l):
    for i in range(0, len(l), 50):
        yield l[i:i + 50]

def valid_files():
    valid = {}
    with open('validfiles.json', 'r') as f:
        valid = json.load(f)

    for k, v in valid.items():
        yield k, v

def read_until_headers(reader):
    headers = []
    while True:
        try:
            headers = reader.__next__()
        except StopIteration:
            break
        except csv.Error:
            break

        count = sum(1 for h in headers if h)
        if count > 5:
            break

    if not headers:
        return []

    return headers

def try_file(f, db):
    row_count = 0

    reader = csv.reader(open(f, 'r',encoding="utf-8", errors="ignore"))
    headers = read_until_headers(reader)
    idx = h.guess_indexes(headers)
    for row in reader:
        # Skip any empty rows
        cell_count = sum(1 for h in row if h.strip())
        if cell_count == 0:
            continue

        db.begin()
        s = SpendRecord()
        s.from_row(row, idx)
        try:
            s.save()
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

        row_count += 1

    # Temporarily do not commit

    return row_count

def process_files(db):
    total_count = 0
    for org, all_files in valid_files():
        print(f"Processing files for {org}")
        row_count = 0
        for files in chunks_of_50(all_files):
            print(f"..processing {len(files)}...")
            for file in files:
                row_count += try_file(file, db)
            break

        print(f'{row_count} rows in {org}')
        total_count += row_count
    print(f'{total_count} rows in total')

if __name__ == '__main__':
    db.connect()
    try:
        print("+ Creating tables")
        db.create_tables([SpendRecord])
        print("+ Tables created")
    except ProgrammingError:
        print("- Tables already exist")

    process_files(db)
    db.close()
