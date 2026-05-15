#!/usr/bin/env bash

. ./pgsql_config.sh

if [ ! -d "${PGDBDIR}" ]; then
  echo "${PGDBDIR} does not exist"
  exit 1
fi
pg_ctl -D "${PGDBDIR}" -l pglogfile stop -o "-p $PORT"
