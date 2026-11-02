#!/bin/bash
# usage: phase3_fetch.sh URL OUTPATH  -> saves file + .meta.txt
url="$1"; out="$2"
code=$(curl -sS -L -A 'Mozilla/5.0' --max-time 60 -o "$out" -w '%{http_code}' "$url")
printf 'URL: %s\n取得日: 2026-11-02\nHTTPステータス: %s\n' "$url" "$code" > "$out.meta.txt"
echo "$code $out $(stat -c %s "$out" 2>/dev/null)"
sleep 2
