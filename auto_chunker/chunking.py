#autochunker 
#diviser le texte en unité plus petite:Phrases
import spacy
from typing import List, Tuple
import os
import sys
import requests
import json
from dotenv import load_dotenv
load_dotenv()
import re
api_key = os.getenv("llm_key")


           

def extract_pages(text: str) -> List[str]:
    """
    Extrait les pages en découpant sur chaque balise de fermeture </pageN>.
    Si aucune balise d'ouverture, on prend tout jusqu'à </pageN>.
    """
    # 1) Split sur la fermeture
    parts = re.split(r'</\s*page\s*\d+\s*>', text, flags=re.IGNORECASE)
    pages = []
    for part in parts:
        # 2) Supprime toute balise d'ouverture résiduelle
        page = re.sub(r'<\s*page\s*\d+\s*>', '', part, flags=re.IGNORECASE).strip()
        # 3) Garde si non vide
        if page:
            pages.append(page)
    return pages

# Exemple d'utilisation
if __name__ == "__main__":
    with open(r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\pretraitement2\0703-15 Project Charter for Tribal Trails.pdf_resultat.md", "r", encoding="utf-8") as f:
        document_text = f.read()
    pages = extract_pages(document_text)
    print(f"Nombre de pages extraites : {len(pages)}")
    for i, pg in enumerate(pages, 1):
        print(f"--- Page {i} (début) ---\n{pg[:200]}...\n")
        