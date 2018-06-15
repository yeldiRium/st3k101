#!/usr/bin/env bash

set -e

psql -v ON_ERROR_STOP=1 --dbname "$POSTGRES_DB" --username "$POSTGRES_USER" <<-EOSQL
    CREATE EXTENSION HSTORE;
EOSQL