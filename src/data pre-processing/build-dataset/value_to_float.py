import json

cleaned_data = []

with open("final_dataset_cleaned.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)

        # Corriger chaque food_component
        for contrib in entry.get("target", []):
            components = contrib.get("food_components", [])
            for comp in components:
                val = comp.get("value")
                try:
                    # Convertir value en float si possible
                    comp["value"] = float(val)
                except (ValueError, TypeError):
                    # Si non convertible, mettre à null
                    comp["value"] = None

        cleaned_data.append(entry)

# Sauvegarde
with open("final_dataset_fixed.jsonl", "w", encoding="utf-8") as f:
    for item in cleaned_data:
        json.dump(item, f, ensure_ascii=False)
        f.write("\n")

print(f"✅ Fichier nettoyé avec {len(cleaned_data)} lignes.")
