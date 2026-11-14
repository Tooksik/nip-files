"""Із меж admin_level=4 (OSM) робить список областей: id, назва, межі з невеликим запасом."""
import json, sys
IDS = {
    "Вінницька область": "vinnytsia", "Волинська область": "volyn", "Дніпропетровська область": "dnipro",
    "Донецька область": "donetsk", "Житомирська область": "zhytomyr", "Закарпатська область": "zakarpattia",
    "Запорізька область": "zaporizhzhia", "Івано-Франківська область": "ivano-frankivsk",
    "Київська область": "kyiv", "Кіровоградська область": "kirovohrad", "Луганська область": "luhansk",
    "Львівська область": "lviv", "Миколаївська область": "mykolaiv", "Одеська область": "odesa",
    "Полтавська область": "poltava", "Рівненська область": "rivne", "Сумська область": "sumy",
    "Тернопільська область": "ternopil", "Харківська область": "kharkiv", "Херсонська область": "kherson",
    "Хмельницька область": "khmelnytskyi", "Черкаська область": "cherkasy", "Чернівецька область": "chernivtsi",
    "Чернігівська область": "chernihiv",
}
only = {x.strip() for x in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if x.strip()}
data = json.load(open(sys.argv[1]))
boxes = {}
def walk(c, acc):
    if isinstance(c[0], (int, float)): acc.append(c)
    else:
        for x in c: walk(x, acc)
for f in data["features"]:
    p = f.get("properties", {})
    name = p.get("name:uk") or p.get("name")
    if name not in IDS: continue
    pts = []; walk(f["geometry"]["coordinates"], pts)
    if not pts: continue
    b = [min(x for x, y in pts), min(y for x, y in pts), max(x for x, y in pts), max(y for x, y in pts)]
    old = boxes.get(name)
    boxes[name] = b if not old else [min(old[0], b[0]), min(old[1], b[1]), max(old[2], b[2]), max(old[3], b[3])]
m = 0.08
for name, b in sorted(boxes.items()):
    rid = IDS[name]
    if only and rid not in only: continue
    title = "Київська область і Київ" if rid == "kyiv" else name
    print(f"{rid}\t{title}\t{b[0]-m:.3f},{b[1]-m:.3f},{b[2]+m:.3f},{b[3]+m:.3f}")
missing = set(IDS) - set(boxes)
if missing: print("Немає меж для: " + ", ".join(sorted(missing)), file=sys.stderr)
