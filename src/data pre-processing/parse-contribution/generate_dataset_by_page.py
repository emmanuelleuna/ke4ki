import pdfplumber
import json
import re
from collections import defaultdict

# === 1. Extraction page par page du PDF ===
def extract_pdf_pages(pdf_path):
    segments = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                segments.append({
                    "page": i + 1,
                    "text": text.strip()
                })
    return segments

# === 2. Matching intelligent d'une contribution à une page ===
def contribution_matches_text(contribution, text):
    text_lower = text.lower()
    name_matches = []

    local_name = (contribution.get("local_name") or "").lower()
    common_name = (contribution.get("common_name") or "").lower()

    # Direct matching
    if local_name and local_name in text_lower:
        name_matches.append("local_name")

    if common_name and common_name in text_lower:
        name_matches.append("common_name")

    # Prefix matching via food_component_label
    for component in contribution.get("food_components", []):
        label = component.get("label", "")
        if "_" in label:
            prefix = label.split("_")[0].lower()
            if prefix and prefix in text_lower:
                name_matches.append("component_prefix")
                break

    return len(name_matches) > 0

# === 3. Construire la map page → contributions ===
def build_page_contribution_map(contributions, segments):
    page_map = defaultdict(list)
    for contrib in contributions:
        for seg in segments:
            if contribution_matches_text(contrib, seg["text"]):
                page_map[seg["page"]].append(contrib)
    return page_map

# === 4. Générer le dataset final ===
def build_dataset(segments, page_contributions):
    dataset = []
    for seg in segments:
        page = seg["page"]
        text = seg["text"]
        target_contribs = page_contributions.get(page, [])

        if target_contribs:
            dataset.append({
                "input": f"Page {page}:\n{text}",
                "target": target_contribs
            })
    return dataset

# === 5. Sauvegarde en JSONL ===
def save_jsonl(dataset, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in dataset:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")
    print(f"✅ {len(dataset)} entrées sauvegardées dans {output_path}")

# === MAIN ===
def main():
    pdf_path = "west african food composition table/paper/ca7779b.PDF"
    contrib_path = "west african food composition table/contributions/v5/high_quality_contributions.json"
    output_path = "west african food composition table/contributions/v5/contribution_dataset_westafrican.jsonl"

    print("📥 Extraction du PDF...")
    segments = extract_pdf_pages(pdf_path)

    print("📥 Chargement des contributions...")
    with open(contrib_path, "r", encoding="utf-8") as f:
        contributions = json.load(f)

    print("🔍 Matching des contributions aux pages...")
    page_contributions = build_page_contribution_map(contributions, segments)

    print("🧪 Génération du dataset final...")
    dataset = build_dataset(segments, page_contributions)

    print("💾 Sauvegarde...")
    save_jsonl(dataset, output_path)

if __name__ == "__main__":
    main()
