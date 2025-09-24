# src/app.py
import streamlit as st
from pathlib import Path
import base64
import sys

# ========== CONFIG (DOIT ÊTRE EN PREMIER) ==========
st.set_page_config(page_title="Risk Analyst Hub", layout="wide", initial_sidebar_state="expanded")

# Ajouter le chemin vers les modules
sys.path.append(str(Path(__file__).parent))

# Initialiser les variables globales
UTILS_AVAILABLE = False
LLAMAPARSE_AVAILABLE = False

# Importer les fonctions utilitaires avec diagnostic détaillé
try:
    from utils.function import (
        extract_pages, save_uploaded_file, process_with_llamaparse,
        clean_filename, get_file_info, cleanup_temp_file,
        save_processed_document, get_processed_documents, 
        delete_processed_document, search_in_pages, LLAMAPARSE_AVAILABLE,
        delete_page_from_document, get_page_statistics
    )
    UTILS_AVAILABLE = True
except ImportError as e:
    UTILS_AVAILABLE = False
    # Ne pas utiliser st.error ici, on le fera plus tard dans l'interface

# Configuration des chemins
STATIC_DIR = Path(__file__).parent / "static"
ASSETS_DIR = Path(__file__).parent.parent / "assets"

# ========== FONCTIONS DE DIAGNOSTIC ==========
def show_diagnostic_info():
    """Affiche les informations de diagnostic des modules"""
    st.error("Erreur d'importation des modules utilitaires")
    
    # Diagnostic détaillé
    utils_dir = Path(__file__).parent / "utils"
    fonctions_file = utils_dir / "fonctions.py"
    content_file = Path(__file__).parent / "content_extraction.py"
    
    st.write("### Diagnostic des fichiers :")
    st.write(f"- Dossier utils existe : {utils_dir.exists()}")
    st.write(f"- Fichier fonctions.py existe : {fonctions_file.exists()}")
    st.write(f"- Fichier content_extraction.py existe : {content_file.exists()}")
    
    if utils_dir.exists():
        st.write(f"- Contenu du dossier utils : {list(utils_dir.iterdir())}")
    
    st.write("### Actions à effectuer :")
    if not utils_dir.exists():
        st.write("1. Créez le dossier `src/utils/`")
    if not fonctions_file.exists():
        st.write("2. Copiez le fichier `fonctions.py` dans `src/utils/`")
    if not content_file.exists():
        st.write("3. Vérifiez que `content_extraction.py` est dans `src/`")
    
    st.write("4. Redémarrez l'application")

