import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import sys

# Configuration des chemins relatifs adaptée à la nouvelle structure
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ANALYSE_DIR = SRC_DIR / "Analyse"
PRETRAITEMENT_DIR = PROJECT_ROOT / "pretraitement2"
PROMPT_DIR = SRC_DIR / "prompt"
OUTPUT_DIR = SRC_DIR / "output"
sys.path.append(str(ANALYSE_DIR))
sys.path.append(str(PROMPT_DIR))

from templates import prompt_links
from file_conversion import extract_pages, extract_page, extract

# Charger les variables d'environnement
load_dotenv(PROJECT_ROOT / ".env")
llm_key = os.getenv("llm_key")

def main():
    print("\n" + "="*60)
    print("[MAIN] DÉBUT DE LA FONCTION MAIN()")
    print("="*60)
    
    try:
        # 1. Charger le texte du document (découpé en pages)
        print("📄 [MAIN] Étape 1: Chargement du document...")
        document_path = PRETRAITEMENT_DIR / "DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md"
        print(f"📄 [MAIN] Chemin du document: {document_path}")
        
        if not document_path.exists():
            raise FileNotFoundError(f"Document introuvable: {document_path}")
        
        with open(document_path, "r", encoding="utf-8") as f:
            document_text = f.read()
        
        pages = extract_pages(document_text)
        print(f"[OK] [MAIN] Document chargé: {len(pages)} pages extraites")
        
        # 2. Charger le contexte JSON
        print(" [MAIN] Étape 2: Chargement du contexte JSON...")
        json_path = ANALYSE_DIR / "resultats_context_llm.json"
        print(f"[MAIN] Chemin JSON: {json_path}")
        
        with open(json_path, "r", encoding="utf-8") as f:
            pages_data = json.load(f)
        print(f"[OK] [MAIN] JSON chargé: {len(pages_data)} pages de contexte")
        
        # 3. Charger les données ALOE (optionnel pour ce script)
        print(" [MAIN] Étape 3: Chargement des données ALOE...")
        aloe_path = ANALYSE_DIR / "rt.md"
        print(f" [MAIN] Chemin ALOE: {aloe_path}")
        
        if aloe_path.exists():
            with open(aloe_path, "r", encoding="utf-8") as f:
                aloe_data = f.read()
            print(f"[OK] [MAIN] ALOE chargé: {len(aloe_data)} caractères")
        else:
            print("[WARNING] [MAIN] Fichier ALOE non trouvé, mais optionnel")
        
        # 4. Charger les données d'objets depuis le fichier de réponse précédent
        print(" [MAIN] Étape 4: Chargement des réponses précédentes...")
        reponse_path = ANALYSE_DIR / "reponse.md"
        print(f" [MAIN] Chemin réponse: {reponse_path}")
        
        with open(reponse_path, "r", encoding="utf-8") as f:
            objet_data = f.read()
        
        if not objet_data.strip():
            raise ValueError("Le fichier reponse.md est vide!")
        
        print(f"[OK] [MAIN] Fichier réponse chargé: {len(objet_data)} caractères")
        
        # Extraire et organiser les objets
        print(" [MAIN] Étape 5: Extraction des objets...")
        objet = extract(objet_data)
        print(f" [MAIN] Objets extraits: {len(objet)} pages")
        print(f"[MAIN] Pages trouvées: {list(objet.keys())}")
        
        page_numbers = sorted(objet.keys())
        ordered_objet = [objet[page] for page in page_numbers]
        print(f"[OK] [MAIN] Objets organisés: {len(ordered_objet)} pages")
        
        # Vérifier la cohérence des données
        print(" [MAIN] Étape 6: Vérification de la cohérence...")
        print(f" [MAIN] - Pages document: {len(pages)}")
        print(f" [MAIN] - Pages contexte: {len(pages_data)}")
        print(f" [MAIN] - Pages objets: {len(ordered_objet)}")
        
        if len(pages) != len(pages_data):
            print("[WARNING] [MAIN] ATTENTION: Nombre de pages incohérent!")
            min_pages = min(len(pages), len(pages_data), len(ordered_objet))
            pages = pages[:min_pages]
            pages_data = pages_data[:min_pages]
            ordered_objet = ordered_objet[:min_pages]
            print(f"🔧 [MAIN] Ajusté à {min_pages} pages")
        
        main_goal = pages_data[0].get("pageSummary", "") if pages_data else ""
        print(f" [MAIN] Objectif principal: {main_goal[:100]}...")
        
        # 7. Vérifier la clé API
        print(" [MAIN] Étape 7: Vérification de la clé API...")
        if not llm_key:
            raise ValueError("Clé API LLM manquante!")
        print(f"[OK] [MAIN] Clé API présente: {llm_key[:10]}...")
        
        # 8. Créer le fichier de sortie
        print(" [MAIN] Étape 8: Préparation du fichier de sortie...")
        output_path = ANALYSE_DIR / "Analyse_de_lien.md"
        print(f"[MAIN] Fichier de sortie: {output_path}")
        
        # Test d'écriture
        try:
            with open(output_path, "w", encoding="utf-8") as test_file:
                test_file.write("# Test d'écriture\n")
            print("[OK] [MAIN] Test d'écriture réussi")
        except Exception as e:
            raise PermissionError(f"Impossible d'écrire: {e}")
        
        # 9. BOUCLE PRINCIPALE
        print(f" [MAIN] Étape 9: DÉBUT de la boucle principale ({len(pages)} pages)")
        print("="*60)
        
        successful_pages = 0
        failed_pages = 0
        
        with open(output_path, "w", encoding="utf-8") as md_file:
            # En-tête du fichier
            md_file.write("# Analyse des liens entre éléments\n\n")
            md_file.write(f"- Document: {document_path.name}\n")
            md_file.write(f"- Pages à traiter: {len(pages)}\n")
            md_file.write(f"- Date: {json.dumps([], default=str)}\n\n")
            md_file.flush()  # Forcer l'écriture
            print("[OK] [MAIN] En-tête écrit dans le fichier")
            
            for idx, (page_content, page_ctx, ordered_objet_content) in enumerate(zip(pages, pages_data, ordered_objet)):
                print(f"\n[MAIN] === PAGE {idx+1}/{len(pages)} ===")
                
                try:
                    # Récupération des données de contexte
                    page_summary = page_ctx.get("pageSummary", "")
                    global_summary = page_ctx.get("updatedGlobalSummary", "")
                    
                    if idx == 0:
                        last_page_summary = page_summary
                    else:
                        last_page_summary = pages_data[idx-1].get("pageSummary", "")
                    
                    print(f" [MAIN] Page {idx+1} - Résumé: {len(page_summary)} caractères")
                    print(f" [MAIN] Page {idx+1} - Objets: {len(str(ordered_objet_content))} caractères")
                    
                    # Vérifier que les objets ne sont pas vides
                    if not ordered_objet_content or not str(ordered_objet_content).strip():
                        print(f"[WARNING] [MAIN] Page {idx+1}: Objets vides ou invalides")
                        print(f" [MAIN] Page {idx+1}: Type objets = {type(ordered_objet_content)}")
                        print(f" [MAIN] Page {idx+1}: Contenu objets = {repr(ordered_objet_content)}")
                    
                    # Créer le prompt pour l'analyse des liens
                    print(f" [MAIN] Page {idx+1}: Création du prompt...")
                    prompt = prompt_links.format(
                        globalSummary=global_summary,
                        lastPageSummary=last_page_summary,
                        PageSummary=page_summary,
                        but_principal=main_goal,
                        objects=ordered_objet_content
                    )
                    
                    print(f" [MAIN] Page {idx+1}: Prompt créé ({len(prompt)} caractères)")
                    
                    # Appeler l'API LLM
                    print(f" [MAIN] Page {idx+1}: Appel API...")
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
                        timeout=60  # Timeout de 60 secondes
                    )
                    
                    print(f" [MAIN] Page {idx+1}: Réponse API reçue (status: {response.status_code})")
                    response.raise_for_status()
                    
                    response_data = response.json()
                    result = response_data['choices'][0]['message']['content']
                    
                    print(f"[OK] [MAIN] Page {idx+1}: Résultat obtenu ({len(result)} caractères)")
                    print(f" [MAIN] Page {idx+1}: Aperçu = {result[:100]}...")
                    
                    # Écrire le résultat
                    md_file.write(f"\n---\n\n# Page {idx+1}\n\n{result}\n")
                    md_file.flush()  # Forcer l'écriture immédiate
                    
                    print(f" [MAIN] Page {idx+1}: Résultat écrit dans le fichier")
                    successful_pages += 1
                    
                except requests.RequestException as e:
                    error_msg = f"Erreur API pour la page {idx+1}: {e}"
                    print(f"[ERROR] [MAIN] {error_msg}")
                    md_file.write(f"\n---\n\n# Page {idx+1}\n\n**ERREUR API:** {error_msg}\n")
                    md_file.flush()
                    failed_pages += 1
                    
                except KeyError as e:
                    error_msg = f"Erreur de format de réponse pour la page {idx+1}: {e}"
                    print(f"[ERROR] [MAIN] {error_msg}")
                    md_file.write(f"\n---\n\n# Page {idx+1}\n\n**ERREUR FORMAT:** {error_msg}\n")
                    md_file.flush()
                    failed_pages += 1
                    
                except Exception as e:
                    error_msg = f"Erreur inattendue pour la page {idx+1}: {e}"
                    print(f"[ERROR] [MAIN] {error_msg}")
                    print(f"🔍 [MAIN] Type d'erreur: {type(e).__name__}")
                    import traceback
                    print(f" [MAIN] Traceback: {traceback.format_exc()}")
                    md_file.write(f"\n---\n\n# Page {idx+1}\n\n**ERREUR:** {error_msg}\n")
                    md_file.flush()
                    failed_pages += 1
        
        print("\n" + "="*60)
        print(" [MAIN] FIN DE LA BOUCLE PRINCIPALE")
        print(f" [MAIN] Résultats finaux:")
        print(f"   [OK] Pages réussies: {successful_pages}")
        print(f"   [ERROR] Pages échouées: {failed_pages}")
        print(f"   📁 Fichier créé: {output_path}")
        print(f"    Taille du fichier: {output_path.stat().st_size} octets")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f" [MAIN] ERREUR FATALE dans main(): {e}")
        print(f" [MAIN] Type d'erreur: {type(e).__name__}")
        import traceback
        print(f" [MAIN] Traceback complet:")
        print(traceback.format_exc())
        return False

