#!/usr/bin/env bash

: ${DATABASE_FILE_PATH:="/app/data/data.db"}
: ${S3_BUCKET:="sqlite"}

set -e -o pipefail

export DATABASE_PATH=$DATABASE_FILE_PATH S3_BUCKET

err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ($PROGNAME): ERROR: $@" >&2
}

status() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ($PROGNAME): $@"
}

set -e -o pipefail

if [[ ! -z $AWS_ACCESS_KEY_ID ]] && [[ ! -z $AWS_SECRET_ACCESS_KEY ]]; then 
  status "==> AWS CREDS DETECTED"
  if [[ ! -f $DATABASE_PATH ]] ; then 
    /usr/local/bin/sqlite-to-s3.sh restore
  else
   status "LOCAL DB FOUND at $DATABASE_PATH!";
  fi
fi
