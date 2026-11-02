"""helper(目視確認用): キー行の各数値の列幅(隣接数値の中点)で、1ページ目ヘッダ文字を拾って表示。
usage: python3 -I work/phase1_hdr.py <pdf> <key>"""
import sys, re, pdfplumber
def num(t): return re.fullmatch(r'[-−‐－―…]|\(?[\d,]+\)?', t) is not None
path=sys.argv[1]; key=sys.argv[2]
with pdfplumber.open(path) as pdf:
    hp=pdf.pages[0]; hw=hp.extract_words(x_tolerance=1.5)
    for pi,page in enumerate(pdf.pages):
        words=page.extract_words(x_tolerance=1.5)
        tot=[w for w in words if w['text'].replace(' ','').replace('　','')==key]
        if not tot: continue
        y=tot[-1]['top']
        row=sorted([w for w in words if abs(w['top']-y)<4 and num(w['text'])], key=lambda w:w['x0'])
        ytop=min(w['top'] for w in hw if num(w['text']) and w['top']>75 and w['x0']>row[0]['x0']-30)
        chars=[c for c in hp.chars if 45<c['top']<ytop-2]
        xs=[w['x1'] for w in row]
        print(path,'page',pi+1,'ncols',len(row))
        for i,w in enumerate(row):
            lo=xs[i-1]+1 if i>0 else xs[i]-28
            hi=xs[i]+1
            cs=sorted([c for c in chars if lo<=(c['x0']+c['x1'])/2<hi], key=lambda c:(round(c['top']/3),c['x0']))
            print(f"{i+1:2d} {w['text']:>8} | "+''.join(c['text'] for c in cs).replace(' ','')[:80])
        break
