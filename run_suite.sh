#!/bin/bash
# usage: run_suite.sh LOGFILE [pytest args...]
# Runs from task-tracker; starts Flask on 5050 (macOS AirPlay holds 5000), temporarily points the
# E2E/UI test URLs at 5050, then points them back. Flask's own log is saved next to LOGFILE as LOGFILE.flask.txt
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/task-tracker" || exit 1
LOG="$1"; shift; case "$LOG" in /*) ;; *) LOG="$HERE/$LOG";; esac
FILES=$(ls tests/api/*.py tests/ui/*.py 2>/dev/null)
[ -n "$FILES" ] && sed -i '' 's/127.0.0.1:5000/127.0.0.1:5050/' $FILES
(uv run flask --app app run --port 5050 > "$LOG.flask.txt" 2>&1 &)
for i in $(seq 1 30); do curl -s http://127.0.0.1:5050/api/health >/dev/null && break; sleep 1; done
uv run python -m pytest "$@" 2>&1 | tee "$LOG"
pkill -f "flask --app app run --port 5050" || true
[ -n "$FILES" ] && sed -i '' 's/127.0.0.1:5050/127.0.0.1:5000/' $FILES
