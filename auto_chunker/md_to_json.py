import re
import json

# Chemin du fichier markdown à lire
input_md = r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\auto_chunker\resultats_context_llm.md"
# Chemin du fichier JSON à écrire
output_json = r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\auto_chunker\resultats_context_llm.json"

pages = []
with open(input_md, encoding="utf-8") as f:
    content = f.read()

# Séparer chaque page par le séparateur ---
blocks = re.split(r"^-{3,}\s*$", content, flags=re.MULTILINE)
for block in blocks:
    if not block.strip():
        continue
    # Extraire le numéro de page
    m = re.search(r"# Page (\d+)", block)
    if not m:
        continue
    page_num = int(m.group(1))
    # Extraire les champs
    section = re.search(r"\*\*Section Title:\*\*\s*(.*)", block)
    summary = re.search(r"\*\*Page Summary:\*\*\s*(.*)", block)
    global_summary = re.search(r"\*\*Updated Global Summary:\*\*\s*(.*)", block)
    is_cont = re.search(r"\*\*Is Continuation:\*\*\s*(.*)", block)
    pages.append({
        "page": page_num,
        "sectionTitle": section.group(1).strip() if section else None,
        "pageSummary": summary.group(1).strip() if summary else None,
        "updatedGlobalSummary": global_summary.group(1).strip() if global_summary else None,
        "isContinuation": is_cont.group(1).strip().lower() == "true" if is_cont else None
    })

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)

print(f"Conversion terminée. Résultat écrit dans {output_json}")
