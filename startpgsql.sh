#!/usr/bin/env bash

. ./pgsql_config.sh

if [ ! -d "${DBDIR}" ]; then
  echo "INITIALIZING DB"
  initdb -D "${DBDIR}" -U ${USER}
fi
pg_ctl -D "${DBDIR}" -l pglogfile start -o "-p $PORT"
