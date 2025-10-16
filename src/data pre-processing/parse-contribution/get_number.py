import json

def analyser_fichier(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nb_items = len(data)
    total_food_components = sum(len(item.get("food_components", [])) for item in data)

    print(f"Nombre d'éléments dans le fichier : {nb_items}")
    print(f"Nombre total de 'food_components' : {total_food_components}")
    return nb_items, total_food_components

# Exemple d'utilisation
json_path = "high_quality_contributions.json"
analyser_fichier(json_path)
