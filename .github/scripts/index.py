import json, os, sys, datetime
tag, built = sys.argv[1], sys.argv[2]
p = "maps/index.json"
os.makedirs("maps", exist_ok=True)
idx = json.load(open(p)) if os.path.exists(p) else {"regions": []}
regions = {r["id"]: r for r in idx["regions"]}
for line in open(built, encoding="utf-8"):
    rid, name, bounds, size = line.rstrip("\n").split("\t")
    regions[rid] = {
        "id": rid, "name": name, "size": int(size), "version": tag,
        "date": datetime.date.today().strftime("%d.%m.%y"),
        "bounds": [float(x) for x in bounds.split(",")],
        "url": f"https://github.com/Tooksik/nip-files/releases/download/{tag}/{rid}.pmtiles",
    }
idx["regions"] = sorted(regions.values(), key=lambda r: r["name"])
json.dump(idx, open(p, "w"), ensure_ascii=False, indent=1)
print(len(idx["regions"]), "областей у списку")
