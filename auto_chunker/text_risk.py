import os
import requests
import json
from dotenv import load_dotenv
from chunking import extract_pages
import sys
sys.path.append(r'C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\src\prompt')
from templates import prompt_elements_attributes # On utilise le prompt contextuel
from templates import prompt_de_base

load_dotenv()
llm_key = os.getenv("llm_key")

# 1. Charger le texte du document (découpé en pages)
with open(r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\pretraitement2\DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md", "r", encoding="utf-8") as f:
    document_text = f.read()
pages = extract_pages(document_text)  # Liste des textes de chaque page

# 2. Charger le contexte JSON (résumés, titres, etc. pour chaque page)
json_path = r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\auto_chunker\resultats_context_llm.json"
with open(json_path, "r", encoding="utf-8") as f:
    pages_data = json.load(f)
main_goal = pages_data[0].get("pageSummary", "")

# 3. Ouvrir/créer le fichier markdown pour écrire les résultats
output_md = r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\auto_chunker\reponse.md"
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
        
        prompt2=prompt_elements_attributes.format(
            globalSummary=global_summary,
            lastPageSummary=last_page_summary,
            lastSectionTitle=last_section_title,
            pageContent=page_content,
            but_principal=main_goal,
        )
        prompt= prompt_de_base.format(
            globalSummary=global_summary,
            lastPageSummary=last_page_summary,
            PageSummary=page_summary,
            pageContent=page_content,
            but_principal=main_goal,
            
        )
        

        # 7. Appeler l’API LLM
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {llm_key}", "Content-Type": "application/json"},
            data=json.dumps({
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "temperature": 0.4,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        result = response.json()['choices'][0]['message']['content']

        # 8. Afficher et écrire le résultat
        print(f"Page {idx+1} : {result}")
        md_file.write(f"\n---\n\n# Page {idx+1}\n\n{result}\n") 