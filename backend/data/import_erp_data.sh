#!/bin/bash

# Define database and CSV file
DB_NAME="erp_database.db"
CSV_FILE="ERP_data.csv"
TABLE_NAME="erp_table"

# Run SQLite commands
sqlite3 "$DB_NAME" <<EOF
.mode csv
.headers on
.import $CSV_FILE $TABLE_NAME
SELECT * FROM $TABLE_NAME LIMIT 5;
.exit
EOF
