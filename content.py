import os
from content_extraction import Content_Extractor

extractor = Content_Extractor()

chemin = r'C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\case studies with context'

# Crée le dossier de sortie s'il n'existe pas
output_dir = "pretraitrement_1"
os.makedirs(output_dir, exist_ok=True)

if os.path.isdir(chemin):
    # Si c'est un dossier, traite tous les PDF du dossier
    for filename in os.listdir(chemin):
        if filename.lower().endswith('.pdf'):
            chemin_fichier = os.path.join(chemin, filename)
            if not os.path.isfile(chemin_fichier):
                print(f"Fichier introuvable, ignoré : {chemin_fichier}")
                continue
            print(f"Processing: {chemin_fichier}")
            output_markdown_path = os.path.join(output_dir, f"{filename}_resultat.md")
            extractor.save_extracted_data(
                file_path=chemin_fichier,
                output_markdown_path=output_markdown_path,
            )
elif os.path.isfile(chemin) and chemin.lower().endswith('.pdf'):
    # Si c'est un fichier PDF unique
    print(f"Processing: {chemin}")
    filename = os.path.basename(chemin)
    output_markdown_path = os.path.join(output_dir, f"{filename}_resultat.md")
    extractor.save_extracted_data(
        file_path=chemin,
        output_markdown_path=output_markdown_path,
    )
else:
    print("Le chemin spécifié n'est ni un dossier ni un fichier PDF valide.")