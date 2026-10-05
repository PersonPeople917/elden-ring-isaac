import json,sys
L=lambda n:json.load(open(n+".json"))
items,pools,bosses,systems=L("items"),L("pools"),L("bosses"),L("systems")
pids={p["id"] for p in pools}; hooks={s["id"] for s in systems}
issues=[]
def chk(sheet,rows):
    for r in rows:
        for k,v in r.items():
            if v is None: issues.append(f"{sheet}:{r['id']}.{k} unfilled")
            if isinstance(v,dict):
                for kk,vv in v.items():
                    if vv is None: issues.append(f"{sheet}:{r['id']}.{k}.{kk} unfilled")
chk("items",items);chk("pools",pools);chk("bosses",bosses);chk("systems",systems)
for i in items:
    if i["pool"] not in pids: issues.append(f"items:{i['id']} pool unresolved")
for b in bosses:
    if b["drop_pool"] not in pids: issues.append(f"bosses:{b['id']} drop_pool unresolved")
for p in pools:
    for h in (p["chest_hook"],p["enemy_hook"]):
        if h not in hooks: issues.append(f"pools:{p['id']} hook {h} unresolved")
for s in systems:
    if s["needs_pool"] and s["needs_pool"] not in pids: issues.append(f"systems:{s['id']} pool unresolved")
    if not s["verified"]: issues.append(f"systems:{s['id']} not verified in game")
print(len(issues),"open cells/refs");print("\n".join(issues[:15]),"\n..." if len(issues)>15 else "")
sys.exit(1 if issues else 0)
