#!/bin/sh

sleep 2
export $(grep -v '^#' .env | xargs) ; poetry run uvicorn dcms:app \
    --host 0.0.0.0 \
    --port 443 \
    --proxy-headers \
    --forwarded-allow-ips '*' \
    --use-colors \
    --ssl-keyfile /certs/server.key \
    --ssl-certfile /certs/server.crt \
    $(test "$DEBUG" && echo "--reload")
