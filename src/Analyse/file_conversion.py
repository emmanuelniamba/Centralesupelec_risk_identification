
from typing import List, Tuple
import os
import sys
import requests
import json
import re
from collections import OrderedDict
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



def extract(content: str) -> dict[int, str]:
    """
    Retourne un dict {num_page: contenu} à partir d'un markdown
    contenant des en-têtes 'Page N :' ou '# Page N'.
    """
    # En-tête de page en début de ligne, avec variantes:
    # - lignes '---' possibles juste avant
    # - '#' optionnel
    # - ':' optionnels
    header_re = re.compile(
        r'^(?:-{3,}\s*\n)?\s*#?\s*Page\s+(\d+)\s*:?\s*$',
        re.IGNORECASE | re.MULTILINE
    )

    pages = OrderedDict()
    matches = list(header_re.finditer(content))
    if not matches:
        print("Aucun en-tête 'Page N' trouvé. Vérifie le format des titres.")
        return pages

    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(content)
        pages[int(m.group(1))] = content[start:end].strip()
    return pages


import re

def extract_page(content):
    # Define the regex pattern to match pages and their content
    pattern = r"Page (\d+) :(.+?)(?=Page \d+ :|$)"
    
    # Use re.findall to extract all matches
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Create a dictionary to store the page content
    pages = {int(page): text.strip() for page, text in matches}
    
    return pages


