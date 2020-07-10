#!/usr/bin/env bash

set -e -o pipefail

err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ($PROGNAME): ERROR: $@" >&2
}

status() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ($PROGNAME): $@"
}


: ${DATABASE_PATH:="/app/data.db"}
: ${S3_BUCKET:="sqlite"}

export DATABASE_PATH S3_BUCKET

if [[ ! -z $AWS_ACCESS_KEY_ID && ! -z $AWS_SECRET_ACCESS_KEY ]]; then
  status "==> AWS CREDS DETECTED"
  if ! test -f $DATABASE_PATH ; then /usr/local/bin/sqlite-to-s3.sh restore || true ;fi
fi

exec /usr/sbin/uwsgi --ini /etc/uwsgi/uwsgi.ini --die-on-term
