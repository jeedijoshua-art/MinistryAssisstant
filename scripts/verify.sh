#!/usr/bin/env sh
set -eu
(cd backend && python -m compileall -q app alembic)
(cd frontend && npm run typecheck && npm run build)
