import json

# Charger le JSON des contributions
with open("west african food composition table/contributions/v5/grouped_contributions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Fonction pour vérifier si un composant est complet
def is_complete_component(comp):
    return (
        comp.get("label") and
        comp.get("value") is not None and
        comp.get("unit")
    )

# Filtrer les contributions de qualité
high_quality_contributions = []

for contrib in data:
    components = contrib.get("food_components", [])

    # Vérifie si TOUS les composants sont valides
    if components and all(is_complete_component(c) for c in components):
        high_quality_contributions.append(contrib)

# Sauvegarder dans un nouveau fichier
with open("west african food composition table/contributions/v5/high_quality_contributions.json", "w", encoding="utf-8") as f:
    json.dump(high_quality_contributions, f, ensure_ascii=False, indent=2)

print(f"✅ {len(high_quality_contributions)} contributions de bonne qualité conservées.")
