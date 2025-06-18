#!/usr/bin/env bash
echo "INITIALIZING DB"
initdb -D "${DBDIR}"
pg_ctl -D "${DBDIR}" -l pglogfile start -o "-p $PORT"
