import os
import requests
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Configuration des chemins relatifs adaptée à la nouvelle structure
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ANALYSE_DIR = SRC_DIR / "Analyse"  # Changé : src/Analyse au lieu d'auto_chunker
PRETRAITEMENT_DIR = PROJECT_ROOT / "pretraitement2"
PROMPT_DIR = SRC_DIR / "prompt"

sys.path.append(str(PROMPT_DIR))
from templates import prompt_context

# Imports des modules locaux
from file_conversion import extract_pages  # Import depuis src/Analyse

# Charger les variables d'environnement
load_dotenv(PROJECT_ROOT / ".env")
api_key = os.getenv("llm_key")

def main():
    """Fonction principale pour l'analyse de contexte"""
    
    # Vérifier que la clé API est disponible
    if not api_key:
        print("❌ Erreur: Clé API non trouvée. Vérifiez votre fichier .env")
        return
    
    # Lire le contenu du fichier
    input_path = PRETRAITEMENT_DIR / "DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md"
    
    if not input_path.exists():
        print(f"❌ Erreur: Fichier non trouvé: {input_path}")
        return
    
    with open(input_path, "r", encoding="utf-8") as f:
        document_text = f.read()
    
    # Extraire les pages du document
    pages = extract_pages(document_text)
    print(f"📄 Document chargé: {len(pages)} pages détectées")
    
    # Initialiser les variables pour le suivi du résumé et des sections
    global_summary = ""
    last_page_summary = ""
    last_section_title = ""
    is_continuation = False
    
    # Chemins des fichiers de sortie dans le nouveau répertoire
    OUTPUT_DIR = SRC_DIR / "output"
    output_md = OUTPUT_DIR / "context" / "resultats_context_llm.md"
    output_json = OUTPUT_DIR / "context" / "resultats_context_llm.json"
    
    # S'assurer que le dossier de sortie existe
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    
    pages_json = []
    successful_pages = 0
    failed_pages = 0
    
    print(f"📁 Fichiers de sortie:")
    print(f"  - Markdown: {output_md}")
    print(f"  - JSON: {output_json}")
    print("\n🚀 Démarrage de l'analyse de contexte...\n")
    
    with open(output_md, "w", encoding="utf-8") as md_file:  # Changé "a" en "w" pour écraser
        md_file.write("# Analyse de contexte du document\n\n")
        md_file.write(f"Document source: {input_path.name}\n")
        md_file.write(f"Nombre de pages: {len(pages)}\n")
        md_file.write(f"Date d'analyse: {json.dumps(pages_json, default=str)}\n\n")
        
        for idx, page_content in enumerate(pages):
            print(f"📄 Traitement de la page {idx + 1}/{len(pages)}...")
            
            # Créer le prompt
            prompt = prompt_context.format(
                globalSummary=global_summary,
                lastPageSummary=last_page_summary,
                lastSectionTitle=last_section_title,
                pageContent=page_content,
                isContinuation=is_continuation
            )
            
            # Appeler l'API LLM avec gestion d'erreurs
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}", 
                        "Content-Type": "application/json"
                    },
                    data=json.dumps({
                        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                        "temperature": 0.1,  # Température plus basse pour plus de cohérence
                        "messages": [{"role": "user", "content": prompt}]
                    }),
                    timeout=30  # Timeout de 30 secondes
                )
                
                response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
                
                response_json = response.json()
                result = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Traitement de la réponse JSON
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
                        
                        # Mettre à jour les variables pour la prochaine itération
                        last_page_summary = page_summary
                        last_section_title = section_title
                        global_summary = updated_global_summary
                        
                        # Afficher les résultats
                        print(f"✅ Page {idx + 1} traitée avec succès")
                        print(f"   📑 Section: {section_title}")
                        print(f"   📝 Résumé: {page_summary[:100]}...")
                        
                        # Écrire dans le fichier markdown
                        md_file.write(f"\n---\n\n# Page {idx + 1}\n\n")
                        md_file.write(f"**Section Title:** {section_title}\n\n")
                        md_file.write(f"**Page Summary:** {page_summary}\n\n")
                        md_file.write(f"**Updated Global Summary:** {updated_global_summary}\n\n")
                        md_file.write(f"**Is Continuation:** {is_continuation}\n\n")
                        
                        # Ajouter à la liste pour le JSON
                        pages_json.append({
                            "page": idx + 1,
                            "sectionTitle": section_title,
                            "pageSummary": page_summary,
                            "updatedGlobalSummary": updated_global_summary,
                            "isContinuation": is_continuation
                        })
                        
                        successful_pages += 1
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ Erreur de décodage JSON pour la page {idx + 1}: {e}")
                        print(f"   Contenu brut: {result[:200]}...")
                        failed_pages += 1
                        
                        # Ajouter une entrée d'erreur dans le JSON
                        pages_json.append({
                            "page": idx + 1,
                            "error": "JSON decode error",
                            "raw_content": result[:500]  # Limiter la taille
                        })
                        
                else:
                    print(f"❌ Format inattendu pour la page {idx + 1}")
                    print(f"   Contenu: {result[:200]}...")
                    failed_pages += 1
                    
                    # Ajouter une entrée d'erreur dans le JSON
                    pages_json.append({
                        "page": idx + 1,
                        "error": "Unexpected format",
                        "raw_content": result[:500]
                    })
                    
            except requests.RequestException as e:
                print(f"❌ Erreur lors de l'appel API pour la page {idx + 1}: {e}")
                failed_pages += 1
                
                # Ajouter une entrée d'erreur dans le JSON
                pages_json.append({
                    "page": idx + 1,
                    "error": f"API request error: {str(e)}"
                })
                
            except Exception as e:
                print(f"❌ Erreur inattendue pour la page {idx + 1}: {e}")
                failed_pages += 1
                
                # Ajouter une entrée d'erreur dans le JSON
                pages_json.append({
                    "page": idx + 1,
                    "error": f"Unexpected error: {str(e)}"
                })
    
    # Écriture du JSON à la fin
    try:
        with open(output_json, "w", encoding="utf-8") as f_json:
            json.dump(pages_json, f_json, ensure_ascii=False, indent=2)
        
        # Résumé final
        print(f"\n Analyse terminée!")
        print(f"Résultats:")
        print(f"   - Pages traitées avec succès: {successful_pages}/{len(pages)}")
        print(f"   - Pages avec erreur: {failed_pages}/{len(pages)}")
        print(f"Fichiers générés:")
        print(f"   - Markdown: {output_md}")
        print(f"   - JSON: {output_json}")
        
        if failed_pages > 0:
            print(f"\n {failed_pages} page(s) ont échoué. Vérifiez les logs ci-dessus.")
        
    except Exception as e:
        print(f" Erreur lors de l'écriture du fichier JSON: {e}")

def validate_setup():
    """Valider la configuration avant de commencer"""
    print(" Validation de la configuration...")
    
    # Vérifier les répertoires
    required_dirs = [PROJECT_ROOT, SRC_DIR, ANALYSE_DIR, PRETRAITEMENT_DIR, PROMPT_DIR]
    for dir_path in required_dirs:
        if not dir_path.exists():
            print(f" Répertoire manquant: {dir_path}")
            return False
        print(f" {dir_path.name}/")
    
    # Vérifier les fichiers critiques
    input_file = PRETRAITEMENT_DIR / "DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md"
    if not input_file.exists():
        print(f" Fichier d'entrée manquant: {input_file}")
        return False
    print(f" Fichier d'entrée trouvé")
    
    # Vérifier la clé API
    if not api_key:
        print(" Clé API manquante dans .env")
        return False
    print(" Clé API configurée")
    
    print(" Configuration validée\n")
    return True

if __name__ == "__main__":
    print("🚀 Script d'analyse de contexte - Architecture src/Analyse/")
    print("=" * 60)
    
    if validate_setup():
        main()
    else:
        print(" Erreur de configuration. Vérifiez votre setup.")