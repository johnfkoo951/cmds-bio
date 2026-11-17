#!/usr/bin/env bash
# Production deployment followed by private catalog/cover refresh.
set -euo pipefail
cd "$(dirname "$0")"
vercel deploy --prod --yes --scope johnfkoo951s-projects

# Refresh the private Obsidian/Eagle catalog after a successful production deployment.
CATALOG_HOME="${CMDS_SITE_CATALOG_HOME:-$HOME/DEV/cmds-site-catalog}"
if [[ -f "$CATALOG_HOME/after-deploy.sh" ]]; then
  if ! bash "$CATALOG_HOME/after-deploy.sh" "https://bio.cmdspace.work/"; then
    echo "Deployment succeeded; catalog refresh failed. Retry after-deploy.sh without redeploying." >&2
    exit 2
  fi
else
  echo "Site catalog is not installed on this host; preview refresh was skipped." >&2
fi
