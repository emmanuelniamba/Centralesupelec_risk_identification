import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import sys

# Configuration des chemins relatifs
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ANALYSE_DIR = SRC_DIR / "Analyse"
PRETRAITEMENT_DIR = PROJECT_ROOT / "pretraitement2"
PROMPT_DIR = SRC_DIR / "prompt"
OUTPUT_DIR = SRC_DIR / "output"

# Ajouter les modules au path
sys.path.append(str(ANALYSE_DIR))
sys.path.append(str(PROMPT_DIR))

from templates import prompt_aloe
from file_conversion import extract_pages, extract_page, extract

# Charger les variables d'environnement
load_dotenv(PROJECT_ROOT / ".env")
llm_key = os.getenv("llm_key")

def main():
    print("\n" + "=" * 60)
    print("ALOE ANALYSIS - Analyse ALOE")
    print("=" * 60)
    
    # Vérification de la clé API
    if not llm_key:
        print("[ERROR] Clé API non trouvée dans .env")
        return
    
    print("[OK] Clé API configurée")
    
    # 1. Charger le texte du document
    document_path = PRETRAITEMENT_DIR / "DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md"
    print(f"Chargement document: {document_path}")
    
    if not document_path.exists():
        print(f"[ERROR] Document non trouvé: {document_path}")
        return
    
    with open(document_path, "r", encoding="utf-8") as f:
        document_text = f.read()
    
    pages = extract_pages(document_text)
    print(f"[OK] {len(pages)} pages extraites du document")
    
    if len(pages) == 0:
        print("[ERROR] Aucune page extraite du document")
        return
    
    # 2. Charger le contexte JSON
    json_path = OUTPUT_DIR / "context" / "resultats_context_llm.json"
    print(f"Chargement contexte: {json_path}")
    
    if not json_path.exists():
        print(f"[ERROR] Contexte JSON non trouvé: {json_path}")
        print("[INFO] Exécutez d'abord le summarizer pour générer le contexte")
        return
    
    with open(json_path, "r", encoding="utf-8") as f:
        pages_data = json.load(f)
    print(f"[OK] Contexte chargé pour {len(pages_data)} pages")
    
    # 3. Charger les données ALOE
    aloe_path = OUTPUT_DIR / "analysis" / "element_vulnerable.md"
    print(f"Chargement données ALOE: {aloe_path}")
    
    if not aloe_path.exists():
        print(f"[ERROR] Fichier ALOE non trouvé: {aloe_path}")
        print("[INFO] Exécutez d'abord element_vulnerable.py pour générer ce fichier")
        return
    
    with open(aloe_path, "r", encoding="utf-8") as f:
        aloe_data = f.read()
    
    print(f"[OK] Données ALOE chargées ({len(aloe_data)} caractères)")
    
    # Extraire les données ALOE par page - essayer différentes méthodes
    print("[INFO] Extraction des pages ALOE...")
    
    # Méthode 1: extract_page (recherche "Page N :")
    aloe = extract_page(aloe_data)
    
    # Méthode 2: extract (recherche "# Page N" ou "Page N")
    if len(aloe) == 0:
        print("[WARNING] extract_page a échoué, essai avec extract...")
        aloe = extract(aloe_data)
    
    # Méthode 3: extraction par séparateurs "---"
    if len(aloe) == 0:
        print("[WARNING] extract a échoué, essai avec séparateurs...")
        sections = aloe_data.split('---')
        aloe = {}
        for i, section in enumerate(sections):
            if section.strip():
                aloe[i+1] = section.strip()
    
    if len(aloe) == 0:
        print("[ERROR] Impossible d'extraire les pages ALOE")
        print("[DEBUG] Aperçu du contenu ALOE (500 premiers caractères):")
        print(aloe_data[:500])
        return
    
    page_numbers = sorted(aloe.keys())
    ordered_aloe = [aloe[page] for page in page_numbers]
    
    print(f"[OK] {len(ordered_aloe)} pages ALOE extraites")
    print(f"[DEBUG] Pages ALOE disponibles: {page_numbers}")
    
    # Ajuster les données pour avoir la même longueur
    min_length = min(len(pages), len(pages_data), len(ordered_aloe))
    pages = pages[:min_length]
    pages_data = pages_data[:min_length]
    ordered_aloe = ordered_aloe[:min_length]
    
    print(f"[INFO] Ajustement à {min_length} pages pour cohérence")
    
    main_goal = pages_data[0].get("pageSummary", "") if pages_data else ""
    print(f"Objectif principal: {main_goal[:100]}...")
    
    # 4. Créer le fichier de sortie
    output_path = OUTPUT_DIR / "analysis" / "aloe_analyse.md"
    print(f"Fichier de sortie: {output_path}")
    
    # Créer le répertoire de sortie
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Début du traitement de {min_length} pages...")
    print("=" * 60)
    
    successful_pages = 0
    failed_pages = 0
    
    with open(output_path, "w", encoding="utf-8") as md_file:
        # En-tête du fichier
        md_file.write("# Analyse ALOE\n\n")
        md_file.write(f"Document source: {document_path.name}\n")
        md_file.write(f"Pages traitées: {min_length}\n")
        md_file.write(f"Objectif principal: {main_goal}\n\n")
        
        for idx, (page_content, page_ctx, ordered_aloe_content) in enumerate(zip(pages, pages_data, ordered_aloe)):
            print(f"\nTraitement page {idx + 1}/{min_length}")
            
            try:
                # Préparer les données de contexte
                page_summary = page_ctx.get("pageSummary", "")
                global_summary = page_ctx.get("updatedGlobalSummary", "")
                
                if idx == 0:
                    last_page_summary = page_summary
                else:
                    last_page_summary = pages_data[idx-1].get("pageSummary", "")
                
                last_section_title = (
                    pages_data[idx-1].get("sectionTitle", "")
                    if idx > 0 else
                    page_ctx.get("sectionTitle", "")
                )
                
                is_continuation = page_ctx.get("isContinuation", False)
                aloe_content = ordered_aloe_content
                
                print(f"   Résumé page: {len(page_summary)} caractères")
                print(f"   Contenu ALOE: {len(str(aloe_content))} caractères")
                
                # Créer le prompt
                prompt = prompt_aloe.format(
                    globalSummary=global_summary,
                    lastPageSummary=last_page_summary,
                    PageSummary=page_summary,
                    pageContent=page_content,
                    but_principal=main_goal,
                    element_vulnerable_menace=aloe_content
                )
                
                print(f"   Prompt créé ({len(prompt)} caractères)")
                
                # Appeler l'API LLM
                print(f"   Appel API...")
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
                    }),
                    timeout=60
                )
                
                response.raise_for_status()
                result = response.json()['choices'][0]['message']['content']
                
                print(f"   [OK] Résultat obtenu ({len(result)} caractères)")
                print(f"   Aperçu: {result[:100]}...")
                
                # Écrire le résultat
                md_file.write(f"\n---\n\n# Page {idx+1}\n\n{result}\n")
                md_file.flush()
                
                successful_pages += 1
                print(f"   Page {idx+1} traitée avec succès")
                
            except requests.RequestException as e:
                error_msg = f"Erreur API pour la page {idx+1}: {e}"
                print(f"   [ERROR] {error_msg}")
                md_file.write(f"\n---\n\n# Page {idx+1}\n\n**ERREUR API:** {error_msg}\n")
                md_file.flush()
                failed_pages += 1
                
            except KeyError as e:
                error_msg = f"Erreur de format de réponse pour la page {idx+1}: {e}"
                print(f"   [ERROR] {error_msg}")
                md_file.write(f"\n---\n\n# Page {idx+1}\n\n**ERREUR FORMAT:** {error_msg}\n")
                md_file.flush()
                failed_pages += 1
                
            except Exception as e:
                error_msg = f"Erreur inattendue pour la page {idx+1}: {e}"
                print(f"   [ERROR] {error_msg}")
                print(f"   Type d'erreur: {type(e).__name__}")
                md_file.write(f"\n---\n\n# Page {idx+1}\n\n**ERREUR:** {error_msg}\n")
                md_file.flush()
                failed_pages += 1
    
    # Résumé final
    print("\n" + "=" * 60)
    print("ANALYSE ALOE TERMINÉE")
    print("=" * 60)
    print(f"Résultats:")
    print(f"   Pages réussies: {successful_pages}/{min_length}")
    print(f"   Pages échouées: {failed_pages}/{min_length}")
    print(f"Fichier généré: {output_path}")
    
    if output_path.exists():
        file_size = output_path.stat().st_size
        print(f"Taille du fichier: {file_size} octets")
    
    print("=" * 60)
  
if __name__ == "__main__":
    main() 