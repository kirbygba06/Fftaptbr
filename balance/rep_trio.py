import json, statistics as S, sim, sys
J={str(j['id']):j for j in sim.load()['jobs']}; race={1:'Hume',2:'Bangaa',3:'Nu Mou',4:'Viera',5:'Moogle'}
labs=sys.argv[1:]; D={n:json.load(open(f'exp3_team_{n}.json')) for n in labs}
e=lambda n,lv,k:25*D[n][lv]['coef'][k] if k in D[n][lv]['avail'] else None
b=labs[0]
for n in labs: print(n,'σ25',round(S.pstdev([e(n,'25',k) for k in J if e(n,'25',k) is not None]),1),'σ45',round(S.pstdev([e(n,'45',k) for k in J if e(n,'45',k) is not None]),1),'ações',round(D[n]['25']['acts']))
W=('Fire','Fira','Firaga','Blizzard','Blizzara','Blizzaga','Thunder','Thundara','Thundaga')
for n in labs:
    if n!=b:
        sh=sorted((e(n,'25',k)-e(b,'25',k),k) for k in J if e(n,'25',k) is not None and e(b,'25',k) is not None)
        print(n,[(J[k]['name']+'/'+race[J[k]['race']][:2],round(d,1)) for d,k in sh[:3]+sh[-3:]])
    for lv in ('25','45'):
        d=D[n][lv]; print(' ',lv,{k.split('|')[1]:round(100*d['best'].get(k,0)/m,1) for k,m in d['evalln'].items() if k.startswith('Black Mage|') and m>200 and k.split('|')[1] in W})
for n in labs:
    print(n,'Black Mage/Red Mage:',[(J[k]['name']+'/'+race[J[k]['race']][:2],round(e(n,'25',k),1),round(e(n,'45',k),1)) for k in J if J[k]['name'] in ('Black Mage','Red Mage') and e(n,'25',k) is not None])
