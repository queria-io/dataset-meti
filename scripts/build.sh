#!/usr/bin/env bash
set -euo pipefail
# 説明 (テーブルの tabledoc.yml) の無いテーブルは掲載しない
export FDL_UNDESCRIBED="${FDL_UNDESCRIBED:-unlisted}"
exec "$(dirname "$0")/../shared/scripts/build-fdl.sh" "$@"
