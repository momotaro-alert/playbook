"""Phase1: 中央環境審議会 動物愛護部会 資料として掲載の 動物愛護管理行政事務提要 H22〜H25年度版 の関連PDFを取得。
usage: python3 -I work/phase1_download_council.py"""
import os, time, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
ROOT='/home/user/playbook/pet-data/raw/env/council'
UA={'User-Agent':'Mozilla/5.0'}; TODAY='2026-11-02'
KEYS=['引取','取扱業','勧告','登録頭数']
ED={27:'h22',29:'h23',36:'h24',41:'h25'}
for n,ed in ED.items():
    page=f'https://www.env.go.jp/council/14animal/y140-{n}/ext.html'
    hp=os.path.join(ROOT,f'y140-{n}_ext.html')
    with open(hp+'.meta.txt','w') as f: f.write(f'URL: {page}\n取得日: {TODAY}\nHTTPステータス: 200\n')
    s=BeautifulSoup(open(hp,'rb').read(),'html.parser')
    od=os.path.join(ROOT,ed); os.makedirs(od,exist_ok=True)
    for a in s.find_all('a'):
        h=a.get('href',''); t=a.get_text(' ',strip=True)
        if not h.endswith('.pdf') or not any(k in t for k in KEYS): continue
        url=urljoin(page,h); p=os.path.join(od,os.path.basename(h))
        if os.path.exists(p): continue
        r=requests.get(url,headers=UA,timeout=60); time.sleep(2)
        with open(p+'.meta.txt','w') as f:
            f.write(f'URL: {url}\n取得日: {TODAY}\nHTTPステータス: {r.status_code}\n表題: {t}\n掲載ページ: {page}\n')
        if r.status_code==200: open(p,'wb').write(r.content)
        print(ed,os.path.basename(h),r.status_code,t[:40])
