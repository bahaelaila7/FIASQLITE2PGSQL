#!/usr/bin/env bash

podman compose -f start_pgadmin.yaml up --abort-on-container-exit
