import json

# Charger les données
with open("final_dataset_fixed.jsonl", "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]

# Nettoyer les targets
for entry in dataset:
    cleaned_contributions = []
    for contrib in entry["target"]:
        if isinstance(contrib, dict):
            contrib.pop("contribution_id", None)
            contrib.pop("description", None)
            contrib.pop("paper_id", None)
            cleaned_contributions.append(contrib)
    entry["target"] = cleaned_contributions

# Sauvegarde dans un nouveau fichier
with open("contributions.jsonl", "w", encoding="utf-8") as f:
    for item in dataset:
        json.dump(item, f, ensure_ascii=False)
        f.write("\n")

print(f"✅ {len(dataset)} entrées nettoyées et enregistrées.")
