#!/usr/bin/env bash
initdb -D "${DBDIR}"
pg_ctl -D "${DBDIR}" -l pglogfile start -o "-p $PORT"
