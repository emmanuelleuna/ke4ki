import json
from collections import defaultdict

# === 1. Charger le fichier JSON plat ===
with open("west african food composition table/contributions/v5/dataset-v5.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2. Regrouper par ID de contribution ===
contributions = {}

for entry in data:
    cid = entry["contribution"]
    if cid not in contributions:
        # Création d'un nouvel objet contribution
        contributions[cid] = {
            "contribution_id": cid,
            "paper": entry.get("paper"),
            "geo_area": entry.get("geo_area_label"),
            "local_name": entry.get("local_name_label"),
            "common_name": entry.get("common_name_label"),
            "food_group": entry.get("food_group_label"),
            "food_components": []  
        }

    # Ajout du food_component (s’il est présent)
    if "food_component_label" in entry and entry["food_component_label"]:
        component = {
            "label": entry["food_component_label"],
            "value": entry.get("numeric_value"),
            "unit": entry.get("unit_label")
        }

        if component not in contributions[cid]["food_components"]:
            contributions[cid]["food_components"].append(component)


# === 3. Résultat final : liste de contributions propres ===
grouped_contributions = list(contributions.values())

# === 4. Sauvegarde dans un fichier structuré ===
with open("west african food composition table/contributions/v5/grouped_contributions.json", "w", encoding="utf-8") as f:
    json.dump(grouped_contributions, f, ensure_ascii=False, indent=2)

print(f"✅ {len(grouped_contributions)} contributions regroupées et sauvegardées dans grouped_contributions.json")
