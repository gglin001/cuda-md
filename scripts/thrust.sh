#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

exec python "${SCRIPT_DIR}/crawl.py" \
  --base-url "https://nvidia.github.io/cccl/unstable/thrust/" \
  --output-dir "${REPO_ROOT}/docs/thrust" \
  "$@"
