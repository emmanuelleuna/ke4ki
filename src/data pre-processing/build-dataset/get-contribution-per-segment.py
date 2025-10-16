import json

def compter_contributions_par_segment(fichier_jsonl):
    resultats = []

    with open(fichier_jsonl, 'r', encoding='utf-8') as f:
        for i, ligne in enumerate(f, 1):
            donnees = json.loads(ligne)
            target = donnees.get("target", [])

            total_contributions = len(target)
            total_ingredients = 0
            total_food_components = 0

            for contrib in target:
                ingredients = contrib.get("ingredients", [])
                food_components = contrib.get("food_components", [])

                if isinstance(ingredients, list):
                    total_ingredients += len(ingredients)
                if isinstance(food_components, list):
                    total_food_components += len(food_components)

            total_segment = total_contributions + total_ingredients + total_food_components

            resultats.append({
                "segment": i,
                "nb_contributions": len(target),
                "nb_ingredients": total_ingredients,
                "nb_food_components": total_food_components,
                "total": total_segment
            })

    return resultats

# Exemple d'utilisation
fichier = "final_dataset_fixed.jsonl"
stats = compter_contributions_par_segment(fichier)

# Affichage
for r in stats:
    print(f"Segment {r['segment']} → Total: {r['total']} (Contrib: {r['nb_contributions']}, "
          f"Ingredients: {r['nb_ingredients']}, Food components: {r['nb_food_components']})")
