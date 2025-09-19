#!/bin/bash
# Helper script: sets remote and pushes to GitHub (run locally)
set -e
if [ -z "$1" ]; then
  echo "Usage: ./scripts/init_repo.sh git@github.com:USERNAME/REPO.git"
  exit 1
fi
git remote add origin "$1"
git branch -M main
git push -u origin main
