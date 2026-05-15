import duckdb
import argparse
import sqlite3
import psycopg2
import sys
from pathlib import Path


def translate_schema_sqlite2pgsql3(schema_sql):
    import sqlglot
    return sqlglot.transpile(schema_sql, read="sqlite", write="postgres")[0]
def translate_schema_sqlite2pgsql(schema_sql):
    return schema_sql \
    .replace(' DATETIME',' TIMESTAMP') \
    .replace(' VARCHAR(4000)',' TEXT') \
    .replace('CN INTEGER','CN VARCHAR(34)') \
    .replace('"','') \
    .replace('P1PNTCNT_EU INTEGER','P1PNTCNT_EU BIGINT') \
    .replace('P1POINTCNT INTEGER','P1POINTCNT BIGINT') \
    .replace('P2POINTCNT INTEGER','P2POINTCNT BIGINT') \
    #.replace(' REAL',' DOUBLE PRECISION')  #Technically SQLITE REAL is 64-bit, but FIA DB doesn't really need it that big

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

    print(f"Extracting Schemas and Indices from SQLITE: {args.sqlite_path}")
    with sqlite3.connect(f'file:{args.sqlite_path}?mode=ro', uri=True) as con:
        schemas = {name:sql for name, sql in con.execute("SELECT name, sql FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND sql IS NOT NULL;")}
        indices = {name:sql for name, sql in con.execute("SELECT name, sql FROM sqlite_master WHERE type = 'index' AND name NOT LIKE 'sqlite_%' AND sql IS NOT NULL;")}
    #translating to pgsql syntax
    pg_schemas = {schema_name:translate_schema_sqlite2pgsql(schema_sql) for schema_name, schema_sql in schemas.items()}
    print("Connecting to PGSQL directly to create schemas")
    with psycopg2.connect(host=args.dbdir, dbname=args.dbname, user=args.user, port=args.port) as con:
        for schema_name, schema_sql in pg_schemas.items():
            print(f'\t{schema_name}')
            print(f'\t\t{schema_sql}')
            cur = con.cursor()
            cur.execute(f'DROP TABLE IF EXISTS {schema_name};')
            cur.execute(f'{schema_sql};')

    print(f"Establishing Duckdb {args.duckdb_path}")
    with duckdb.connect(f'{args.duckdb_path}') as con:
        print(f"Attaching SQLITE from within DUCKDB")
        con.execute('INSTALL sqlite;')
        con.execute('LOAD sqlite;')
        con.execute(f"ATTACH '{args.sqlite_path}' as slite (TYPE sqlite);")
        tables = con.execute('SHOW tables FROM slite;').fetchall()
        assert tables, "No tables"


        print(f"Dumping tables into {args.duckdb_path}")
        for table, in tables:
            print(f'\t{table}')
            con.execute(f'CREATE OR REPLACE TABLE {table} AS FROM slite.{table};')

        print(f"Applying Indices on {args.duckdb_path}")
        for name, index_sql in indices:
            print(f'\t{name}')
            con.execute(index_sql)
        print("Done with SQLITE, DETACHing.")
        con.execute('DETACH slite;')

        duckdb_tables = con.execute('SHOW tables;').fetchall()
        assert len(tables) == len(duckdb_tables), f"mismatch in tables: {set(tables).difference(set(duckdb_tables))}"


        print("Connecting to PGSQL from within DUCKDB")
        con.execute('INSTALL postgres;')
        con.execute('LOAD postgres;')
        con.execute(f"ATTACH 'dbname={args.dbname} host={args.dbdir} user={args.user} port={args.port}' as pg (TYPE postgres);")
        print("Copying tables to PGSQL from DUCKDB")
        for schema_name,schema_sql in pg_schemas.items():
            print(f'\t{schema_name}')
            # apparently duckdb will insist on table name case, so if it's upper case
            # it will be wrapped in quotes. Will make referencing tables harder within PGSQL
            # so, lowering...
            cols = [c[0] for c in con.execute(f"DESCRIBE {schema_name}").fetchall()]
            cols_lower = [c.lower() for c in cols]
            cols_lower_str = ','.join(cols_lower)
            cols_as_lower = [f'{c} AS {c_lower}' for c,c_lower in zip(cols, cols_lower)]
            cols_as_lower_str = ', '.join(cols_as_lower)
            #sql_cmd = f'CREATE OR REPLACE TABLE pg.{table.lower()} AS SELECT {cols_as_lower_str} FROM {table};'
            sql_cmd = f'INSERT INTO pg.{schema_name.lower()}({cols_lower_str}) SELECT {cols_as_lower_str} FROM {schema_name};'
            #print(sql_cmd)
            con.execute(sql_cmd)


    print("Connecting to PGSQL directly to apply indices")
    with psycopg2.connect(host=args.dbdir, dbname=args.dbname, user=args.user, port=args.port) as con:
        for name, index_sql in indices.items():
            print(f'\t{name}')
            print(f'\t\t{index_sql}')
            cur = con.cursor()
            cur.execute(index_sql)

    print("Done migrating to Duckdb and PGSQL")
