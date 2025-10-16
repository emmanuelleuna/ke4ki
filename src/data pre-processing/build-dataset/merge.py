import json

# Fichiers source
fichier1 = "Composition of dishes consumed in Cameroon/contributions/contribution_dataset_cmr.jsonl"
fichier2 = "west african food composition table/contributions/contribution_dataset.jsonl"

# Fichier de sortie
fichier_sortie = "final_dataset.jsonl"

# Liste pour stocker les objets JSON
donnees = []

# Lire et ajouter les données du premier fichier
with open(fichier1, 'r', encoding='utf-8') as f1:
    for ligne in f1:
        donnees.append(json.loads(ligne.strip()))

# Lire et ajouter les données du second fichier
with open(fichier2, 'r', encoding='utf-8') as f2:
    for ligne in f2:
        donnees.append(json.loads(ligne.strip()))

# Écrire le tout dans un nouveau fichier
with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
    for item in donnees:
        f_out.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Concaténation terminée : {len(donnees)} éléments écrits dans {fichier_sortie}")
