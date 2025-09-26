# utils/Summarizer.py
import os
import requests
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from typing import List, Dict, Any, Optional, Tuple
import re

# Charger les variables d'environnement
load_dotenv()

# Configuration
api_key = os.getenv("llm_key")

# Template de prompt optimisé
PROMPT_TEMPLATE = """Vous êtes un assistant spécialisé dans la gestion de projet.   

Vous traitez un document **page par page**. À chaque itération, vous recevrez :

globalSummary: "{globalSummary}" 
lastPageSummary: "{lastPageSummary}" 
lastSectionTitle: "{lastSectionTitle}" 
pageContent: "{pageContent}" 
isContinuation: {isContinuation}  

Votre mission : 
1. **Identifier** le titre ou thème principal de la page N → sectionTitle (un ou deux mots).   
2. Déterminer si cette page **continue** la même section qu'à la page N‑1 → isContinuation.   
3. Générer un **pageSummary** (5–9 phrases) qui mentionne:    
   - le **titre de section**,    
   - les points clés précis,    
   - un repère de continuité si `isContinuation` est `true`.   
4. Mettre à jour le **globalSummary** sans répéter l'existant.   
5. **IMPORTANT** : Ta réponse doit être **uniquement un objet JSON valide**.

Format de réponse EXACT :
```json
{{   
    "sectionTitle": "<Titre de la page N>",   
    "isContinuation": <true|false>,   
    "pageSummary": "<Résumé de la page N>",   
    "updatedGlobalSummary": "<Résumé global mis à jour incluant N>" 
}}
```"""

