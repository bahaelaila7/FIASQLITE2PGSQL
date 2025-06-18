#!/bin/bash

PORT=5432


# clean slate
dropdb -h "$SOCKET" -p $PORT -U "$DBUSER" "$DB"
createdb -h "$SOCKET" -p $PORT -U "$DBUSER" "$DB"

# apply schema
psql -h "$SOCKET" -p $PORT -U "$DBUSER" -d "$DB" -f apply_schema.sql
# copy data
psql -h "$SOCKET" -p $PORT -U "$DBUSER" -d "$DB" -f copy_csv.sql
# apply constraints
psql -h "$SOCKET" -p $PORT -U "$DBUSER" -d "$DB" -f apply_constraints.sql
