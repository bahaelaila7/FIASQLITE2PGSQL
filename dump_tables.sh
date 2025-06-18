#!/usr/bin/env bash

sqlite3 "$SQLITE_FIADB" ".schema" > $RAW_SCHEMA
sqlite3 "$SQLITE_FIADB" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';" > $TABLE_LIST

mkdir -p "$CSV_DIR"

while read -r table; do
  echo "Exporting $table"
  sqlite3 "$SQLITE_FIADB" <<EOF
.headers on
.mode csv
.output "${CSV_DIR}/${table}.csv"
SELECT * FROM "$table";
EOF
done < $TABLE_LIST


