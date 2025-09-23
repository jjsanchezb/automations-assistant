#!/bin/sh

set -e

/usr/bin/mc alias set minio http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

/usr/bin/mc mb minio/$APP_STORAGE_BUCKET_NAME || true
/usr/bin/mc admin accesskey create minio "$MINIO_ROOT_USER" --access-key "$APP_STORAGE_ACCESS_KEY_ID" --secret-key "$APP_STORAGE_SECRET_ACCESS_KEY"