class SummarizerAgent:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise l'agent Summarizer
        
        Args:
            api_key: Clé API (optionnelle, utilisera la variable d'environnement par défaut)
        """
        self.api_key = api_key or os.getenv("llm_key")
        self.prompt_template = PROMPT_TEMPLATE
        self.model = "deepseek/deepseek-chat"  # Modèle plus stable
        self.temperature = 0.1
        self.timeout = 45  # Timeout augmenté pour éviter les erreurs
        
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extrait et parse le JSON depuis la réponse, même si mal formaté
        
        Args:
            response_text: Texte de la réponse de l'API
            
        Returns:
            Dict contenant les données parsées
        """
        # Nettoyer la réponse
        text = response_text.strip()
        
        # Essayer d'extraire le JSON de différentes manières
        json_str = text
        
        # Si entouré de ```json
        if "```json" in text:
            match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if match:
                json_str = match.group(1)
        # Si entouré de ```
        elif "```" in text:
            match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
            if match:
                json_str = match.group(1)
        
        # Nettoyer les caractères indésirables
        json_str = json_str.strip()
        
        # Parser le JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Tentative de réparation basique
            # Remplacer les retours à la ligne dans les valeurs
            json_str = re.sub(r':\s*"([^"]*)\n([^"]*)"', r': "\1 \2"', json_str)
            # Essayer à nouveau
            return json.loads(json_str)
        
    def process_pages(
        self, 
        pages: List[str], 
        progress_callback: Optional[callable] = None, 
        status_callback: Optional[callable] = None
    ) -> Tuple[List[Dict], int, int]:
        """
        Traite une liste de pages avec le Summarizer Agent
        
        Args:
            pages: Liste des pages extraites
            progress_callback: Fonction pour mettre à jour la barre de progression
            status_callback: Fonction pour afficher le statut
            
        Returns:
            tuple: (pages_summaries, success_count, error_count)
        """
        if not self.api_key:
            raise ValueError("Clé API non trouvée. Vérifiez votre fichier .env avec llm_key")
        
        # Initialiser les variables pour le suivi
        global_summary = ""
        last_page_summary = ""
        last_section_title = ""
        is_continuation = False
        
        pages_summaries = []
        successful_pages = 0
        failed_pages = 0
        total_pages = len(pages)
        
        for idx, page_content in enumerate(pages):
            page_num = idx + 1
            
            # Mise à jour du statut
            if status_callback:
                status_callback(f"📄 Traitement page {page_num}/{total_pages}...")
            
            if progress_callback:
                progress = int((idx / total_pages) * 100)
                progress_callback(progress)
            
            try:
                # Limiter la taille du contenu pour éviter les timeouts
                truncated_content = page_content[:3000] if len(page_content) > 3000 else page_content
                
                # Créer le prompt
                prompt = self.prompt_template.format(
                    globalSummary=global_summary[:1000],  # Limiter aussi le global summary
                    lastPageSummary=last_page_summary,
                    lastSectionTitle=last_section_title,
                    pageContent=truncated_content,
                    isContinuation=str(is_continuation).lower()
                )
                
                # Appeler l'API LLM avec retry
                for attempt in range(2):  # 2 tentatives
                    try:
                        response = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json",
                                "HTTP-Referer": "https://github.com/yourusername/yourproject",
                                "X-Title": "Risk Analysis Platform"
                            },
                            data=json.dumps({
                                "model": self.model,
                                "temperature": self.temperature,
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "Vous êtes un assistant expert en analyse de documents. Répondez UNIQUEMENT avec du JSON valide."
                                    },
                                    {
                                        "role": "user",
                                        "content": prompt
                                    }
                                ],
                                "max_tokens": 1000
                            }),
                            timeout=self.timeout
                        )
                        
                        if response.status_code == 200:
                            break
                        elif attempt == 0:  # Première tentative échouée
                            continue
                        else:
                            response.raise_for_status()
                            
                    except requests.Timeout:
                        if attempt == 0:
                            continue
                        raise
                
                response_json = response.json()
                result = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Parser la réponse JSON
                parsed_result = self._extract_json_from_response(result)
                
                # Extraire les données
                section_title = parsed_result.get("sectionTitle", "Section inconnue")
                page_summary = parsed_result.get("pageSummary", "Résumé non disponible")
                updated_global_summary = parsed_result.get("updatedGlobalSummary", global_summary)
                is_continuation = parsed_result.get("isContinuation", False)
                
                # Validation basique
                if not section_title or not page_summary:
                    raise ValueError("Données manquantes dans la réponse")
                
                # Mettre à jour les variables pour la prochaine itération
                last_page_summary = page_summary
                last_section_title = section_title
                global_summary = updated_global_summary
                
                # Ajouter à la liste des résultats
                pages_summaries.append({
                    "page": page_num,
                    "sectionTitle": section_title,
                    "pageSummary": page_summary,
                    "updatedGlobalSummary": updated_global_summary,
                    "isContinuation": is_continuation,
                    "originalContent": page_content,
                    "status": "success"
                })
                
                successful_pages += 1
                
            except (json.JSONDecodeError, ValueError) as e:
                # Erreur de parsing JSON
                error_msg = f"Erreur de format: {str(e)}"
                pages_summaries.append({
                    "page": page_num,
                    "error": error_msg,
                    "raw_content": result[:500] if 'result' in locals() else "N/A",
                    "originalContent": page_content,
                    "status": "error",
                    "sectionTitle": "Erreur",
                    "pageSummary": "Erreur lors du traitement de cette page",
                    "isContinuation": False
                })
                failed_pages += 1
                
            except requests.RequestException as e:
                # Erreur réseau/API
                error_msg = f"Erreur API: {str(e)}"
                pages_summaries.append({
                    "page": page_num,
                    "error": error_msg,
                    "originalContent": page_content,
                    "status": "error",
                    "sectionTitle": "Erreur réseau",
                    "pageSummary": "Impossible de contacter l'API",
                    "isContinuation": False
                })
                failed_pages += 1
                
            except Exception as e:
                # Erreur inattendue
                error_msg = f"Erreur inattendue: {str(e)}"
                pages_summaries.append({
                    "page": page_num,
                    "error": error_msg,
                    "originalContent": page_content,
                    "status": "error",
                    "sectionTitle": "Erreur",
                    "pageSummary": "Une erreur inattendue s'est produite",
                    "isContinuation": False
                })
                failed_pages += 1
        
        # Mise à jour finale
        if progress_callback:
            progress_callback(100)
        
        if status_callback:
            status_callback(f"✅ Traitement terminé: {successful_pages} succès, {failed_pages} erreurs")
        
        return pages_summaries, successful_pages, failed_pages
    
    def save_results(self, pages_summaries: List[Dict], output_path: Path) -> bool:
        """
        Sauvegarde les résultats du summarizer
        
        Args:
            pages_summaries: Liste des résumés de pages
            output_path: Chemin de sauvegarde
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarder en JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(pages_summaries, f, ensure_ascii=False, indent=2)
            
            # Sauvegarder aussi en Markdown pour lecture facile
            md_path = output_path.with_suffix('.md')
            with open(md_path, "w", encoding="utf-8") as f:
                f.write("# Résumés des Pages\n\n")
                
                for summary in pages_summaries:
                    f.write(f"## Page {summary['page']}\n\n")
                    
                    if summary.get('status') == 'error':
                        f.write(f"**❌ Erreur:** {summary.get('error', 'Erreur inconnue')}\n\n")
                    else:
                        f.write(f"**📑 Section:** {summary.get('sectionTitle', 'N/A')}\n\n")
                        f.write(f"**📝 Résumé:**\n{summary.get('pageSummary', 'N/A')}\n\n")
                        f.write(f"**🔗 Continuation:** {'Oui' if summary.get('isContinuation') else 'Non'}\n\n")
                        
                        if summary.get('updatedGlobalSummary'):
                            f.write(f"**🌐 Résumé global mis à jour:**\n")
                            f.write(f"{summary['updatedGlobalSummary'][:500]}...\n\n")
                    
                    f.write("---\n\n")
            
            return True
            
        except Exception as e:
            if st:
                st.error(f"Erreur lors de la sauvegarde : {e}")
            else:
                print(f"Erreur lors de la sauvegarde : {e}")
            return False
    
    def get_statistics(self, pages_summaries: List[Dict]) -> Dict[str, Any]:
        """
        Calcule des statistiques sur les résumés
        
        Args:
            pages_summaries: Liste des résumés
            
        Returns:
            Dict contenant les statistiques
        """
        total = len(pages_summaries)
        successes = sum(1 for p in pages_summaries if p.get('status') != 'error')
        errors = total - successes
        
        sections = {}
        for summary in pages_summaries:
            if summary.get('sectionTitle') and summary.get('status') != 'error':
                section = summary['sectionTitle']
                if section not in sections:
                    sections[section] = 0
                sections[section] += 1
        
        continuations = sum(1 for p in pages_summaries 
                          if p.get('isContinuation') and p.get('status') != 'error')
        
        return {
            'total_pages': total,
            'successful_pages': successes,
            'failed_pages': errors,
            'success_rate': (successes / total * 100) if total > 0 else 0,
            'unique_sections': len(sections),
            'sections': sections,
            'continuations': continuations,
            'new_sections': successes - continuations
        }