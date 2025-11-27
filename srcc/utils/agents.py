import os
import json
import requests
import re
import time
import concurrent.futures
import streamlit as st
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# ==========================================
# 1. MODÈLES DE DONNÉES
# ==========================================
class PageAnalysisResult(BaseModel):
    sectionTitle: str = Field(..., description="Titre")
    isContinuation: bool = Field(..., description="Suite ?")
    pageSummary: str = Field(..., description="Résumé")
    updatedGlobalSummary: str = Field(default="", description="Contexte Global")

class RiskPageResult(BaseModel):
    vulnerabilities: List[Dict[str, str]] = Field(default_factory=list)
    threats: List[Dict[str, str]] = Field(default_factory=list)

# ==========================================
# 2. AGENT DE BASE
# ==========================================
class BaseAgent:
    def __init__(self):
        self.api_key = os.getenv("llm_key") or os.getenv("LLAMA_CLOUD_API_KEY") or st.session_state.get('api_key_llm')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # --- UTILISATION DE QWEN (Le meilleur gratuit actuel) ---
        # Si tu tiens à ton ancien modèle, remets son nom ici, mais celui-ci est très fiable.
        self.model = "meta-llama/llama-3.3-70b-instruct:free" 

    def _clean_json(self, text: str) -> str:
        """Tentative de sauver le JSON au milieu du texte."""
        if not text: return "{}"
        try:
            # Nettoyage DeepSeek/Qwen thinking
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```', '', text)
            
            # Chercher le JSON entre accolades
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1: 
                return text[start:end]
            return text
        except: 
            return "{}"

    def _call_llm(self, messages: list, temperature: float) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://risk-assistant.app",
            "X-Title": "Risk Assistant"
        }
        
        payload = {
            "model": self.model,
            "temperature": temperature,
            "messages": messages
        }

        for attempt in range(3):
            try:
                response = requests.post(self.base_url, headers=headers, data=json.dumps(payload), timeout=90)
                if response.status_code == 404:
                    print(f"❌ ERREUR 404: Le modèle {self.model} n'existe pas. Change le nom dans BaseAgent.")
                    break
                if response.status_code == 429:
                    time.sleep(2)
                    continue
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt == 2: print(f"API Error: {e}")
                time.sleep(1)
        return {}

# ==========================================
# 3. AGENT DE RÉSUMÉ
# ==========================================
class SummarizerAgent(BaseAgent):
    def analyze_page(self, content: str, prev_summary: str, global_summary: str, last_section: str, 
                     system_prompt: str, temperature: float) -> Dict:
        
        user_content = f"""
        PRECEDENT: {last_section}
        CONTEXTE GLOBAL: {global_summary}
        PAGE COURANTE: {content[:5000]}
        
        INSTRUCTION: Renvoie un JSON strict avec les clés : sectionTitle, isContinuation, pageSummary, updatedGlobalSummary.
        """
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_content}]

        try:
            res = self._call_llm(messages, temperature)
            if 'choices' in res:
                raw = res['choices'][0]['message']['content']
                return PageAnalysisResult(**json.loads(self._clean_json(raw))).model_dump()
        except Exception as e:
            print(f"⚠️ Erreur Résumé: {e}")
        
        return PageAnalysisResult(sectionTitle="...", isContinuation=False, pageSummary="...", updatedGlobalSummary=global_summary).model_dump()

    def process_document(self, pages_data: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        results = []
        last_p, global_s, last_s = "", "", ""
        total = len(pages_data)
        
        for i, page in enumerate(pages_data):
            an = self.analyze_page(page['content'], last_p, global_s, last_s, system_prompt, temperature)
            last_p = an.get('pageSummary', '')
            global_s = an.get('updatedGlobalSummary', '')
            last_s = an.get('sectionTitle', '')
            results.append({"page": page['page'], "original_content": page['content'], **an})
            if progress_callback: progress_callback(int((i+1)/total*100))
        return results

# ==========================================
# 4. AGENT DE VULNÉRABILITÉ (LE CŒUR DU PROBLÈME)
# ==========================================
class VulnerabilityAgent(BaseAgent):
    
    def _analyze_single_page(self, args):
        data, prev_summary, prompt_template, temp = args
        
        # 1. Construction du prompt EXACTEMENT comme ton script
        try:
            formatted_prompt = prompt_template.format(
                globalSummary=data.get('updatedGlobalSummary', ''),
                lastPageSummary=prev_summary,
                PageSummary=data.get('pageSummary', ''),
                pageContent=data['original_content'][:4000]
            )
        except:
            formatted_prompt = f"Analyse: {data.get('pageSummary')}"

        # 2. On ajoute l'instruction JSON (Obligatoire pour l'interface Streamlit)
        json_instruction = """
        
        IMPORTANT : Tu dois répondre UNIQUEMENT en JSON valide.
        Format :
        {
            "vulnerabilities": [{"element": "...", "justification": "..."}],
            "threats": [{"element": "...", "threat": "...", "consequence": "..."}]
        }
        """
        
        final_prompt = formatted_prompt + json_instruction
        messages = [{"role": "user", "content": final_prompt}]
        
        raw_content = ""
        
        try:
            # Appel API
            res = self._call_llm(messages, temperature=0.3)
            
            if 'choices' in res:
                # 3. ON RÉCUPÈRE LE TEXTE BRUT
                raw_content = res['choices'][0]['message']['content']
                
                # --- DEBUG : AFFICHE LA RÉPONSE DANS TON TERMINAL ---
                print(f"\n--- RÉPONSE BRUTE PAGE {data.get('page')} ---\n{raw_content[:200]}...\n-----------------------------------")
                
                # 4. TENTATIVE DE PARSING JSON
                cleaned_json = self._clean_json(raw_content)
                parsed = json.loads(cleaned_json)
                
                # Vérification des clés
                if "vulnerabilities" not in parsed: parsed["vulnerabilities"] = []
                if "threats" not in parsed: parsed["threats"] = []

                # Si vide mais JSON valide
                if not parsed["vulnerabilities"] and not parsed["threats"]:
                    parsed["vulnerabilities"].append({"element": "RAS (Format OK)", "justification": "Pas de risque détecté."})

                return {
                    "page": data['page'],
                    "sectionTitle": data['sectionTitle'],
                    **parsed
                }

        except Exception as e:
            # 5. --- SAUVETAGE EN CAS D'ÉCHEC DU JSON ---
            # Si le modèle a répondu du texte (comme dans ton script) mais que le JSON a planté,
            # on affiche quand même le texte dans l'interface !
            
            print(f"❌ ÉCHEC JSON PAGE {data.get('page')} : {e}")
            
            # On prend les 500 premiers caractères de la réponse brute pour l'afficher
            preview_text = raw_content if raw_content else "Pas de réponse reçue."
            
            return {
                "page": data['page'],
                "sectionTitle": "SORTIE BRUTE (NON-JSON)",
                "vulnerabilities": [{
                    "element": "AFFICHAGE DU TEXTE BRUT",
                    "justification": f"Le modèle n'a pas renvoyé de JSON valide. Voici sa réponse :\n\n{preview_text}"
                }],
                "threats": []
            }
            
        return {"page": data['page'], "sectionTitle": "...", "vulnerabilities": [], "threats": []}

    def process_risks(self, context_results: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        results = []
        total = len(context_results)
        tasks = []
        
        for idx, page_ctx in enumerate(context_results):
            if idx == 0:
                last_page_summary = page_ctx.get("pageSummary", "")
            else:
                last_page_summary = context_results[idx-1].get("pageSummary", "")
            
            tasks.append((page_ctx, last_page_summary, system_prompt, temperature))
        
        # On peut monter les workers si on utilise un modèle Qwen standard
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self._analyze_single_page, t) for t in tasks]
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                completed += 1
                if progress_callback: progress_callback(int(completed/total*100))
        
        results.sort(key=lambda x: x['page'])
        return results