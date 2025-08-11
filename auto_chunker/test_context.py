
import os
import requests
import json
import sys
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("llm_key")
sys.path.append(r'C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\src\prompt')
from templates import prompt_context
from chunking import extract_pages

# Lire le contenu du fichier
with open(r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\pretraitement2\DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md", "r", encoding="utf-8") as f:
    document_text = f.read()

# Extraire les pages du document
pages = extract_pages(document_text)

# Initialiser les variables pour le suivi du résumé et des sections
global_summary = ""
last_page_summary = ""
last_section_title = ""
is_continuation = False

# Chemin du fichier markdown de sortie
output_md = r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\auto_chunker\resultats_context_llm2.md"

with open(output_md, "a", encoding="utf-8") as md_file:
    # Parcourir chaque page
    for idx, page_content in enumerate(pages):
        prompt = prompt_context.format(
            globalSummary=global_summary,
            lastPageSummary=last_page_summary,
            lastSectionTitle=last_section_title,
            pageContent=page_content,
            isContinuation=is_continuation
        )

        # Appel à l'API LLM
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            data=json.dumps({
                "model": "qwen/qwen3-14b:free", 
                "messages": [{"role": "user", "content": prompt}]
            })
        )

        # Vérifier si la réponse est correcte
        if response.status_code == 200:
            response_json = response.json()

            # Extraire la réponse et vérifier si elle est au format JSON ou JSON brut
            result = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Accepter les deux formats : avec ou sans balises ```json
            if (result.startswith("```json") and result.endswith("```")) or result.strip().startswith("{"):
                if result.startswith("```json") and result.endswith("```"):
                    result2 = result.strip("```json").strip("\n```")
                else:
                    result2 = result.strip()
                try:
                    result2 = json.loads(result2)
                    section_title = result2.get("sectionTitle", "")
                    page_summary = result2.get("pageSummary", "")
                    updated_global_summary = result2.get("updatedGlobalSummary", "")
                    is_continuation = result2.get("isContinuation", False)

                    last_page_summary = page_summary
                    last_section_title = section_title
                    global_summary = updated_global_summary

                    # Afficher les résultats ou les stocker
                    print(f"--- Page {idx + 1} ---")
                    print(f"Section Title: {section_title}")
                    print(f"Page Summary: {page_summary}")
                    print(f"Updated Global Summary: {updated_global_summary}")
                    print(f"Is Continuation: {is_continuation}\n")

                    # Écrire dans le fichier markdown
                    md_file.write(f"\n---\n\n# Page {idx + 1}\n\n")
                    md_file.write(f"**Section Title:** {section_title}\n\n")
                    md_file.write(f"**Page Summary:** {page_summary}\n\n")
                    md_file.write(f"**Updated Global Summary:** {updated_global_summary}\n\n")
                    md_file.write(f"**Is Continuation:** {is_continuation}\n\n")

                except json.JSONDecodeError:
                    print(f"Erreur de décodage JSON pour la page {idx + 1}: {result}")
                    print("Contenu brut:", result)
            else:
                print(f"Format inattendu pour la page {idx + 1}: {result}")
                continue
        else:
            print(f"Erreur lors de l'appel API : {response.status_code}")
            print("Détails de l'erreur :", response.text)
