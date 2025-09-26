# utils/function.py
import os
import re
import tempfile
import streamlit as st
from pathlib import Path
import sys
import json
from typing import List, Dict, Any, Optional, Tuple

# Ajouter le chemin vers le module content_extraction qui est dans le dossier parent
sys.path.append(str(Path(__file__).parent.parent))

try:
    from utils.content_extraction import Content_Extractor
    LLAMAPARSE_AVAILABLE = True
except ImportError:
    LLAMAPARSE_AVAILABLE = False

try:
    from utils.Summarizer import SummarizerAgent
    SUMMARIZER_AVAILABLE = True
except ImportError:
    SUMMARIZER_AVAILABLE = False

try:
    from utils.vulnerability_analyzer import analyze_vulnerabilities
    VULNERABILITY_AVAILABLE = True
except ImportError:
    VULNERABILITY_AVAILABLE = False

# ========== CONFIGURATION ==========
PROCESSED_DIR = Path(__file__).parent.parent / "processed_documents"
PROCESSED_DIR.mkdir(exist_ok=True)

# ========== FONCTIONS UTILITAIRES LLAMAPARSE ==========

def extract_pages(text: str) -> List[str]:
    """
    Extrait les pages en découpant sur chaque balise de fermeture </pageN>.
    
    Args:
        text: Texte contenant les balises de pages
        
    Returns:
        Liste des contenus de pages extraites
    """
    parts = re.split(r'</\s*page\s*\d+\s*>', text, flags=re.IGNORECASE)
    pages = []
    
    for part in parts:
        page = re.sub(r'<\s*page\s*\d+\s*>', '', part, flags=re.IGNORECASE).strip()
        if page:
            pages.append(page)
    
    # Si aucune page n'est trouvée, découper par longueur
    if not pages and text:
        # Découper le texte en pages de ~3000 caractères
        page_size = 3000
        for i in range(0, len(text), page_size):
            pages.append(text[i:i+page_size])
    
    return pages

