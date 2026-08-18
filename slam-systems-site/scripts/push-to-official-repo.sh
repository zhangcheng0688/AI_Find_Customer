#!/usr/bin/env bash
# Publish the WATERMOON SLAM.SYSTEMS official site to its own GitHub repo.
# Default destination: https://github.com/zhangcheng0688/slam-systems-site
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST_URL="${1:-https://github.com/zhangcheng0688/slam-systems-site.git}"
WORK="$(mktemp -d /tmp/slam-official-XXXXXX)"

cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

cp -a "$ROOT"/. "$WORK/"
rm -rf "$WORK/.git" "$WORK/node_modules" "$WORK/scripts/push-to-official-repo.sh"

# Official production host
printf 'slam.systems\n' > "$WORK/CNAME"
printf '' > "$WORK/.nojekyll"

cd "$WORK"
git init -b main
git add -A
git commit -m "SLAM.SYSTEMS official website (watermoon.communication gmbh)"
git remote add origin "$DEST_URL"
# Fresh single-commit history on every publish, so the push must replace remote main.
git push -u --force origin main

echo
echo "Published to $DEST_URL"
echo "If GitHub Pages is enabled on that repo, open:"
echo "  https://zhangcheng0688.github.io/slam-systems-site/"
