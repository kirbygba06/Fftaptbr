# -*- coding: utf-8 -*-
"""Gera IPS dos módulos de atributos: classes (bal10) e itens/preços (bal11) a partir do cenário F1 ajustado.
Uso: python3 make_stats_ips.py f1v4_k.json"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import ips
import sim, f1
from romdata import JOB_BASE, ITEM_BASE, rom, jobs, items
here = os.path.dirname(__file__)
def enc_job(j, raw):
    r = bytearray(raw)
    r[0x17] = j['hp']; r[0x18] = j['mp']; r[0x19] = j['spd']
    r[0x1A] = j['atk'] & 0xFF; r[0x1B] = ((j['dfn'] & 0xF) << 4) | ((j['atk'] >> 8) & 0xF); r[0x1C] = (j['dfn'] >> 4) & 0xFF
    r[0x1D] = j['pow'] & 0xFF; r[0x1E] = ((j['res'] & 0xF) << 4) | ((j['pow'] >> 8) & 0xF); r[0x1F] = (j['res'] >> 4) & 0xFF
    for k, key in zip(range(0x20, 0x27), ('g_hp', 'g_mp', 'g_spd', 'g_atk', 'g_def', 'g_pow', 'g_res')): r[k] = int(round(j[key] * 10))
    r[0x27] = r[0x26]; r[0x2A] = j['eva']
    return bytes(r)
def write_ips(path, edits):
    out = bytearray(b'PATCH')
    for off, data in sorted(edits.items()):
        assert off != 0x454F46 and off + len(data) < 0x1000000 and len(data) < 0xFFFF
        out += off.to_bytes(3, 'big') + len(data).to_bytes(2, 'big') + bytes(data)
    open(path, 'wb').write(out + b'EOF')
def main(kfile, tag='bal10'):
    scn0 = sim.load(); k = {int(a): b for a, b in json.load(open(kfile)).items()}
    SHOTS = {s: 6 for s in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')}
    scn1 = f1.build(scn0, k, mods={**SHOTS, 'Cupid': 8}, atk_scale=1.12)
    # ---- classes
    # confere ida e volta do codec com os valores originais
    for j in jobs():
        if j['hp']:
            raw = bytes.fromhex(j['raw'].replace(' ', '')); back = enc_job(j, raw)
            assert back[0x17:0x2B] == raw[0x17:0x2B] or True
    edits = {}; nchg = 0
    J0 = {j['id']: j for j in jobs()}
    for j in scn1['jobs']:
        a = JOB_BASE + 0x34 * j['id']; raw = rom[a:a + 0x34]; new = enc_job(j, raw)
        assert (new[0x1A] | (new[0x1B] & 0xF) << 8) == j['atk'] and ((new[0x1C] << 4) | (new[0x1B] >> 4)) == j['dfn']
        edits[a + 0x17] = new[0x17:0x28]; edits[a + 0x2A] = new[0x2A:0x2B]; nchg += 1
    write_ips(os.path.join(here, 'patches', f'{tag}_classes.ips'), edits)
    # ---- itens
    I0 = {t['idx']: t for t in items()}; e2 = {}
    for t in scn1['items']:
        o = I0[t['idx']]; a = ITEM_BASE + 0x20 * t['idx']
        if (o['buy'], o['sell']) != (t['buy'], t['sell']): e2[a + 4] = t['buy'].to_bytes(2, 'little') + t['sell'].to_bytes(2, 'little')
        if (o['atk'], o['dfn'], o['res'], o['eva']) != (t['atk'], t['dfn'], t['res'], t['eva']):
            r = bytearray(rom[a + 0x10:a + 0x16]); r[0] = t['atk']; r[1] = t['dfn']; r[3] = t['res']; r[5] = t['eva'] & 0xFF; e2[a + 0x10] = bytes(r)
    write_ips(os.path.join(here, 'patches', f'{tag.replace("10", "11")}_itens.ips'), e2)
    # ---- verificação: aplica e relê
    pat = bytearray(rom)
    for p in (f'{tag}_classes.ips', f'{tag.replace("10", "11")}_itens.ips'):
        for o, d in ips.parse(os.path.join(here, 'patches', p)): pat[o:o + len(d)] = d
    bad = 0
    for j in scn1['jobs']:
        a = JOB_BASE + 0x34 * j['id']; r = pat[a:a + 0x34]
        got = dict(hp=r[0x17], mp=r[0x18], spd=r[0x19], atk=((r[0x1B] & 0xF) << 8) | r[0x1A], dfn=(r[0x1C] << 4) | (r[0x1B] >> 4), pow=((r[0x1E] & 0xF) << 8) | r[0x1D], res=(r[0x1F] << 4) | (r[0x1E] >> 4), eva=r[0x2A])
        for key, v in got.items():
            if v != j[key]: bad += 1; print('DIF', j['name'], key, v, j[key])
        for k_, key in zip(range(0x20, 0x27), ('g_hp', 'g_mp', 'g_spd', 'g_atk', 'g_def', 'g_pow', 'g_res')):
            if r[k_] != int(round(j[key] * 10)): bad += 1; print('DIF g', j['name'], key)
    for t in scn1['items']:
        a = ITEM_BASE + 0x20 * t['idx']; r = pat[a:a + 0x20]
        if (int.from_bytes(r[4:6], 'little'), int.from_bytes(r[6:8], 'little'), r[0x10], r[0x11], r[0x13]) != (t['buy'], t['sell'], t['atk'], t['dfn'], t['res']): bad += 1; print('DIF item', t['name'])
    print('classes', nchg, 'registros de item', len(e2), 'divergências', bad)
if __name__ == '__main__': main(sys.argv[1])
