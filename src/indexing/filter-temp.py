import json

# Charger le fichier JSON
with open("food template orkg.json", "r") as f:
    data = json.load(f)

# Clés à supprimer
keys_to_remove = [
    "templateOfResearchProblemLabel",
    "templateOfResearchProblem",
    "templateOfResearchFieldLabel",
    "templateOfResearchField",
    "targetClassLabel",
    "targetClass",
    "propertyShapeMaxCount",
    "propertyShapeMinCount"
]

# Supprimer les clés indésirables
cleaned_data = []
for item in data:
    cleaned_item = {k: v for k, v in item.items() if k not in keys_to_remove}
    cleaned_data.append(cleaned_item)

# Retirer les doublons selon le champ propertyShapePathLabel
seen_labels = set()
unique_data = []
for item in cleaned_data:
    label = item.get("propertyShapePathLabel")
    if label and label not in seen_labels:
        seen_labels.add(label)
        unique_data.append(item)

# Sauvegarde du résultat
with open("cleaned_unique_data.json", "w") as f:
    json.dump(unique_data, f, indent=4)

# Affichage pour vérification
print(json.dumps(unique_data, indent=4))
