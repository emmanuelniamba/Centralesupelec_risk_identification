import os
import json
import requests
import re
import time
import streamlit as st
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# ==========================================
# 1. MODÈLES PYDANTIC
# ==========================================
class PageAnalysisResult(BaseModel):
    sectionTitle: str = Field(..., description="Titre court de la section")
    isContinuation: bool = Field(..., description="Si c'est la suite de la page précédente")
    pageSummary: str = Field(..., description="Résumé concis de la page")
    updatedGlobalSummary: str = Field(..., description="Résumé global mis à jour")

class VulnerableElement(BaseModel):
    element: str = Field(..., description="Nom de l'élément vulnérable")
    justification: str = Field(..., description="Citation ou explication de la vulnérabilité")

class ThreatAssociation(BaseModel):
    element: str = Field(..., description="L'élément vulnérable concerné")
    threat: str = Field(..., description="La menace identifiée")
    consequence: str = Field(..., description="Les conséquences possibles")

class RiskPageResult(BaseModel):
    vulnerabilities: List[VulnerableElement] = Field(default_factory=list)
    threats: List[ThreatAssociation] = Field(default_factory=list)

# ==========================================
# 2. CLASSE PARENTE (BASE AGENT)
# ==========================================
class BaseAgent:
    def __init__(self):
        self.api_key = os.getenv("llm_key") or os.getenv("LLAMA_CLOUD_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        # Modèle gratuit Google (Rapide et efficace)
        self.model = "google/gemini-2.0-flash-lite-preview-02-05:free"
        self.last_request_time = 0 

    def _clean_json(self, text: str) -> str:
        """Nettoie la réponse pour extraire le JSON pur."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                return text[start:end]
            return text
        except:
            return text

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
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        max_retries = 5
        
        for attempt in range(max_retries):
            try:
                # Délai minimum entre requêtes pour éviter le 429
                elapsed = time.time() - self.last_request_time
                if elapsed < 2.0:
                    time.sleep(2.0 - elapsed)
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=45
                )
                
                self.last_request_time = time.time()
                
                if response.status_code == 429:
                    wait_time = min(60, 5 * (2 ** attempt))
                    print(f"⚠️ Rate Limit. Pause de {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()

            except Exception as e:
                if attempt == max_retries - 1:
                    st.error(f"❌ Erreur API : {str(e)}")
                    raise e
                time.sleep(2)
        
        return {}

# ==========================================
# 3. SUMMARIZER AGENT
# ==========================================
class SummarizerAgent(BaseAgent):
    def analyze_page(self, content: str, prev_summary: str, global_summary: str, last_section: str, 
                     system_prompt: str, temperature: float) -> Dict:
        
        user_content = f"""
        CONTEXTE PRÉCÉDENT:
        - Titre Section Précédente: "{last_section}"
        - Résumé Page Précédente: "{prev_summary}"
        - Résumé Global Actuel: "{global_summary}"
        
        CONTENU PAGE ACTUELLE:
        {content[:4000]}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        for attempt in range(2):
            try:
                response = self._call_llm(messages, temperature)
                if 'choices' in response:
                    content_str = response['choices'][0]['message']['content']
                    clean_json = self._clean_json(content_str)
                    json_data = json.loads(clean_json)
                    return PageAnalysisResult(**json_data).model_dump()
            except Exception as e:
                print(f"Summarizer JSON Error: {e}")
                continue
        
        # Fallback
        return PageAnalysisResult(
            sectionTitle="Erreur", isContinuation=False, 
            pageSummary="Erreur analyse.", updatedGlobalSummary=global_summary
        ).model_dump()

    def process_document(self, pages_data: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        results = []
        global_summary = ""
        last_page_summary = ""
        last_section = ""
        total = len(pages_data)
        
        for i, page in enumerate(pages_data):
            try:
                # Utilisation de page['content'] (et non page_num)
                analysis = self.analyze_page(
                    page['content'], last_page_summary, global_summary, last_section,
                    system_prompt, temperature
                )
                
                last_page_summary = analysis['pageSummary']
                global_summary = analysis['updatedGlobalSummary']
                last_section = analysis['sectionTitle']
                
                # CORRECTION CLÉ : On utilise page['page'] et on aplatit le résultat
                results.append({
                    "page": page['page'],  # C'était ici l'erreur 'page_num'
                    "original_content": page['content'],
                    **analysis
                })
                
                if progress_callback:
                    progress_callback(int((i + 1) / total * 100))
                    
            except Exception as e:
                st.warning(f"⚠️ Erreur page {page.get('page', '?')} : {str(e)}")
                continue
        
        return results

# ==========================================
# 4. VULNERABILITY AGENT
# ==========================================
class VulnerabilityAgent(BaseAgent):
    def analyze_risk(self, page_content: str, context_data: Dict, system_prompt: str, temperature: float) -> Dict:
        
        user_content = f"""
        ANALYSE RISQUE PAGE {context_data.get('page', '?')}
        CONTEXTE: {context_data.get('sectionTitle')}
        RÉSUMÉ: {context_data.get('pageSummary')}
        
        TEXTE:
        {page_content[:4000]}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        for attempt in range(2):
            try:
                response = self._call_llm(messages, temperature)
                if 'choices' in response:
                    content_str = response['choices'][0]['message']['content']
                    clean_json = self._clean_json(content_str)
                    json_data = json.loads(clean_json)
                    return RiskPageResult(**json_data).model_dump()
            except Exception as e:
                print(f"Risk JSON Error: {e}")
                continue
                
        return RiskPageResult().model_dump()

    def process_risks(self, context_results: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        results = []
        total = len(context_results)
        
        for i, data in enumerate(context_results):
            risk_analysis = self.analyze_risk(
                data['original_content'], data, system_prompt, temperature
            )
            
            results.append({
                "page": data['page'],
                "sectionTitle": data['sectionTitle'],
                **risk_analysis
            })
            
            if progress_callback:
                progress_callback(int((i + 1) / total * 100))
                
        return results