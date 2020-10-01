#!/bin/sh

sleep 2
export $(grep -v '^#' .env | xargs) ; poetry run uvicorn dcms:app \
    --host 0.0.0.0 \
    --port 80 \
    --proxy-headers \
    --forwarded-allow-ips '*' \
    --use-colors \
    $(test "$API_ROOT_PATH" && echo "--root-path $API_ROOT_PATH") \
    $(test "$DEBUG" && echo "--reload")
