import json
from collections import Counter, defaultdict

# === 1. Charger les données ===
with open("west african food composition table/contributions/v5/grouped_contributions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total = len(data)
print(f"🔎 Nombre total de contributions : {total}")

# === 2. Contributions nulles / non-nulles ===
null_contribs = [c for c in data if not c.get("food_components")]
non_null_contribs = [c for c in data if c.get("food_components")]

print(f"❌ Contributions sans composants : {len(null_contribs)}")
print(f"✅ Contributions avec composants : {len(non_null_contribs)}")

# === 3. Stats sur les composants par contribution ===
component_counts = [len(c.get("food_components", [])) for c in data]
min_comp = min(component_counts)
max_comp = max(component_counts)
avg_comp = sum(component_counts) / len(component_counts)

print(f"📊 Composants par contribution :")
print(f"   ➤ Min : {min_comp}")
print(f"   ➤ Max : {max_comp}")
print(f"   ➤ Moyenne : {avg_comp:.2f}")

# === 4. Distribution par groupe alimentaire ===
group_counter = Counter()
for c in data:
    group = c.get("food_group", "Inconnu")
    group_counter[group] += 1

print("\n🍽️ Top groupes d'aliments :")
for group, count in group_counter.most_common(10):
    print(f"   - {group}: {count} contributions")

# === 5. Groupe ayant le plus de contributions non-nulles ===
non_null_by_group = defaultdict(int)
for c in non_null_contribs:
    group = c.get("food_group", "Inconnu")
    non_null_by_group[group] += 1

top_group = max(non_null_by_group.items(), key=lambda x: x[1])
print(f"\n🏆 Groupe avec le plus de contributions complètes : {top_group[0]} ({top_group[1]})")

# === 6. Stat sur les composants utilisés (nom du label nutritionnel) ===
component_labels = []
for c in non_null_contribs:
    for comp in c["food_components"]:
        if comp.get("label"):
            component_labels.append(comp["label"])

component_freq = Counter(component_labels)

print("\n💊 Top 10 des composants nutritionnels les plus fréquents :")
for label, freq in component_freq.most_common(10):
    print(f"   - {label}: {freq} apparitions")

# === 7. Longueur moyenne du nom local / commun ===
local_lengths = [len(c["local_name"]) for c in data if c.get("local_name")]
common_lengths = [len(c["common_name"]) for c in data if c.get("common_name")]

if local_lengths:
    print(f"\n📝 Longueur moyenne du nom local : {sum(local_lengths) / len(local_lengths):.2f}")
if common_lengths:
    print(f"📝 Longueur moyenne du nom commun : {sum(common_lengths) / len(common_lengths):.2f}")

# === 8. Contributions sans groupe alimentaire ===
no_group = [c for c in data if not c.get("food_group")]
print(f"\n⚠️ Contributions sans groupe alimentaire : {len(no_group)}")
