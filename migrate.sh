#!/usr/bin/env bash

. ./pgsql_config.sh
. ./migrate_config.sh

./echos.sh && \
./dump_schema.sh && \
./countrows.sh && \
./build_migration.sh && \
./startpgsql.sh && \
./dump_data.sh && \
./pgcopy.sh

echo "Configure start_pgadmin.yaml from the template, and run start_pgadmin.sh (requires docker, rootless is ok)"
