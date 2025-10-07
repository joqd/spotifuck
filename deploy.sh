#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="./deploy.log"
BRANCH="main"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

fail() {
  log "❌ Error: $*"
  exit 1
}

log "🚀 Start deploying for branch '$BRANCH'"

if [ ! -d ".git" ]; then
  fail "There is not .git!"
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
  log "📦 Switch to branch $BRANCH"
  git fetch origin "$BRANCH" || fail "fetch from origin failed"
  git checkout "$BRANCH" || fail "checkout to $BRANCH failed"
fi

log "🔄 pull latest updates from origin/$BRANCH"
git pull origin "$BRANCH" || fail "pull failed"

log "🐳 Recreate services"
docker compose up --build -d --no-deps --remove-orphans || fail "failed to recreate services"

log "🧹 Clearing"
docker image prune -f >/dev/null 2>&1 || true

log "✅ Deployment was successful"
