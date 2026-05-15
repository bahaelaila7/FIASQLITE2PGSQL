#!/usr/bin/env bash

. ./pgsql_config.sh

if [ ! -d "${PGDBDIR}" ]; then
  echo "INITIALIZING DB"
  initdb -D "${PGDBDIR}" -U ${USER}
  sed -i 's|#unix_socket_directories =.*$|unix_socket_directories = '"'$PGDBDIR'"'|' "${PGDBDIR}/postgresql.conf"
fi
pg_ctl -D "${PGDBDIR}" -l pglogfile start -o "-p $PORT"
