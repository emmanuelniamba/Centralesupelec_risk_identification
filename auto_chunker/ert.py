import re
from collections import OrderedDict

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


with open(r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\auto_chunker\reponse.md", encoding="utf-8") as f:
    objet_data = f.read()
objet= extract(objet_data)
page_numbers = sorted(objet.keys())
ordered_objet = [objet[page] for page in page_numbers]
print(ordered_objet)