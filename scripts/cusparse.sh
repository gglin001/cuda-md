#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

exec python "${SCRIPT_DIR}/crawl.py" \
  --base-url "https://docs.nvidia.com/cuda/cusparse/" \
  --output-dir "${REPO_ROOT}/docs/cusparse" \
  "$@"
