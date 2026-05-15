#!/usr/bin/env bash

. ./pgsql_config.sh

export SQLITE_FIADB="${HOME}/Documents/projects/FIA/SQLite_FIADB_ENTIRE.db"
export DUCKDB_FIADB="${DB}.duckdb"

./startpgsql.sh &&
  dropdb --if-exists -h "$SOCKET" -p $PORT -U "$DBUSER" "$DB" &&
  createdb -h "$SOCKET" -p $PORT -U "$DBUSER" "$DB" &&
  python sqlite2duckdb2pgsql.py --sqlite_path "$SQLITE_FIADB" --duckdb_path "${DUCKDB_FIADB}" --dbdir "$PGDBDIR" --user "$USER" --port "$PORT" --dbname "$DB"

echo "Configure start_pgadmin.yaml from the template, and run start_pgadmin.sh (requires docker, rootless is ok)"
echo "You will need to have a signed TLS certificate for pgadmin"
cat <<EOF
You can create a self-signed one with the following commands: 
# this is to create the a private key with no passkey using a 384-bit elliptical curve algorithm
$ openssl ecparam -name secp384r1 -genkey -noout -out privateec384.nopass.pem

# create the public key matching the private one
$ openssl ec -in privateec384.nopass.pem -pubout -out publicec384.nopass.pem

# create a certificate and sign it with the key set just generated, valid for 10 years
$ openssl req -new -key privateec384.nopass.pem -x509 -days 3650 -out certec384.pem
EOF
