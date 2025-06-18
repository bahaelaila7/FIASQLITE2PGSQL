#!/usr/bin/env bash

echo "DUMPING DATA TO CSV"
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


