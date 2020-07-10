#!/usr/bin/env bash
#
set -eo pipefail

shopt -s nullglob dotglob

PROGNAME=$(basename $0)

# Provide an option to override values via env variables
: ${BKPINTERVAL:="900"}
: ${LOCK_FD:="200"}
: ${LOCK_FILE:="/var/lock/${PROGNAME}.lock"}
: ${S3_BUCKET:="sqlite"}
: ${DATABASE_PATH:="/app/data.db"}

export S3_BUCKET DATABASE_PATH

err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ($PROGNAME): ERROR: $@" >&2
}

status() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ($PROGNAME): $@"
}

lock() {
  eval "exec $LOCK_FD>$LOCK_FILE"
  flock -n $LOCK_FD || ( err "Cannot aquire lock on ${LOCK_FILE}" ; exit 1; )
}

cleanup() {
  shopt -u nullglob dotglob
}

finish() {
  local exit_status="${1:-$?}"
  if [[ "$exit_status" -eq 0 ]]; then
    status "DONE (exit code: ${exit_status})"
  else
    err "exit code: ${exit_status}"
  fi
  cleanup
  exit $exit_status
}

trap finish SIGHUP SIGINT SIGQUIT SIGTERM ERR

lock
status '-r invoked'
while :;do
   status "Starting backup"
  /usr/local/bin/sqlite-to-s3.sh backup
   status "DONE."
   status "Next backup in $BKPINTERVAL seconds..."
   sleep "$BKPINTERVAL"
done

finish
