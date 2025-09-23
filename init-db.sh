#!/bin/bash
set -e

# Perform all actions as the 'postgres' user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create database for directus
    CREATE DATABASE ${DIRECTUS_DB_NAME};
    CREATE USER ${DIRECTUS_DB_USER} WITH PASSWORD '${DIRECTUS_DB_PASSWORD}';
    GRANT ALL PRIVILEGES ON DATABASE ${DIRECTUS_DB_NAME} TO ${DIRECTUS_DB_USER};

    -- Create database for the inventory service
    CREATE DATABASE ${GITEA_DB_NAME};
    CREATE USER ${GITEA_DB_USER} WITH PASSWORD '${GITEA_DB_PASSWORD}';
    GRANT ALL PRIVILEGES ON DATABASE ${GITEA_DB_NAME} TO ${GITEA_DB_USER};
EOSQL


echo "Granting full schema permissions for Directus database"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="${DIRECTUS_DB_NAME}" <<-EOSQL
    -- This is the recommended, more complete grant for an application user
    GRANT ALL PRIVILEGES ON SCHEMA public TO ${DIRECTUS_DB_USER};
EOSQL

echo "Granting full schema permissions for Gitea database"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="${GITEA_DB_NAME}" <<-EOSQL
    -- Applying the same robust grant for the Gitea user
    GRANT ALL PRIVILEGES ON SCHEMA public TO ${GITEA_DB_USER};
EOSQL