def save_uploaded_file(uploaded_file) -> Optional[str]:
    """
    Sauvegarde le fichier uploadé temporairement.
    
    Args:
        uploaded_file: Fichier uploadé via Streamlit
        
    Returns:
        Chemin vers le fichier temporaire ou None si erreur
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde du fichier : {e}")
        return None

def process_with_llamaparse(file_path: str, output_name: str) -> Optional[Tuple[str, Path]]:
    """
    Traite le fichier avec LlamaParse et retourne le contenu.
    
    Args:
        file_path: Chemin vers le fichier à traiter
        output_name: Nom pour le fichier de sortie
        
    Returns:
        tuple: (texte_complet, chemin_fichier_sortie) ou None si erreur
    """
    try:
        if not LLAMAPARSE_AVAILABLE:
            st.error("LlamaParse n'est pas disponible. Vérifiez l'installation.")
            return None
            
        extractor = Content_Extractor()
        documents = extractor.extract_content(file_path)
        
        if documents:
            full_text = '\n'.join([doc.text for doc in documents if hasattr(doc, 'text') and doc.text])
            
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

def clean_filename(filename: str) -> str:
    """
    Nettoie le nom de fichier pour éviter les caractères problématiques.
    
    Args:
        filename: Nom de fichier original
        
    Returns:
        Nom de fichier nettoyé
    """
    clean_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    name_parts = clean_name.rsplit('.', 1)
    if len(name_parts) == 2:
        clean_name = name_parts[0].replace('.', '_') + '.' + name_parts[1]
    else:
        clean_name = clean_name.replace('.', '_')
    
    return clean_name[:50]  # Limiter la longueur

def format_file_size(size_bytes: int) -> str:
    """
    Formate la taille de fichier en unités lisibles.
    
    Args:
        size_bytes: Taille en bytes
        
    Returns:
        Taille formatée (ex: "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_file_type(filename: str, allowed_types: Optional[List[str]] = None) -> bool:
    """
    Valide le type de fichier.
    
    Args:
        filename: Nom du fichier
        allowed_types: Liste des extensions autorisées
        
    Returns:
        True si le type est autorisé
    """
    if allowed_types is None:
        allowed_types = ['.pdf', '.docx', '.txt', '.doc', '.md']
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_types

def get_file_info(uploaded_file) -> Dict[str, Any]:
    """
    Extrait les informations du fichier uploadé.
    
    Args:
        uploaded_file: Fichier uploadé via Streamlit
        
    Returns:
        Dictionnaire avec les informations du fichier
    """
    return {
        "nom": uploaded_file.name,
        "taille": format_file_size(uploaded_file.size),
        "taille_bytes": uploaded_file.size,
        "type": uploaded_file.type,
        "extension": Path(uploaded_file.name).suffix.lower(),
        "nom_propre": clean_filename(uploaded_file.name)
    }

def cleanup_temp_file(file_path: str) -> None:
    """
    Supprime un fichier temporaire en toute sécurité.
    
    Args:
        file_path: Chemin vers le fichier à supprimer
    """
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception:
        pass  # Ignorer les erreurs de suppression

# ========== GESTION DES DOCUMENTS TRAITÉS ==========

def save_processed_document(doc_name: str, pages: List[str], file_path: str, original_name: str) -> None:
    """
    Sauvegarde un document traité dans le session state.
    
    Args:
        doc_name: Nom du document
        pages: Liste des pages extraites
        file_path: Chemin vers le fichier sauvegardé
        original_name: Nom original du fichier
    """
    if 'processed_documents' not in st.session_state:
        st.session_state.processed_documents = {}
    
    st.session_state.processed_documents[doc_name] = {
        'pages': pages,
        'file_path': str(file_path),
        'original_name': original_name,
        'num_pages': len(pages),
        'processed_at': str(Path().resolve()),
        'type': 'llamaparse'
    }

def get_processed_documents() -> Dict[str, Any]:
    """
    Récupère la liste des documents traités.
    
    Returns:
        Dictionnaire des documents traités
    """
    return st.session_state.get('processed_documents', {})

def delete_processed_document(doc_name: str) -> None:
    """
    Supprime un document traité du session state.
    
    Args:
        doc_name: Nom du document à supprimer
    """
    if 'processed_documents' in st.session_state and doc_name in st.session_state.processed_documents:
        doc_data = st.session_state.processed_documents[doc_name]
        file_path = doc_data.get('file_path')
        if file_path and os.path.exists(file_path):
            cleanup_temp_file(file_path)
        
        del st.session_state.processed_documents[doc_name]

def delete_page_from_document(doc_name: str, page_index: int) -> bool:
    """
    Supprime une page spécifique d'un document traité.
    
    Args:
        doc_name: Nom du document
        page_index: Index de la page à supprimer (base 0)
        
    Returns:
        True si suppression réussie
    """
    if 'processed_documents' in st.session_state and doc_name in st.session_state.processed_documents:
        doc_data = st.session_state.processed_documents[doc_name]
        pages = doc_data['pages']
        
        if 0 <= page_index < len(pages):
            pages.pop(page_index)
            st.session_state.processed_documents[doc_name]['num_pages'] = len(pages)
            
            if len(pages) == 0:
                delete_processed_document(doc_name)
                return False  # Document entièrement supprimé
            return True
    return False

def get_page_statistics(pages: List[str]) -> Dict[str, Any]:
    """
    Calcule des statistiques sur les pages.
    
    Args:
        pages: Liste des pages
        
    Returns:
        Statistiques des pages
    """
    if not pages:
        return {
            "total_pages": 0,
            "total_chars": 0,
            "avg_chars_per_page": 0,
            "shortest_page": 0,
            "longest_page": 0
        }
    
    total_chars = sum(len(page) for page in pages)
    
    return {
        "total_pages": len(pages),
        "total_chars": total_chars,
        "avg_chars_per_page": total_chars // len(pages) if pages else 0,
        "shortest_page": min(len(page) for page in pages) if pages else 0,
        "longest_page": max(len(page) for page in pages) if pages else 0
    }

# ========== FONCTIONS SUMMARIZER ==========

def process_with_summarizer(
    pages: List[str], 
    doc_name: str, 
    progress_callback: Optional[callable] = None, 
    status_callback: Optional[callable] = None
) -> Optional[Tuple[List[Dict], Path, int, int]]:
    """
    Traite les pages avec le Summarizer Agent.
    
    Args:
        pages: Liste des pages à traiter
        doc_name: Nom du document
        progress_callback: Fonction pour la barre de progression
        status_callback: Fonction pour les messages de statut
        
    Returns:
        tuple: (summaries, output_path, success_count, error_count) ou None si erreur
    """
    try:
        if not SUMMARIZER_AVAILABLE:
            st.error("Module Summarizer non disponible")
            return None
            
        agent = SummarizerAgent()
        summaries, success_count, error_count = agent.process_pages(
            pages, progress_callback, status_callback
        )
        
        output_path = PROCESSED_DIR / f"{doc_name}_summaries.json"
        success = agent.save_results(summaries, output_path)
        
        if success:
            # Calculer et afficher les statistiques
            stats = agent.get_statistics(summaries)
            if status_callback:
                status_callback(f"✅ Traité: {stats['successful_pages']}/{stats['total_pages']} pages")
            
            return summaries, output_path, success_count, error_count
        else:
            return None
            
    except Exception as e:
        st.error(f"Erreur lors du traitement avec Summarizer : {e}")
        return None

def save_summarizer_document(
    doc_name: str, 
    summaries: List[Dict], 
    file_path: str, 
    original_name: str, 
    success_count: int, 
    error_count: int
) -> None:
    """
    Sauvegarde un document traité par le Summarizer dans le session state.
    
    Args:
        doc_name: Nom du document
        summaries: Liste des résumés par page
        file_path: Chemin vers le fichier sauvegardé
        original_name: Nom original du fichier
        success_count: Nombre de pages traitées avec succès
        error_count: Nombre de pages avec erreur
    """
    if 'summarizer_documents' not in st.session_state:
        st.session_state.summarizer_documents = {}
    
    st.session_state.summarizer_documents[doc_name] = {
        'summaries': summaries,
        'file_path': str(file_path),
        'original_name': original_name,
        'num_pages': len(summaries),
        'success_count': success_count,
        'error_count': error_count,
        'processed_at': str(Path().resolve()),
        'type': 'summarizer'
    }

def get_summarizer_documents() -> Dict[str, Any]:
    """
    Récupère la liste des documents traités par le Summarizer.
    
    Returns:
        Dictionnaire des documents traités
    """
    return st.session_state.get('summarizer_documents', {})

def delete_summarizer_document(doc_name: str) -> None:
    """
    Supprime un document traité par le Summarizer du session state.
    
    Args:
        doc_name: Nom du document à supprimer
    """
    if 'summarizer_documents' in st.session_state and doc_name in st.session_state.summarizer_documents:
        doc_data = st.session_state.summarizer_documents[doc_name]
        file_path = doc_data.get('file_path')
        if file_path and os.path.exists(file_path):
            cleanup_temp_file(file_path)
        
        del st.session_state.summarizer_documents[doc_name]

def process_existing_pages_with_summarizer(
    pages: List[str], 
    doc_name: str, 
    progress_callback: Optional[callable] = None, 
    status_callback: Optional[callable] = None
) -> Optional[Tuple[List[Dict], Path, int, int]]:
    """
    Traite directement des pages déjà extraites avec le Summarizer Agent.
    
    Args:
        pages: Liste des pages déjà extraites
        doc_name: Nom du document
        progress_callback: Fonction pour la barre de progression
        status_callback: Fonction pour les messages de statut
        
    Returns:
        tuple: (summaries, output_path, success_count, error_count) ou None si erreur
    """
    try:
        if not SUMMARIZER_AVAILABLE:
            st.error("Module Summarizer non disponible")
            return None
            
        agent = SummarizerAgent()
        summaries, success_count, error_count = agent.process_pages(
            pages, progress_callback, status_callback
        )
        
        output_path = PROCESSED_DIR / f"{doc_name}_summaries_direct.json"
        success = agent.save_results(summaries, output_path)
        
        if success:
            return summaries, output_path, success_count, error_count
        else:
            return None
            
    except Exception as e:
        st.error(f"Erreur lors du traitement direct avec Summarizer : {e}")
        return None

# ========== FONCTION DE NETTOYAGE DU CONTENU ==========
def clean_llm_output(text: str) -> str:
    """
    Nettoie la sortie des modèles LLM des balises de code indésirables.
    
    Args:
        text: Texte à nettoyer
        
    Returns:
        Texte nettoyé
    """
    if not text:
        return ""
    
    # Supprimer les blocs de code JSON
    text = re.sub(r'```json\s*\{.*?\}\s*```', '', text, flags=re.DOTALL)
    
    # Supprimer les marqueurs de code
    text = re.sub(r'```\w*', '', text)
    
    # Nettoyer les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()