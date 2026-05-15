import duckdb
import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbdir', type=Path)
    parser.add_argument('--duckdb_path', type=Path)
    parser.add_argument('--sqlite_path', type=Path)
    parser.add_argument('--dbname', type=str)
    parser.add_argument('--port', type=int, default=5432)
    parser.add_argument('--user', type=str)

    args = parser.parse_args()
    assert args.dbdir.exists(), f"PostgreSQL Path {args.dbdir} does not exist"
    assert args.sqlite_path.exists(), f"Sqlite path {args.sqlite_path} does not exist"
    #assert args.duckdb_path.exists(), f"Duckdb path {args.duckdb_file} does not exist"

    con=duckdb.connect(f'{args.duckdb_path}')
    con.execute('INSTALL sqlite;')
    con.execute('LOAD sqlite;')
    con.execute(f"ATTACH '{args.sqlite_path}' as slite (TYPE sqlite);")
    tables = con.execute('SHOW tables FROM slite;').fetchall()
    assert tables, "No tables"

    con.execute('INSTALL postgres;')
    con.execute('LOAD postgres;')
    con.execute(f"ATTACH 'dbname={args.dbname} host={args.dbdir} user={args.user} port={args.port}' as pg (TYPE postgres);")

    for table, in tables:
        print(table)
        print('\tduckdb<<sqlite')
        con.execute(f'CREATE OR REPLACE TABLE {table} AS FROM slite.{table};')

    for table, in tables:
        print(table)
        print('\tduckdb>>pgsql')
        # apparently duckdb will insist on table name case, so if it's upper case
        # it will be wrapped in quotes. Will make referencing tables harder within PGSQL
        # so, lowering...
        print(f'CREATE OR REPLACE TABLE pg.{table.lower()} AS FROM {table};')
