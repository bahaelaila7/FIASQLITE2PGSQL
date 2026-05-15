#!/usr/bin/env bash

. ./pgsql_config.sh

if [ ! -d "${PGDBDIR}" ]; then
  echo "INITIALIZING DB"
  initdb -D "${PGDBDIR}" -U ${USER}
fi
pg_ctl -D "${PGDBDIR}" -l pglogfile start -o "-p $PORT"
