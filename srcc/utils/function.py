# utils/fonctions.py
import os
import re
import tempfile
import streamlit as st
from pathlib import Path
import sys

# Ajouter le chemin vers le module content_extraction qui est dans le même dossier
sys.path.append(str(Path(__file__).parent))

try:
    from content_extraction import Content_Extractor
    LLAMAPARSE_AVAILABLE = True
except ImportError:
    LLAMAPARSE_AVAILABLE = False

# ========== CONFIGURATION ==========
PROCESSED_DIR = Path(__file__).parent.parent / "processed_documents"
PROCESSED_DIR.mkdir(exist_ok=True)

# ========== FONCTIONS UTILITAIRES LLAMAPARSE ==========

def extract_pages(text: str):
    """
    Extrait les pages en découpant sur chaque balise de fermeture </pageN>.
    Si aucune balise d'ouverture, on prend tout jusqu'à </pageN>.
    
    Args:
        text (str): Texte contenant les balises de pages
        
    Returns:
        list: Liste des contenus de pages extraites
    """
    # Split sur la fermeture
    parts = re.split(r'</\s*page\s*\d+\s*>', text, flags=re.IGNORECASE)
    pages = []
    
    for part in parts:
        # Supprime toute balise d'ouverture résiduelle
        page = re.sub(r'<\s*page\s*\d+\s*>', '', part, flags=re.IGNORECASE).strip()
        # Garde si non vide
        if page:
            pages.append(page)
    
    return pages

