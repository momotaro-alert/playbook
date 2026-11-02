#!/bin/bash
# ペットフード協会 /pdf/data/{年}/{n}.pdf を総当たりで取得（404が2連続で打ち切り）
cd /home/user/playbook/pet-data/raw/petfood
for y in $(seq 2013 2026); do
  mkdir -p $y; miss=0
  for n in $(seq 1 25); do
    out=$y/$n.pdf
    if [ -s $out ] && head -c4 $out | grep -q '%PDF'; then miss=0; continue; fi
    r=$(/home/user/playbook/pet-data/work/phase2_fetch.sh "https://petfood.or.jp/pdf/data/$y/$n.pdf" $out)
    if head -c4 $out | grep -q '%PDF'; then echo "OK $r"; miss=0; else echo "NG $r"; rm -f $out; mv $out.meta.txt $y/$n.pdf.notfound.meta.txt; miss=$((miss+1)); fi
    [ $miss -ge 2 ] && break
  done
done
