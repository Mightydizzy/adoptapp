import json
from pathlib import Path
from django.conf import settings

DATA_PATH = Path(settings.BASE_DIR) / "pets" / "data" / "comunas-regiones.json"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def regiones():
    data = load_data()
    return [r["region"] for r in data["regiones"]]

def comunas_por_region(region_nombre: str):
    data = load_data()
    for r in data["regiones"]:
        if r["region"] == region_nombre:
            return r["comunas"]
    return []
