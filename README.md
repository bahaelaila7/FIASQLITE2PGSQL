# FIA SQLite to PGSQL

# Usage
Double check the variables in `pgsql_config.sh` and `migrate_config.sh` then run `migrate.sh`

It will create `.pgsql` local db

Then you may run start the database by running `startpgsql.sh`.

You may create a pgadmin out of the template provided then run `start_pgadmin.sh`

## Requirements
- PostgreSQL installation (commands: `initdb`, `dropdb`, `createdb`, `psql`, `pg_ctl`)
- SQLite installation (command: `sqlite3`)
- core utils: (commands: `grep`, `sed`, `cat`, `mkdir`)
- shell (`bash`)
