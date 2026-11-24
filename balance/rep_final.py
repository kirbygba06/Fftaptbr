import json, statistics as S, sim, sys
J={str(j['id']):j for j in sim.load()['jobs']}; race={1:'Hu',2:'Ba',3:'Nu',4:'Vi',5:'Mo'}
labs=sys.argv[1:]; D={n:json.load(open(f'exp3_team_{n}.json')) for n in labs}
def e(n,lv,k): return 25*D[n][lv]['coef'][k] if k in D[n][lv]['avail'] and lv in D[n] else None
for n in labs:
    row=[]
    for lv in ('10','25','45'):
        if lv not in D[n]: continue
        v=[e(n,lv,k) for k in J if e(n,lv,k) is not None]
        row.append(f"{lv}: σ {S.pstdev(v):.1f} máx {max(v):+.1f} mín {min(v):+.1f} fora±5 {sum(abs(x)>5 for x in v)}/{len(v)} ações {D[n][lv]['acts']:.0f}")
    print(n,' | '.join(row))
b=labs[0]
for n in labs[1:]:
    sh=sorted((e(n,'25',k)-e(b,'25',k),k) for k in J if e(n,'25',k) is not None and e(b,'25',k) is not None)
    print(n,'vs',b,[(J[k]['name']+'/'+race[J[k]['race']],round(d,1)) for d,k in sh[:4]+sh[-4:]])
