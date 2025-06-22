import os
from content_extraction import Content_Extractor

extractor = Content_Extractor()


chemin = r'C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\case studies with context\DO - NOTE TECHNIQUE BAT ZZ.pdf'  

if os.path.isdir(chemin):
    # Si c'est un dossier, traite tous les PDF du dossier
    for filename in os.listdir(chemin):
        if filename.lower().endswith('.pdf'):
            chemin_fichier = os.path.join(chemin, filename)
            print(f"Processing: {chemin_fichier}")
            extractor.save_extracted_data(
                file_path=chemin_fichier,
                output_text_path=f"{filename}_resultat.txt",
                output_markdown_path=f"{filename}_resultat.md",
                output_json_path=f"{filename}_resultat.json"
            )
elif os.path.isfile(chemin) and chemin.lower().endswith('.pdf'):
    # Si c'est un fichier PDF unique
    print(f"Processing: {chemin}")
    filename = os.path.basename(chemin)
    extractor.save_extracted_data(
        file_path=chemin,
        output_text_path=f"{filename}_resultat.txt",
        output_markdown_path=f"{filename}_resultat.md",
        output_json_path=f"{filename}_resultat.json"
    )
else:
    print("Le chemin spécifié n'est ni un dossier ni un fichier PDF valide.")