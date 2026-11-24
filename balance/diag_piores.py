import json, random, sys, statistics as S, multiprocessing as mp
import sim, sim2, diag_classes as D
scn=sim.load(); J=scn['jobs']; G=sim.gear(scn['items'])
def jid(n,r): return next(j for j in J if j['name']==n and j['race']==r)
FOC=[jid('Time Mage',3),jid('Illusionist',1),jid('Summoner',4),jid('Bishop',2),jid('Morpher',3)]
D.FM.update({(lv,k):D.field_mean(lv,k) for lv in (10,25,45) for k in ('spd','mp')})
def task(a):
    xf,j,lv,n,seed=a; sim2.P['OBS']=0; sim2.reset_stats(); rng=random.Random(seed); random.seed(seed+7); w=0
    for _ in range(n):
        o=rng.sample([x for x in J if x is not j],5); me=sim2.mk(j,lv,G,scn['abil']); D.XF[xf](me,lv)
        A=[me]+[sim2.mk(x,lv,G,scn['abil']) for x in o[:2]]; B=[sim2.mk(x,lv,G,scn['abil']) for x in o[2:]]
        r,_=sim2.battle(A,B,rng); w+=r
    st=sim2.STATS; cn=j['name']; tot=max(1,st['acts'][(cn,lv)])
    top=[(k[2],round(v/tot*100)) for k,v in sorted(st['use'].items(),key=lambda kv:-kv[1]) if k[0]==cn and k[1]==lv][:4]
    mpu=st['mp'][(cn,lv)]/max(1,st['mpn'][(cn,lv)])
    return dict(xf=xf,cls=f"{cn}/{j['race']}",lv=lv,win=w/n,top=top,mp=mpu)
if __name__=='__main__':
    V=['completo','só Fight (sem habilidades)','sem habilidades de status','velocidade = média do campo','MP = média do campo']
    T=[(x,j,lv,1500,5) for x in V for j in FOC for lv in (10,25,45)]
    with mp.Pool(4) as p: R=p.map(task,T,chunksize=2)
    json.dump(R,open('diag_piores.json','w'),ensure_ascii=False)
    cls=[];[cls.append(r['cls']) for r in R if r['cls'] not in cls]
    print('| classe | nível | '+' | '.join(V)+' | habilidades mais usadas (completo) | MP gasto |'); print('|---|---|'+'---|'*(len(V)+2))
    for c in cls:
        for lv in (10,25,45):
            row=[next(r for r in R if r['cls']==c and r['lv']==lv and r['xf']==x) for x in V]
            print(f'| {c} | {lv} | '+' | '.join(f"{r['win']*100:.0f}%" for r in row)+f" | {row[0]['top']} | {row[0]['mp']:.0f} |")
