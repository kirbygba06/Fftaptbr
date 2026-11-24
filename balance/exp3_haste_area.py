import json, multiprocessing as mp
import exp3
from exp3 import jj
def sp(**k): return dict(base='orig', **k)
V={'original':sp(),'Haste em área (raio 1)':sp(mods={'Haste':{'area':'r1/v2'}}),'Haste em área (raio 1) e dura 4':sp(mods={'Haste':{'area':'r1/v2'}},dur={'Haste':4}),'Haste em área (raio 2)':sp(mods={'Haste':{'area':'r2/v2'}})}
ids=jj('Time Mage')+jj('Templar')
if __name__=='__main__':
    T=[(l,s,i,lv,2000,511) for l,s in V.items() for i in ids for lv in (10,25,45)]
    with mp.Pool(4) as p: R=p.map(exp3.strat_task,T,chunksize=2)
    json.dump(R,open('exp3_haste_area.json','w'),ensure_ascii=False)
    base={(r['cls'],r['lv']):r['win'] for r in R if r['label']=='original'}
    print('| variante | classe | 10 | 25 | 45 | ações (25) |\n|---|---|---|---|---|---|')
    for lab in V:
        for c in sorted({r['cls'] for r in R}):
            rr={r['lv']:r for r in R if r['label']==lab and r['cls']==c}
            print(f"| {lab} | {c} | "+' | '.join(f"{rr[lv]['win']*100:.0f}%"+('' if lab=='original' else f" ({(rr[lv]['win']-base[(c,lv)])*100:+.0f})") for lv in (10,25,45))+f" | {rr[25]['acts']:.0f} |")
