#!/usr/bin/env python
import csv
import json
import os

import datetime
from peewee import *

import header_help as h

db = PostgresqlDatabase('spend', user='rossjones', password='pass')
print(db)

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

class OrganisationStatus(Model):
    department = TextField(index=True)
    month = IntegerField()
    year = IntegerField()
    present = BooleanField()

    class Meta:
        database = db # This model uses the "people.db" database.


if __name__ == '__main__':
    db.connect()
    try:
        print("+ Creating tables")
        #db.create_tables([OrganisationStatus])
        print("+ Tables created")
    except ProgrammingError:
        print("- Tables already exist")

    distinct_list = SpendRecord.select(SpendRecord.department).distinct()
    for record in distinct_list:
        if not record.department.strip():
            continue

        db.begin()
        for year in range(2010, 2018):
            for month in range(1, 13):
                print(f'{record.department} -> {month}/{year}')

                q = f'''
                SELECT count(id) from spendrecord
                WHERE
                EXTRACT(MONTH FROM date) = {month} AND
                EXTRACT(YEAR FROM date) = {year} AND
                department= %s;
                '''
                cursor = db.execute_sql(q,[record.department])
                res = cursor.fetchone()

                OrganisationStatus.create(
                    department=record.department,
                    month=month,
                    year=year,
                    present=res[0] > 0
                )
        db.commit()
    db.close()
