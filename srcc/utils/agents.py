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
# 2. CLASSE PARENTE (BASE AGENT - CONFIG PAYANTE)
# ==========================================
class BaseAgent:
    def __init__(self):
        self.api_key = os.getenv("llm_key") or os.getenv("LLAMA_CLOUD_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "google/gemini-2.0-flash-exp:free"
        self.last_request_time = 0  # ✅ Suivi du dernier appel

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
                # ✅ FORCE UN DÉLAI MINIMUM entre les requêtes
                elapsed = time.time() - self.last_request_time
                if elapsed < 2.0:  # Minimum 2 secondes entre chaque appel
                    time.sleep(2.0 - elapsed)
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=30
                )
                
                self.last_request_time = time.time()  # ✅ Mise à jour
                
                if response.status_code == 429:
                    # ✅ Attente exponentielle AGRESSIVE
                    wait_time = min(60, 5 * (2 ** attempt))  # 5s, 10s, 20s, 40s, 60s max
                    print(f"⚠️ Rate Limit (429). Tentative {attempt+1}/{max_retries}. Pause de {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429 and attempt < max_retries - 1:
                    continue  # ✅ Retry sur 429
                if attempt == max_retries - 1:
                    st.error(f"❌ Erreur API après {max_retries} tentatives : {str(e)}")
                    raise e
                time.sleep(2)
            except Exception as e:
                if attempt == max_retries - 1:
                    st.error(f"❌ Erreur technique : {str(e)}")
                    raise e
                time.sleep(2)
        
        return {}


class SummarizerAgent(BaseAgent):
    def process_document(self, pages_data: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        results = []
        global_summary = ""
        last_page_summary = ""
        last_section = ""
        total = len(pages_data)
        
        for i, page in enumerate(pages_data):
            # ✅ PLUS BESOIN de sleep ici, c'est géré dans _call_llm
            
            try:
                analysis = self.analyze_page(
                    page['content'], last_page_summary, global_summary, last_section,
                    system_prompt, temperature
                )
                last_page_summary = analysis['pageSummary']
                global_summary = analysis['updatedGlobalSummary']
                last_section = analysis['sectionTitle']
                
                results.append({
                    "page_num": page['page_num'],
                    "analysis": analysis
                })
                
                if progress_callback:
                    progress_callback(i + 1, total)
                    
            except Exception as e:
                st.warning(f"⚠️ Page {page['page_num']} ignorée : {str(e)}")
                continue
        
        return results