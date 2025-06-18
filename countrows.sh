#!/usr/bin/env bash

echo "SHOWING ROW COUNT"
while read -r table; do
	COUNT=$(sqlite3 "$SQLITE_FIADB" "SELECT COUNT(*) FROM $table")
    echo "$table: $COUNT"
done < $TABLE_LIST