def save_uploaded_file(uploaded_file):
    """
    Sauvegarde le fichier uploadé temporairement.
    
    Args:
        uploaded_file: Fichier uploadé via Streamlit
        
    Returns:
        str: Chemin vers le fichier temporaire ou None si erreur
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde du fichier : {e}")
        return None

def process_with_llamaparse(file_path, output_name):
    """
    Traite le fichier avec LlamaParse et retourne le contenu.
    
    Args:
        file_path (str): Chemin vers le fichier à traiter
        output_name (str): Nom pour le fichier de sortie
        
    Returns:
        tuple: (texte_complet, chemin_fichier_sortie) ou None si erreur
    """
    try:
        if not LLAMAPARSE_AVAILABLE:
            st.error("LlamaParse n'est pas disponible. Vérifiez l'installation.")
            return None
            
        # Initialiser l'extracteur
        extractor = Content_Extractor()
        
        # Extraire le contenu
        documents = extractor.extract_content(file_path)
        
        if documents:
            # Joindre tout le texte
            full_text = '\n'.join([doc.text for doc in documents if hasattr(doc, 'text') and doc.text])
            
            # Sauvegarder le résultat
            output_path = PROCESSED_DIR / f"{output_name}_parsed.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            return full_text, output_path
        else:
            st.error("Aucun contenu extrait du document")
            return None
            
    except Exception as e:
        st.error(f"Erreur lors du traitement LlamaParse : {e}")
        return None

def clean_filename(filename):
    """
    Nettoie le nom de fichier pour éviter les caractères problématiques.
    
    Args:
        filename (str): Nom de fichier original
        
    Returns:
        str: Nom de fichier nettoyé
    """
    # Remplacer les caractères problématiques
    clean_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remplacer les points par des underscores sauf le dernier (extension)
    name_parts = clean_name.rsplit('.', 1)
    if len(name_parts) == 2:
        clean_name = name_parts[0].replace('.', '_') + '.' + name_parts[1]
    else:
        clean_name = clean_name.replace('.', '_')
    
    return clean_name

def format_file_size(size_bytes):
    """
    Formate la taille de fichier en unités lisibles.
    
    Args:
        size_bytes (int): Taille en bytes
        
    Returns:
        str: Taille formatée (ex: "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_file_type(filename, allowed_types=None):
    """
    Valide le type de fichier.
    
    Args:
        filename (str): Nom du fichier
        allowed_types (list): Liste des extensions autorisées
        
    Returns:
        bool: True si le type est autorisé
    """
    if allowed_types is None:
        allowed_types = ['.pdf', '.docx', '.txt', '.doc']
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_types

def get_file_info(uploaded_file):
    """
    Extrait les informations du fichier uploadé.
    
    Args:
        uploaded_file: Fichier uploadé via Streamlit
        
    Returns:
        dict: Dictionnaire avec les informations du fichier
    """
    return {
        "nom": uploaded_file.name,
        "taille": format_file_size(uploaded_file.size),
        "taille_bytes": uploaded_file.size,
        "type": uploaded_file.type,
        "extension": Path(uploaded_file.name).suffix.lower(),
        "nom_propre": clean_filename(uploaded_file.name)
    }

def cleanup_temp_file(file_path):
    """
    Supprime un fichier temporaire en toute sécurité.
    
    Args:
        file_path (str): Chemin vers le fichier à supprimer
    """
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        # Log silencieux, pas d'erreur utilisateur pour le nettoyage
        pass

def save_processed_document(doc_name, pages, file_path, original_name):
    """
    Sauvegarde un document traité dans le session state.
    
    Args:
        doc_name (str): Nom du document
        pages (list): Liste des pages extraites
        file_path (str): Chemin vers le fichier sauvegardé
        original_name (str): Nom original du fichier
    """
    if 'processed_documents' not in st.session_state:
        st.session_state.processed_documents = {}
    
    st.session_state.processed_documents[doc_name] = {
        'pages': pages,
        'file_path': str(file_path),
        'original_name': original_name,
        'num_pages': len(pages),
        'processed_at': str(Path().resolve())  # Timestamp simple
    }

def get_processed_documents():
    """
    Récupère la liste des documents traités.
    
    Returns:
        dict: Dictionnaire des documents traités
    """
    return st.session_state.get('processed_documents', {})

def delete_processed_document(doc_name):
    """
    Supprime un document traité du session state.
    
    Args:
        doc_name (str): Nom du document à supprimer
    """
    if 'processed_documents' in st.session_state and doc_name in st.session_state.processed_documents:
        # Optionnel : supprimer aussi le fichier physique
        doc_data = st.session_state.processed_documents[doc_name]
        file_path = doc_data.get('file_path')
        if file_path and os.path.exists(file_path):
            cleanup_temp_file(file_path)
        
        # Supprimer du session state
        del st.session_state.processed_documents[doc_name]

def search_in_pages(pages, search_term):
    """
    Recherche un terme dans les pages extraites.
    
    Args:
        pages (list): Liste des pages
        search_term (str): Terme à rechercher
        
    Returns:
        list: Liste des numéros de pages contenant le terme
    """
    matching_pages = []
    search_term = search_term.lower()
    
    for i, page_content in enumerate(pages):
        if search_term in page_content.lower():
            matching_pages.append(i + 1)  # Numéro de page (base 1)
    
    return matching_pages

def delete_page_from_document(doc_name, page_index):
    """
    Supprime une page spécifique d'un document traité.
    
    Args:
        doc_name (str): Nom du document
        page_index (int): Index de la page à supprimer (base 0)
    """
    if 'processed_documents' in st.session_state and doc_name in st.session_state.processed_documents:
        doc_data = st.session_state.processed_documents[doc_name]
        pages = doc_data['pages']
        
        if 0 <= page_index < len(pages):
            # Supprimer la page
            pages.pop(page_index)
            
            # Mettre à jour le nombre de pages
            st.session_state.processed_documents[doc_name]['num_pages'] = len(pages)
            
            # Si plus de pages, supprimer le document entier
            if len(pages) == 0:
                delete_processed_document(doc_name)

def get_page_statistics(pages):
    """
    Calcule des statistiques sur les pages.
    
    Args:
        pages (list): Liste des pages
        
    Returns:
        dict: Statistiques des pages
    """
    if not pages:
        return {"total_pages": 0, "total_chars": 0, "avg_chars_per_page": 0}
    
    total_chars = sum(len(page) for page in pages)
    
    return {
        "total_pages": len(pages),
        "total_chars": total_chars,
        "avg_chars_per_page": total_chars // len(pages) if pages else 0,
        "shortest_page": min(len(page) for page in pages) if pages else 0,
        "longest_page": max(len(page) for page in pages) if pages else 0
    }