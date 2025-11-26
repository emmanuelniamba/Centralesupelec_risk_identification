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
        
        # --- CONFIGURATION DU MODÈLE ---
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # ICI C'EST IMPORTANT : On utilise un modèle PAYANT mais PAS CHER et TRÈS STABLE
        # GPT-4o-mini est excellent pour le JSON et coûte des poussières.
        self.model = "google/gemini-2.0-flash-exp:free" 

    def _clean_json(self, text: str) -> str:
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

        # --- RETRY LOGIC (INSISTANT) ---
        max_retries = 5 # On insiste jusqu'à 5 fois
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=30 # Timeout court pour retry vite
                )
                
                # Gestion Rate Limit (429)
                if response.status_code == 429:
                    wait_time = 2 * (attempt + 1) # Attente progressive : 2s, 4s, 6s...
                    print(f"⚠️ Rate Limit (429). Pause de {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()

            except Exception as e:
                if attempt == max_retries - 1:
                    # Si c'est la dernière tentative, on lève l'erreur pour l'afficher
                    st.error(f"Erreur API ({self.model}) : {str(e)}")
                    raise e
                time.sleep(1) # Petite pause avant retry technique
        
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

        # Tentative d'appel
        try:
            response = self._call_llm(messages, temperature)
            if 'choices' in response:
                content_str = response['choices'][0]['message']['content']
                clean_json = self._clean_json(content_str)
                json_data = json.loads(clean_json)
                return PageAnalysisResult(**json_data).model_dump()
        except Exception as e:
            print(f"Summarizer Error: {e}")
        
        # Fallback en cas d'erreur
        return PageAnalysisResult(
            sectionTitle="Erreur Analyse", isContinuation=False, 
            pageSummary="Impossible de traiter cette page (Erreur API).", 
            updatedGlobalSummary=global_summary
        ).model_dump()

    def process_document(self, pages_data: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        results = []
        global_summary = ""
        last_page_summary = ""
        last_section = ""
        total = len(pages_data)
        
        for i, page in enumerate(pages_data):
            # --- PAUSE DE SECURITE ---
            # Même avec un compte payant, on évite d'envoyer 50 requêtes en 1 seconde
            time.sleep(0.5) 
            
            analysis = self.analyze_page(
                page['content'], last_page_summary, global_summary, last_section,
                system_prompt, temperature
            )
            last_page_summary = analysis['pageSummary']