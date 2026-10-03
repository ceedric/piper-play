#!/bin/bash
# Double-click this file to make your play.
# The first time, macOS may ask if you're sure. See the README, Part 6.

cd "$(dirname "$0")" || exit 1

if command -v python3 >/dev/null 2>&1; then
    python3 make_my_play.py
else
    echo "Python isn't installed yet."
    echo "Please see Part 2 of the README, then double-click this file again."
fi

echo
read -r -p "Press Enter to close this window."
