#!/usr/bin/env bash

echo "DUMPING SCHEMA TO SQL FILES"
sqlite3 "$SQLITE_FIADB" ".schema" > $RAW_SCHEMA
sqlite3 "$SQLITE_FIADB" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';" > $TABLE_LIST
