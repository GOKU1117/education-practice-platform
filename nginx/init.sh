#!/bin/bash
set -e
mkdir -p certs

if [ ! -f certs/server.key ] || [ ! -f certs/server.crt ]; then
  echo "Generating SSL certificates..."
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/server.key \
    -out certs/server.crt \
    -subj "/C=US/ST=None/L=None/O=ICSavant/OU=Dev/CN=localhost"
else
  echo "Certificates already exist."
fi

echo "Certificates ready. You can now run"
