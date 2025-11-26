import os
import json
import requests
import re
import time
import concurrent.futures
import streamlit as st
from typing import List, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# ==========================================
# 1. MODÈLES
# ==========================================
class PageAnalysisResult(BaseModel):
    sectionTitle: str = Field(..., description="Titre court")
    isContinuation: bool = Field(..., description="Si suite page précédente")
    pageSummary: str = Field(..., description="Résumé page")
    updatedGlobalSummary: str = Field(..., description="Résumé global")

class VulnerableElement(BaseModel):
    element: str = Field(..., description="Nom")
    justification: str = Field(..., description="Justification")

class ThreatAssociation(BaseModel):
    element: str = Field(..., description="Élément")
    threat: str = Field(..., description="Menace")
    consequence: str = Field(..., description="Conséquence")

class RiskPageResult(BaseModel):
    vulnerabilities: List[VulnerableElement] = Field(default_factory=list)
    threats: List[ThreatAssociation] = Field(default_factory=list)

# ==========================================
# 2. BASE AGENT (Optimisé)
# ==========================================
class BaseAgent:
    def __init__(self):
        self.api_key = os.getenv("llm_key") or os.getenv("LLAMA_CLOUD_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Pour la vitesse, GPT-4o-mini est le roi (si payant). 
        # En gratuit, Gemini Flash est le moins lent.
        self.model = "deepseek/deepseek-r1-0528" 
        # Si tu veux gratuit : "google/gemini-2.0-flash-lite-preview-02-05:free"

    def _clean_json(self, text: str) -> str:
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1: return text[start:end]
            return text
        except: return text

    def _call_llm(self, messages: list, temperature: float) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://risk.app",
            "X-Title": "Risk Assistant"
        }
        payload = {
            "model": self.model,
            "temperature": temperature,
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        # Retry plus agressif mais sans longue attente
        for attempt in range(3):
            try:
                response = requests.post(self.base_url, headers=headers, data=json.dumps(payload), timeout=30)
                if response.status_code == 429:
                    time.sleep(2) # Pause courte et on réessaie
                    continue
                response.raise_for_status()
                return response.json()
            except Exception:
                if attempt == 2: return {} # Echec silencieux pour ne pas bloquer le thread
                time.sleep(1)
        return {}

# ==========================================
# 3. SUMMARIZER (Séquentiel Obligatoire)
# ==========================================
class SummarizerAgent(BaseAgent):
    def analyze_page(self, content: str, prev_summary: str, global_summary: str, last_section: str, sys_prompt: str, temp: float) -> Dict:
        user_content = f"""
        PRECEDENT: {last_section} | {prev_summary} | {global_summary}
        PAGE: {content[:3500]}
        """
        msg = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_content}]
        
        res = self._call_llm(msg, temp)
        if 'choices' in res:
            try:
                return PageAnalysisResult(**json.loads(self._clean_json(res['choices'][0]['message']['content']))).model_dump()
            except: pass
        
        return PageAnalysisResult(sectionTitle="...", isContinuation=False, pageSummary="...", updatedGlobalSummary=global_summary).model_dump()

    def process_document(self, pages_data: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        # Le contexte DOIT être séquentiel (page 1 -> page 2), on ne peut pas paralléliser
        results = []
        last_sum, global_sum, last_sec = "", "", ""
        total = len(pages_data)
        
        for i, page in enumerate(pages_data):
            # J'ai enlevé le time.sleep() pour aller le plus vite possible
            analysis = self.analyze_page(page['content'], last_sum, global_sum, last_sec, system_prompt, temperature)
            
            last_sum = analysis['pageSummary']
            global_sum = analysis['updatedGlobalSummary']
            last_sec = analysis['sectionTitle']
            
            results.append({"page": page['page'], "original_content": page['content'], **analysis})
            if progress_callback: progress_callback(int((i+1)/total*100))
            
        return results

# ==========================================
# 4. VULNERABILITY AGENT (PARALLELE / TURBO)
# ==========================================
class VulnerabilityAgent(BaseAgent):
    def analyze_risk_wrapper(self, args):
        # Fonction helper pour le threading
        data, sys_prompt, temp = args
        user_content = f"CONTEXTE: {data.get('sectionTitle')} - {data.get('pageSummary')}\nTEXTE: {data['original_content'][:3500]}"
        msg = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_content}]
        
        res = self._call_llm(msg, temp)
        if 'choices' in res:
            try:
                return {
                    "page": data['page'], 
                    "sectionTitle": data['sectionTitle'], 
                    **RiskPageResult(**json.loads(self._clean_json(res['choices'][0]['message']['content']))).model_dump()
                }
            except: pass
        return {"page": data['page'], "sectionTitle": data['sectionTitle'], "vulnerabilities": [], "threats": []}

    def process_risks(self, context_results: List[Dict], system_prompt: str, temperature: float, progress_callback=None) -> List[Dict]:
        # ICI C'EST LA VITESSE : On lance jusqu'à 5 pages EN MÊME TEMPS
        results = []
        total = len(context_results)
        completed = 0
        
        # Préparation des arguments pour chaque page
        tasks = [(data, system_prompt, temperature) for data in context_results]
        
        # Exécution Parallèle (Multi-Threading)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # On lance les scans
            future_to_page = {executor.submit(self.analyze_risk_wrapper, task): task for task in tasks}
            
            for future in concurrent.futures.as_completed(future_to_page):
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    print(f"Erreur thread: {e}")
                
                completed += 1
                if progress_callback: progress_callback(int(completed/total*100))
        
        # On remet les résultats dans l'ordre des pages (1, 2, 3...) car le parallèle peut finir dans le désordre
        results.sort(key=lambda x: x['page'])
        return results