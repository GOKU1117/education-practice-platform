#!/usr/bin/env bash
set -e

host="db"
port="5432"

echo "Waiting for PostgreSQL at $host:$port ..."
until nc -z "$host" "$port"; do
  sleep 1
done

echo "Database is ready! Starting backend..."
exec "$@"