# ========== CHARGER LES STYLES CSS ==========
def load_styles():
    css_files = [
        "style.css", "sidebar.css", "about.css", "note_ai.css",
        "agent_card.css", "main_area.css", "main_chat_input.css",
        "step_indicator.css"
    ]
    for css_file in css_files:
        css_path = STATIC_DIR / css_file
        if css_path.exists():
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ========== CHARGER UN HTML ==========
def load_html(filename):
    html_path = STATIC_DIR / filename
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ========== LOGO EN BASE64 POUR SIDEBAR ==========
def load_logo():
    logo_path = STATIC_DIR / "assets" / "logo_lgi.png"
    if logo_path.exists():
        with open(logo_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    return None

# ========== UI SIDEBAR ==========
def sidebar():
    # Charger le CSS spécifique à la sidebar
    sidebar_css_path = STATIC_DIR / "sidebar.css"
    if sidebar_css_path.exists():
        with open(sidebar_css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
    # Charger le logo
    logo_base64 = load_logo()
        
    with st.sidebar:
        if logo_base64:
            st.markdown(f"""
<div class='sidebar-logo-block'>
    <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo" />
    <div class='sidebar-title'>Risk Analyst</div>
</div>
""", unsafe_allow_html=True)
        
        # Afficher les documents traités seulement si les utilitaires sont disponibles
        if UTILS_AVAILABLE:
            processed_docs = get_processed_documents()
            if processed_docs:
                st.markdown("---")
                st.markdown("### Documents traités")
                
                for doc_name, doc_data in processed_docs.items():
                    with st.expander(f"📄 {doc_data['original_name']}", expanded=False):
                        st.write(f"**Pages extraites:** {doc_data['num_pages']}")
                        
                        # Option de recherche dans le document
                        search_term = st.text_input(
                            "Rechercher dans le document:", 
                            key=f"search_{doc_name}",
                            placeholder="Tapez un mot-clé..."
                        )
                        
                        if search_term:
                            matching_pages = search_in_pages(doc_data['pages'], search_term)
                            if matching_pages:
                                st.success(f"Trouvé dans {len(matching_pages)} page(s): {matching_pages}")
                            else:
                                st.info("Aucun résultat trouvé")
                        
                        # Sélecteur de page
                        if doc_data['pages']:
                            selected_page = st.selectbox(
                                "Page:", 
                                range(1, len(doc_data['pages']) + 1),
                                format_func=lambda x: f"Page {x}",
                                key=f"page_selector_{doc_name}"
                            )
                            
                            if st.button(f"Voir Page {selected_page}", key=f"view_page_{doc_name}_{selected_page}"):
                                # Afficher la page dans la zone principale
                                st.session_state.viewing_page = {
                                    'doc_name': doc_name,
                                    'page_num': selected_page,
                                    'content': doc_data['pages'][selected_page - 1],
                                    'original_name': doc_data['original_name']
                                }
                                st.rerun()
                        
                        if st.button(f"Supprimer", key=f"delete_{doc_name}"):
                            delete_processed_document(doc_name)
                            st.rerun()
        else:
            # Message si les utilitaires ne sont pas disponibles
            st.markdown("---")
            st.info("💡 Les fonctionnalités de gestion des documents ne sont pas disponibles. Vérifiez que le fichier utils/fonctions.py existe.")

# ========== FONCTIONS POUR TRAITER LES AGENTS ==========
def process_llamaparse_agent(uploaded_file):
    """Traite le fichier avec l'agent LlamaParse en utilisant les fonctions utilitaires"""
    if not UTILS_AVAILABLE:
        show_diagnostic_info()
        return
        
    if not LLAMAPARSE_AVAILABLE:
        st.error("LlamaParse n'est pas disponible")
        st.info("Vérifiez :")
        st.write("- Le fichier `content_extraction.py` existe")
        st.write("- Les dépendances sont installées : `pip install llama-parse llama-index`")
        st.write("- Votre clé API est dans le fichier `.env`")
        return
        
    if uploaded_file is not None:
        # Obtenir les informations du fichier
        file_info = get_file_info(uploaded_file)
        st.success(f"Fichier '{file_info['nom']}' chargé ({file_info['taille']})")
        
        # Barre de progression
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Étape 1: Sauvegarde du fichier
        status_text.text("Sauvegarde du fichier...")
        progress_bar.progress(20)
        
        temp_file_path = save_uploaded_file(uploaded_file)
        if not temp_file_path:
            return
        
        # Étape 2: Traitement LlamaParse
        status_text.text("Traitement avec LlamaParse en cours...")
        progress_bar.progress(50)
        
        doc_name = clean_filename(uploaded_file.name).replace('.', '_')
        result = process_with_llamaparse(temp_file_path, doc_name)
        
        if result:
            full_text, output_path = result
            
            # Étape 3: Extraction des pages
            status_text.text("Extraction des pages...")
            progress_bar.progress(80)
            
            pages = extract_pages(full_text)
            
            # Étape 4: Sauvegarde dans session state
            save_processed_document(doc_name, pages, output_path, uploaded_file.name)
            
            # Étape 5: Affichage des résultats
            progress_bar.progress(100)
            status_text.text("Traitement terminé !")
            
            # Affichage des résultats
            st.markdown("### Document parsé avec succès")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.metric("Pages extraites", len(pages))
                st.metric("Taille du contenu", f"{len(full_text)} caractères")
                st.metric("Type de fichier", file_info['type'])
            
            with col2:
                # Aperçu du document
                with st.expander("Aperçu du contenu extrait", expanded=True):
                    if pages:
                        # Sélecteur de page
                        selected_page = st.selectbox(
                            "Sélectionner une page", 
                            range(1, len(pages) + 1),
                            format_func=lambda x: f"Page {x}"
                        )
                        
                        if selected_page:
                            st.markdown(f"**Page {selected_page}:**")
                            # Limiter l'affichage pour éviter de surcharger
                            page_content = pages[selected_page - 1]
                            if len(page_content) > 2000:
                                st.markdown(page_content[:2000] + "...")
                                st.info("Contenu tronqué. Voir la page complète dans la sidebar.")
                            else:
                                st.markdown(page_content)
                    else:
                        st.write("Aucune page détectée avec les balises <pageN>")
                        # Afficher le contenu complet si pas de pages
                        if len(full_text) > 2000:
                            st.text_area("Aperçu du contenu:", full_text[:2000] + "...", height=300)
                        else:
                            st.text_area("Contenu complet:", full_text, height=300)
            
            # Message de succès
            st.success(f"Document '{uploaded_file.name}' ajouté à la sidebar avec {len(pages)} pages")
            
        # Nettoyage du fichier temporaire
        cleanup_temp_file(temp_file_path)

def process_summary_agent(uploaded_file):
    """Traite le fichier avec l'agent Summary"""
    if uploaded_file is not None:
        st.success(f"Fichier '{uploaded_file.name}' chargé pour l'agent Summary")
        st.info("Traitement en cours avec l'agent Summary...")
        
        # Exemple d'affichage des informations du fichier
        file_details = {
            "Nom": uploaded_file.name,
            "Taille": f"{uploaded_file.size} bytes",
            "Type": uploaded_file.type
        }
        st.json(file_details)
        
        # Placeholder pour le résumé
        st.markdown("### Résumé généré")
        st.write("Le résumé du document apparaîtra ici après traitement...")

def process_vulnerability_agent(uploaded_file):
    """Traite le fichier avec l'agent Vulnerability"""
    if uploaded_file is not None:
        st.success(f"Fichier '{uploaded_file.name}' chargé pour l'agent Vulnerability")
        st.info("Analyse des vulnérabilités en cours...")
        
        # Placeholder pour l'analyse
        st.markdown("### Analyse de vulnérabilité")
        st.write("Les vulnérabilités détectées apparaîtront ici...")

def process_aloe_agent(uploaded_file):
    """Traite le fichier avec l'agent ALOE"""
    if uploaded_file is not None:
        st.success(f"Fichier '{uploaded_file.name}' chargé pour l'agent ALOE")
        st.info("Extraction des objets et attributs en cours...")
        
        # Placeholder pour l'extraction ALOE
        st.markdown("### Méthode ALOE")
        st.write("Les objets et attributs extraits apparaîtront ici...")

def process_link_agent(uploaded_file):
    """Traite le fichier avec l'agent Link"""
    if uploaded_file is not None:
        st.success(f"Fichier '{uploaded_file.name}' chargé pour l'agent Link")
        st.info("Construction des liens hiérarchiques en cours...")
        
        # Placeholder pour l'analyse des liens
        st.markdown("### Liens hiérarchiques")
        st.write("Les liens entre objets apparaîtront ici...")

# ========== INTERFACE POUR CHAQUE AGENT ==========
def show_agent_interface(agent_type):
    """Affiche l'interface d'upload et de traitement pour un agent spécifique"""
    
    agent_configs = {
        "llamaparse": {
            "title": "LlamaParse Agent",
            "description": "Chargez un document pour l'analyser et extraire le contenu page par page",
            "processor": process_llamaparse_agent
        },
        "summary": {
            "title": "Summary Agent",
            "description": "Chargez un document pour générer un résumé page par page",
            "processor": process_summary_agent
        },
        "vulnerability": {
            "title": "Vulnerability and Threat Agent", 
            "description": "Chargez un document pour identifier les vulnérabilités et menaces",
            "processor": process_vulnerability_agent
        },
        "aloe": {
            "title": "ALOE Agent",
            "description": "Chargez un document pour extraire les objets et attributs (méthode ALOE)",
            "processor": process_aloe_agent
        },
        "link": {
            "title": "Link Agent",
            "description": "Chargez un document pour construire les liens hiérarchiques entre objets",
            "processor": process_link_agent
        }
    }
    
    if agent_type in agent_configs:
        config = agent_configs[agent_type]
        
        st.markdown(f"## {config['title']}")
        st.markdown(f"*{config['description']}*")
        
        # Zone d'upload de fichier
        uploaded_file = st.file_uploader(
            "Choisissez un fichier",
            type=['pdf', 'docx', 'txt', 'doc'],
            key=f"uploader_{agent_type}",
            help="Formats supportés: PDF, Word, Text"
        )
        
        # Boutons d'action
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("Analyser", key=f"analyze_{agent_type}"):
                if uploaded_file is not None:
                    config['processor'](uploaded_file)
                else:
                    st.warning("Veuillez d'abord charger un fichier")
        
        with col2:
            if st.button("Retour", key=f"back_{agent_type}"):
                st.session_state.selected_agent = None
                st.rerun()

# ========== CARTES INTERACTIVES AVEC DESIGN ORIGINAL ==========
def interactive_agent_cards_with_streamlit():
    """Cartes originales avec boutons Streamlit stylés directement sous chaque carte"""
    
    # CSS pour styliser les boutons Streamlit comme les boutons originaux
    st.markdown("""
    <style>
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa, #00a085);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
        width: 100%;
        margin-top: 10px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00a085, #007d66);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 10px rgba(0, 212, 170, 0.3);
    }
    
    /* Supprimer les boutons RUN AGENT du HTML */
    .run-button {
        display: none !important;
    }
    
    /* Style pour les cartes individuelles */
    .individual-agent-card {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Créer une grille 2x2 pour les cartes avec leurs boutons
    col1, col2 = st.columns(2)
    
    # Configuration des agents (avec LlamaParse en premier)
    agents = [
        {
            "html": """
            <div class="individual-agent-card">
                <div class="agent-card">
                    <div class="feature-icon">📄</div>
                    <div class="feature-title">LlamaParse Agent</div>
                    <div class="feature-description">Parses documents and extracts content page by page with high accuracy.</div>
                </div>
            </div>
            """,
            "button_text": "RUN LLAMAPARSE AGENT",
            "key": "btn_llamaparse",
            "agent_id": "llamaparse"
        },
        {
            "html": """
            <div class="individual-agent-card">
                <div class="agent-card">
                    <div class="feature-icon">🧾</div>
                    <div class="feature-title">Summary Agent</div>
                    <div class="feature-description">Summarizes project content page by page.</div>
                </div>
            </div>
            """,
            "button_text": "RUN SUMMARY AGENT",
            "key": "btn_summary",
            "agent_id": "summary"
        },
        {
            "html": """
            <div class="individual-agent-card">
                <div class="agent-card">
                    <div class="feature-icon">🔍</div>
                    <div class="feature-title">Vulnerability and Threat Agent</div>
                    <div class="feature-description">Identifies vulnerable elements and Detects threats in project documents.</div>
                </div>
            </div>
            """,
            "button_text": "RUN VULNERABILITY AGENT",
            "key": "btn_vulnerability", 
            "agent_id": "vulnerability"
        },
        {
            "html": """
            <div class="individual-agent-card">
                <div class="agent-card">
                    <div class="feature-icon">🔗</div>
                    <div class="feature-title">ALOE Agent</div>
                    <div class="feature-description">Extracts project objects and attributes (ALOE method).</div>
                </div>
            </div>
            """,
            "button_text": "RUN ALOE AGENT",
            "key": "btn_aloe",
            "agent_id": "aloe"
        },
        {
            "html": """
            <div class="individual-agent-card">
                <div class="agent-card">
                    <div class="feature-icon">🕸️</div>
                    <div class="feature-title">Link Agent</div>
                    <div class="feature-description">Builds hierarchical and sequential links between objects.</div>
                </div>
            </div>
            """,
            "button_text": "RUN LINK AGENT",
            "key": "btn_link",
            "agent_id": "link"
        }
    ]
    
    # Première ligne : LlamaParse et Summary  
    with col1:
        # Carte LlamaParse
        st.markdown(agents[0]["html"], unsafe_allow_html=True)
        if st.button(agents[0]["button_text"], key=agents[0]["key"]):
            st.session_state.selected_agent = agents[0]["agent_id"]
            st.rerun()
            
    with col2:
        # Carte Summary
        st.markdown(agents[1]["html"], unsafe_allow_html=True)
        if st.button(agents[1]["button_text"], key=agents[1]["key"]):
            st.session_state.selected_agent = agents[1]["agent_id"]
            st.rerun()
    
    # Deuxième ligne : Vulnerability et ALOE
    with col1:
        # Carte Vulnerability
        st.markdown(agents[2]["html"], unsafe_allow_html=True)
        if st.button(agents[2]["button_text"], key=agents[2]["key"]):
            st.session_state.selected_agent = agents[2]["agent_id"]
            st.rerun()
            
    with col2:
        # Carte ALOE
        st.markdown(agents[3]["html"], unsafe_allow_html=True)
        if st.button(agents[3]["button_text"], key=agents[3]["key"]):
            st.session_state.selected_agent = agents[3]["agent_id"]
            st.rerun()
    
    # Troisième ligne : Link (centré)
    col_empty, col_center, col_empty2 = st.columns([1, 2, 1])
    with col_center:
        # Carte Link
        st.markdown(agents[4]["html"], unsafe_allow_html=True)
        if st.button(agents[4]["button_text"], key=agents[4]["key"]):
            st.session_state.selected_agent = agents[4]["agent_id"]
            st.rerun()

# ========== UI PRINCIPALE ==========
def main_ui():
    # Initialiser l'état de session si nécessaire
    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = None
    
    # Vérifier si on affiche une page de document
    if 'viewing_page' in st.session_state and st.session_state.viewing_page:
        show_document_viewer()
        return
    
    # Vérifier si un agent est sélectionné
    if st.session_state.selected_agent:
        # Afficher l'interface de l'agent sélectionné
        show_agent_interface(st.session_state.selected_agent)
    else:
        # Afficher la page d'accueil avec le design original
        st.title("AI Assistant for Risk Analysis")
        st.markdown("Welcome to your AI-enhanced risk assessment workspace.")
        
        # Utiliser les cartes interactives avec le design original
        interactive_agent_cards_with_streamlit()
        
        with st.expander("ℹ About this App", expanded=False):
            # Vérifier si le fichier about.html existe et le charger proprement
            about_html = load_html("about.html")
            if about_html:
                st.markdown(about_html, unsafe_allow_html=True)
            else:
                # Affichage par défaut si le fichier n'existe pas
                st.markdown("""
                **AI-Powered Risk Intelligence Platform**
                
                Notre plateforme utilise l'intelligence artificielle avancée pour transformer votre processus d'analyse des risques.
                
                **Fonctionnalités principales :**
                - 📄 **LlamaParse Agent** : Parsing et extraction de contenu
                - 🧾 **Summary Agent** : Résumé automatique des documents
                - 🔍 **Vulnerability Agent** : Détection des vulnérabilités
                - 🔗 **ALOE Agent** : Extraction d'objets et attributs
                - 🕸️ **Link Agent** : Analyse des liens hiérarchiques
                """)

# ========== VISUALISATEUR DE DOCUMENTS ==========
def show_document_viewer():
    """Affiche le visualisateur de document avec style PDF et gestion des pages"""
    if not UTILS_AVAILABLE:
        st.error("Les fonctions utilitaires ne sont pas disponibles")
        if st.button("← Retour", key="back_from_page_error"):
            del st.session_state.viewing_page
            st.rerun()
        return
    
    page_data = st.session_state.viewing_page
    doc_name = page_data['doc_name']
    current_page = page_data['page_num']
    
    # Récupérer les données du document complet
    processed_docs = get_processed_documents()
    doc_data = processed_docs.get(doc_name, {})
    total_pages = len(doc_data.get('pages', []))
    
    # Vérifier si le document existe encore
    if not doc_data or not doc_data.get('pages'):
        st.error("Document non trouvé ou supprimé")
        if st.button("← Retour", key="back_from_missing_doc"):
            del st.session_state.viewing_page
            st.rerun()
        return
    
    # CSS pour le style document/PDF
    st.markdown("""
    <style>
    .document-viewer {
        background: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .document-page {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 40px;
        margin: 20px auto;
        max-width: 800px;
        min-height: 600px;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        position: relative;
    }
    
    .document-page::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(to right, #ff6b6b, #4ecdc4, #45b7d1);
        border-radius: 8px 8px 0 0;
    }
    
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .page-number {
        position: absolute;
        bottom: 20px;
        right: 30px;
        background: #f8f9fa;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.9em;
        color: #666;
        border: 1px solid #dee2e6;
    }
    
    .navigation-controls {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 20px 0;
        padding: 15px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .page-content {
        text-align: justify;
        color: #333;
    }
    
    .page-content h1, .page-content h2, .page-content h3 {
        color: #2c3e50;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    .page-content p {
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête avec contrôles
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("← Retour", key="back_from_page"):
            del st.session_state.viewing_page
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="page-header">
            <div>
                <h3 style="margin:0;">📄 {page_data['original_name']}</h3>
                <small>Document parsé • {total_pages} pages</small>
            </div>
            <div style="font-size: 1.2em; font-weight: bold;">
                Page {current_page} / {total_pages}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Menu d'actions
        with st.popover("⚙️ Actions"):
            st.write("**Actions sur cette page :**")
            
            if st.button("🗑️ Supprimer cette page", key="delete_current_page"):
                if total_pages > 1:  # Ne pas supprimer si c'est la seule page
                    delete_page_from_document(doc_name, current_page - 1)  # Index base 0
                    st.success(f"Page {current_page} supprimée")
                    # Rediriger vers une page valide
                    new_page = min(current_page, total_pages - 1)
                    if new_page > 0:
                        st.session_state.viewing_page['page_num'] = new_page
                        st.session_state.viewing_page['content'] = doc_data['pages'][new_page - 1]
                    else:
                        del st.session_state.viewing_page
                    st.rerun()
                else:
                    st.error("Impossible de supprimer la dernière page")
            
            st.write("**Navigation rapide :**")
            selected_page = st.selectbox(
                "Aller à la page :",
                range(1, total_pages + 1),
                index=current_page - 1,
                key="page_jump"
            )
            if st.button("Aller", key="jump_to_page") and selected_page != current_page:
                st.session_state.viewing_page = {
                    'doc_name': doc_name,
                    'page_num': selected_page,
                    'content': doc_data['pages'][selected_page - 1],
                    'original_name': page_data['original_name']
                }
                st.rerun()
    
    # Navigation entre pages
    st.markdown('<div class="navigation-controls">', unsafe_allow_html=True)
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])
    
    with nav_col1:
        if current_page > 1:
            if st.button("⏮️ Première", key="first_page"):
                st.session_state.viewing_page = {
                    'doc_name': doc_name,
                    'page_num': 1,
                    'content': doc_data['pages'][0],
                    'original_name': page_data['original_name']
                }
                st.rerun()
    
    with nav_col2:
        if current_page > 1:
            if st.button("⬅️ Précédente", key="prev_page"):
                prev_page = current_page - 1
                st.session_state.viewing_page = {
                    'doc_name': doc_name,
                    'page_num': prev_page,
                    'content': doc_data['pages'][prev_page - 1],
                    'original_name': page_data['original_name']
                }
                st.rerun()
    
    with nav_col3:
        st.markdown(f"<div style='text-align: center; padding: 8px; font-weight: bold;'>Page {current_page} sur {total_pages}</div>", unsafe_allow_html=True)
    
    with nav_col4:
        if current_page < total_pages:
            if st.button("➡️ Suivante", key="next_page"):
                next_page = current_page + 1
                st.session_state.viewing_page = {
                    'doc_name': doc_name,
                    'page_num': next_page,
                    'content': doc_data['pages'][next_page - 1],
                    'original_name': page_data['original_name']
                }
                st.rerun()
    
    with nav_col5:
        if current_page < total_pages:
            if st.button("⏭️ Dernière", key="last_page"):
                st.session_state.viewing_page = {
                    'doc_name': doc_name,
                    'page_num': total_pages,
                    'content': doc_data['pages'][total_pages - 1],
                    'original_name': page_data['original_name']
                }
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Affichage de la page avec style document
    st.markdown('<div class="document-viewer">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="document-page">
        <div class="page-content">
            {page_data['content'].replace('\n', '<br>')}
        </div>
        <div class="page-number">Page {current_page}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== MAIN ==========
def main():
    load_styles()
    sidebar()
    main_ui()

if __name__ == "__main__":
    main()