def check_dependencies():
    """Vérifier que tous les fichiers nécessaires existent"""
    print("🔍 [CHECK] Vérification des dépendances...")
    
    required_files = [
        PRETRAITEMENT_DIR / "DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md",
        ANALYSE_DIR / "resultats_context_llm.json",
        ANALYSE_DIR / "reponse.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path))
            print(f"[ERROR] [CHECK] Manquant: {file_path}")
        else:
            print(f"[OK] [CHECK] Trouvé: {file_path.name}")
    
    if missing_files:
        print(f"[ERROR] [CHECK] {len(missing_files)} fichier(s) manquant(s)")
        return False
    
    print("[OK] [CHECK] Tous les fichiers requis sont présents")
    return True

def check_file_integrity():
    """Vérifier l'intégrité des fichiers nécessaires"""
    print("🔍 [INTEGRITY] Vérification de l'intégrité des fichiers...")
    
    # Vérifier que le fichier reponse.md contient des données
    reponse_path = ANALYSE_DIR / "reponse.md"
    if reponse_path.exists():
        with open(reponse_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print("[ERROR] [INTEGRITY] reponse.md est vide")
                return False
            print(f"[OK] [INTEGRITY] reponse.md: {len(content)} caractères")
    
    # Vérifier le JSON
    json_path = ANALYSE_DIR / "resultats_context_llm.json"
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"[OK] [INTEGRITY] JSON valide: {len(data)} pages")
        except json.JSONDecodeError as e:
            print(f"[ERROR] [INTEGRITY] Erreur JSON: {e}")
            return False
    
    print("[OK] [INTEGRITY] Tous les fichiers sont intègres")
    return True

if __name__ == "__main__":
    print("🔗 ANALYSE DES LIENS - VERSION DEBUG COMPLÈTE")
    print("="*60)
    print(f"📁 Répertoire d'analyse: {ANALYSE_DIR}")
    
    # Étape 1: Vérification des dépendances
    if check_dependencies():
        # Étape 2: Vérification de l'intégrité
        if check_file_integrity():
            print("[OK] Toutes les vérifications passées")
            print("🚀 LANCEMENT DE LA FONCTION MAIN()...")
            
            # Exécution de main() avec capture du résultat
            success = main()
            
            if success:
                print("🎉 SUCCÈS: Analyse terminée avec succès!")
            else:
                print("💥 ÉCHEC: Erreur durant l'analyse")
        else:
            print("[ERROR] Problème d'intégrité des fichiers")
    else:
        print("[ERROR] Fichiers manquants")
    
    print("="*60)