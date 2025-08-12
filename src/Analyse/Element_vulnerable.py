
import os
import requests
import json
from dotenv import load_dotenv
import sys
from pathlib import Path

# Configuration des chemins relatifs adaptée à la nouvelle structure
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ANALYSE_DIR = SRC_DIR / "Analyse"  
PRETRAITEMENT_DIR = PROJECT_ROOT / "pretraitement2"
PROMPT_DIR = SRC_DIR / "prompt"
OUTPUT_DIR = SRC_DIR / "output"
output_md = OUTPUT_DIR / "analysis" / "element_vulnerable.md"  
# Ajouter les modules au path
import sys
sys.path.append(str(ANALYSE_DIR))  # Changé : ANALYSE_DIR au lieu d'AUTO_CHUNKER_DIR


sys.path.append(str(PROMPT_DIR))

# Imports
from file_conversion import extract_pages  # Import depuis src/Analyse
from templates import prompt_de_base

load_dotenv()
llm_key = os.getenv("llm_key")

# Chemins des fichiers
input_md = os.path.join(PRETRAITEMENT_DIR, 'DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md')
with open(input_md, "r", encoding="utf-8") as f:
    document_text = f.read()

pages = extract_pages(document_text)  # Liste des textes de chaque page

# Charger le contexte JSON depuis le nouveau répertoire
json_path = OUTPUT_DIR / "context" / "resultats_context_llm.json"  
with open(json_path, "r", encoding="utf-8") as f:
    pages_data = json.load(f)

main_goal = pages_data[0].get("pageSummary", "")

# Fichier de sortie dans le nouveau répertoire

os.makedirs(os.path.dirname(output_md), exist_ok=True)

with open(output_md, "a", encoding="utf-8") as md_file:
    for idx, (page_content, page_ctx) in enumerate(zip(pages, pages_data)):
        # 1. pageSummary de la page courante
        page_summary = page_ctx.get("pageSummary", "")

        # 2. globalSummary de la page courante
        global_summary = page_ctx.get("updatedGlobalSummary", "")

        # 3. lastPageSummary :
        #    - si idx == 0 : on reprend le page_summary de la même page
        #    - sinon       : on prend pageSummary de la page précédente
        if idx == 0:
            last_page_summary = page_summary
        else:
            last_page_summary = pages_data[idx-1].get("pageSummary", "")

        # 4. lastSectionTitle : titre de section de la page précédente
        last_section_title = (
            pages_data[idx-1].get("sectionTitle", "")
            if idx > 0 else
            page_ctx.get("sectionTitle", "")
        )

        # 5. isContinuation
        is_continuation = page_ctx.get("isContinuation", False)

        # 6. Construction du prompt
        
        prompt = prompt_de_base.format(
            globalSummary=global_summary,
            lastPageSummary=last_page_summary,
            PageSummary=page_summary,
            pageContent=page_content,
            but_principal=main_goal,
        )

        # 7. Appeler l'API LLM avec gestion d'erreurs améliorée
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {llm_key}", 
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                    "temperature": 0.4,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content']

            # 8. Afficher et écrire le résultat
            print(f"Page {idx+1} : {result}")
            md_file.write(f"\n---\n\n# Page {idx+1}\n\n{result}\n")
            
        except requests.RequestException as e:
            print(f"Erreur API pour la page {idx+1}: {e}")
            md_file.write(f"\n---\n\n# Page {idx+1}\n\nErreur lors du traitement: {e}\n")
        except KeyError as e:
            print(f"Erreur de format de réponse pour la page {idx+1}: {e}")
            md_file.write(f"\n---\n\n# Page {idx+1}\n\nErreur de format de réponse: {e}\n")
        except Exception as e:
            print(f"Erreur inattendue pour la page {idx+1}: {e}")
            md_file.write(f"\n---\n\n# Page {idx+1}\n\nErreur inattendue: {e}\n")

print("Analyse terminée. Résultats sauvegardés dans src/Analyse/reponse.md")