# Spend Prototype

This prototype consists of some ETL scripts in ```fetching``` which retrieves a few million transactions from spend-data scraped from gov.uk.

## Spending Prototype

Spending Prototype is small elixir app that provides a UI for interacting with the spend database.  The database is created from the ETL scripts.

## ETL Scripts

These scripts take just over 74 minutes to process 4,606,759 transactions. A few hundred thousand not imported due to failures in formatting.  Over 1000 original pages, we ended up with 1,1993 CSV files.

