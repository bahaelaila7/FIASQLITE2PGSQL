#!/usr/bin/env bash

export DBDIR="$(pwd)/.pgsql"
export DB="FIADB"
export DBUSER="${USER}"
export PORT=5433
export SOCKET="/tmp"
export SQLITE_FIADB="../SQLite_FIADB_ENTIRE.db"

export TABLE_LIST="tables.txt"
export CSV_DIR="csv_export"
export RAW_SCHEMA="raw_schema.sql"
export SCHEMA_FILE="schema_no_constraints.sql"
export CONSTRAINT_FILE="constraints.sql"
export SCHEMA_MIGRATION_FILE="apply_schema.sql"
export CSV_MIGRATION_FILE="copy_csv.sql"
export CONSTRAINTS_MIGRATION_FILE="apply_constraints.sql"


./echos.sh

./countrows.sh

./dump_tables.sh && \
./build_migration.sh && \
./startpgsql.sh && \
./pgcopy.sh
