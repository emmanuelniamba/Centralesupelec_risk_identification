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
    from srcc.utils.functionn import (
        extract_pages, save_uploaded_file, process_with_llamaparse,
        clean_filename, get_file_info, cleanup_temp_file,
        save_processed_document, get_processed_documents, 
        delete_processed_document, LLAMAPARSE_AVAILABLE,
        delete_page_from_document, get_page_statistics,
        process_with_summarizer, save_summarizer_document, 
        get_summarizer_documents, delete_summarizer_document,
        process_existing_pages_with_summarizer
    )
    UTILS_AVAILABLE = True
except ImportError as e:
    UTILS_AVAILABLE = False

# Configuration des chemins
STATIC_DIR = Path(__file__).parent / "static"
ASSETS_DIR = Path(__file__).parent.parent / "assets"

# ========== FONCTIONS DE DIAGNOSTIC ==========
def show_diagnostic_info():
    """Affiche les informations de diagnostic des modules"""
    st.error("Erreur d'importation des modules utilitaires")
    
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
    sidebar_css_path = STATIC_DIR / "sidebar.css"
    if sidebar_css_path.exists():
        with open(sidebar_css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    logo_base64 = load_logo()
    
    with st.sidebar:
        if logo_base64:
            st.markdown(f"""
<div class='sidebar-logo-block'>
    <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo" />
    <div class='sidebar-title'>Risk Analyst</div>
</div>
""", unsafe_allow_html=True)
        
        # Afficher les documents traités automatiquement
        if UTILS_AVAILABLE:
            # Documents LlamaParse
            processed_docs = get_processed_documents()
            if processed_docs:
                st.markdown("---")
                st.markdown("### 📄 Documents LlamaParse")
                
                for doc_name, doc_data in processed_docs.items():
                    with st.expander(f"📄 {doc_data['original_name']}", expanded=False):
                        st.write(f"**Pages extraites:** {doc_data['num_pages']}")
                        
                        # Sélecteur de page simple
                        if doc_data['pages']:
                            selected_page = st.selectbox(
                                "Page:", 
                                range(1, len(doc_data['pages']) + 1),
                                format_func=lambda x: f"Page {x}",
                                key=f"page_selector_{doc_name}"
                            )
                            
                            if st.button(f"Voir Page {selected_page}", key=f"view_page_{doc_name}_{selected_page}"):
                                st.session_state.viewing_page = {
                                    'doc_name': doc_name,
                                    'page_num': selected_page,
                                    'content': doc_data['pages'][selected_page - 1],
                                    'original_name': doc_data['original_name'],
                                    'type': 'llamaparse'
                                }
                                st.rerun()
                        
                        if st.button(f"Supprimer", key=f"delete_{doc_name}"):
                            delete_processed_document(doc_name)
                            st.rerun()
            
            # Documents Summarizer
            summarizer_docs = get_summarizer_documents()
            if summarizer_docs:
                st.markdown("---")
                st.markdown("### 📊 Documents Summarizer")
                
                for doc_name, doc_data in summarizer_docs.items():
                    with st.expander(f"📊 {doc_data['original_name']}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Pages traitées", doc_data['success_count'])
                        with col2:
                            st.metric("Erreurs", doc_data['error_count'])
                        
                        # Sélecteur de page pour les résumés
                        if doc_data['summaries']:
                            selected_page = st.selectbox(
                                "Résumé:", 
                                range(1, len(doc_data['summaries']) + 1),
                                format_func=lambda x: f"Page {x}",
                                key=f"summary_selector_{doc_name}"
                            )
                            
                            if st.button(f"Voir Résumé {selected_page}", key=f"view_summary_{doc_name}_{selected_page}"):
                                summary_data = next((s for s in doc_data['summaries'] if s.get('page') == selected_page), None)
                                if summary_data:
                                    st.session_state.viewing_page = {
                                        'doc_name': doc_name,
                                        'page_num': selected_page,
                                        'content': summary_data,
                                        'original_name': doc_data['original_name'],
                                        'type': 'summarizer'
                                    }
                                    st.rerun()
                        
                        if st.button(f"Supprimer", key=f"delete_summ_{doc_name}"):
                            delete_summarizer_document(doc_name)
                            st.rerun()

# ========== FONCTIONS POUR TRAITER LES AGENTS ==========
def process_llamaparse_agent(uploaded_file):
    """Traite le fichier avec l'agent LlamaParse"""
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
        file_info = get_file_info(uploaded_file)
        st.success(f"Fichier '{file_info['nom']}' chargé ({file_info['taille']})")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Sauvegarde du fichier...")
        progress_bar.progress(20)
        
        temp_file_path = save_uploaded_file(uploaded_file)
        if not temp_file_path:
            return
        
        status_text.text("Traitement avec LlamaParse en cours...")
        progress_bar.progress(50)
        
        doc_name = clean_filename(uploaded_file.name).replace('.', '_')
        result = process_with_llamaparse(temp_file_path, doc_name)
        
        if result:
            full_text, output_path = result
            
            status_text.text("Extraction des pages...")
            progress_bar.progress(80)
            
            pages = extract_pages(full_text)
            
            save_processed_document(doc_name, pages, output_path, uploaded_file.name)
            
            progress_bar.progress(100)
            status_text.text("Traitement terminé !")
            
            # Affichage des résultats en mode texte
            st.markdown("### Document parsé avec succès")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.metric("Pages extraites", len(pages))
                st.metric("Taille du contenu", f"{len(full_text)} caractères")
                st.metric("Type de fichier", file_info['type'])
            
            with col2:
                with st.expander("Aperçu du contenu extrait", expanded=True):
                    if pages:
                        selected_page = st.selectbox(
                            "Sélectionner une page", 
                            range(1, len(pages) + 1),
                            format_func=lambda x: f"Page {x}"
                        )
                        
                        if selected_page:
                            st.text(f"Page {selected_page}:")
                            page_content = pages[selected_page - 1]
                            if len(page_content) > 2000:
                                st.text(page_content[:2000] + "...")
                                st.info("Contenu tronqué. Voir la page complète dans la sidebar.")
                            else:
                                st.text(page_content)
                    else:
                        st.write("Aucune page détectée avec les balises <pageN>")
                        if len(full_text) > 2000:
                            st.text_area("Aperçu du contenu:", full_text[:2000] + "...", height=300)
                        else:
                            st.text_area("Contenu complet:", full_text, height=300)
            
            st.success(f"✅ Document '{uploaded_file.name}' ajouté automatiquement à la sidebar avec {len(pages)} pages")

            # Bouton pour passer au Summarizer
            if st.button("📊 Analyser avec Summary Agent", key="goto_summary_from_llamaparse", type="primary"):
                st.session_state.processing_with_summarizer = {
                    'doc_name': doc_name,
                    'pages': pages,
                    'original_name': uploaded_file.name
                }
                st.session_state.selected_agent = 'summary'
                st.rerun()

        cleanup_temp_file(temp_file_path)

def process_summary_agent(uploaded_file):
    """Traite le fichier avec l'agent Summary"""
    if not UTILS_AVAILABLE:
        show_diagnostic_info()
        return
        
    if uploaded_file is not None:
        file_info = get_file_info(uploaded_file)
        st.success(f"Fichier '{file_info['nom']}' chargé ({file_info['taille']})")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Sauvegarde du fichier...")
        progress_bar.progress(10)
        
        temp_file_path = save_uploaded_file(uploaded_file)
        if not temp_file_path:
            return
        
        status_text.text("Extraction du contenu avec LlamaParse...")
        progress_bar.progress(20)
        
        doc_name = clean_filename(uploaded_file.name).replace('.', '_')
        llamaparse_result = process_with_llamaparse(temp_file_path, doc_name)
        
        if not llamaparse_result:
            status_text.text("Erreur lors de l'extraction")
            cleanup_temp_file(temp_file_path)
            return
        
        full_text, _ = llamaparse_result
        pages = extract_pages(full_text)
        
        if not pages:
            st.error("Aucune page extraite du document")
            cleanup_temp_file(temp_file_path)
            return
        
        def update_progress(value):
            progress_bar.progress(value)
        
        def update_status(message):
            status_text.text(message)
        
        status_text.text("Traitement avec l'agent Summarizer...")
        progress_bar.progress(30)
        
        summarizer_result = process_with_summarizer(
            pages, doc_name, update_progress, update_status
        )
        
        if not summarizer_result:
            cleanup_temp_file(temp_file_path)
            return
        
        summaries, output_path, success_count, error_count = summarizer_result
        
        save_summarizer_document(doc_name, summaries, output_path, uploaded_file.name, success_count, error_count)
        
        progress_bar.progress(100)
        status_text.text("Traitement terminé !")
        
        # Affichage des résultats en mode texte
        st.markdown("### Document traité avec l'agent Summary")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.metric("Pages traitées", success_count)
            st.metric("Pages avec erreur", error_count)
            st.metric("Type de fichier", file_info['type'])
        
        with col2:
            with st.expander("Aperçu des résumés générés", expanded=True):
                if summaries:
                    selected_page = st.selectbox(
                        "Sélectionner une page", 
                        range(1, len(summaries) + 1),
                        format_func=lambda x: f"Page {x}"
                    )
                    
                    if selected_page:
                        summary_data = next((s for s in summaries if s.get('page') == selected_page), None)
                        
                        if summary_data and 'error' not in summary_data:
                            st.text(f"Page {selected_page}:")
                            st.text(f"Section : {summary_data.get('sectionTitle', 'N/A')}")
                            st.text(f"Résumé : {summary_data.get('pageSummary', 'N/A')}")
                            st.text(f"Continuation : {'Oui' if summary_data.get('isContinuation', False) else 'Non'}")
                        else:
                            st.error(f"Erreur sur la page {selected_page}: {summary_data.get('error', 'Erreur inconnue')}")
        
        if error_count > 0:
            st.warning(f"Document '{uploaded_file.name}' traité avec {success_count}/{len(summaries)} pages réussies")
        else:
            st.success(f"✅ Document '{uploaded_file.name}' entièrement traité avec succès et ajouté automatiquement à la sidebar!")
        
        cleanup_temp_file(temp_file_path)

def process_vulnerability_agent():
    """Traite les documents avec l'agent Vulnerability"""
    st.markdown("### Agent Vulnerability and Threat")
    
    # Vérifier les documents disponibles
    llama_docs = get_processed_documents() if UTILS_AVAILABLE else {}
    summary_docs = get_summarizer_documents() if UTILS_AVAILABLE else {}
    
    if not llama_docs and not summary_docs:
        st.warning("Aucun document disponible. Veuillez d'abord traiter un document avec LlamaParse ou Summary Agent.")
        return
    
    # Sélection des documents
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Documents LlamaParse disponibles")
        selected_llama = st.selectbox(
            "Sélectionner un document LlamaParse:", 
            options=["Aucun"] + list(llama_docs.keys()),
            format_func=lambda x: llama_docs[x]['original_name'] if x != "Aucun" and x in llama_docs else x,
            key="vuln_llama_select"
        )
    
    with col2:
        st.markdown("#### Documents Summary disponibles")
        selected_summary = st.selectbox(
            "Sélectionner un document Summary:", 
            options=["Aucun"] + list(summary_docs.keys()),
            format_func=lambda x: summary_docs[x]['original_name'] if x != "Aucun" and x in summary_docs else x,
            key="vuln_summary_select"
        )
    
    if st.button("🔍 Analyser les vulnérabilités", key="analyze_vulnerabilities", type="primary"):
        if selected_llama == "Aucun" and selected_summary == "Aucun":
            st.error("Veuillez sélectionner au moins un document à analyser")
        else:
            with st.spinner("Analyse des vulnérabilités en cours..."):
                # Récupérer les données
                raw_pages = []
                summaries = []
                
                if selected_llama != "Aucun":
                    llama_data = llama_docs[selected_llama]
                    raw_pages = llama_data['pages']
                    st.info(f"📄 Document LlamaParse : {llama_data['original_name']}")
                
                if selected_summary != "Aucun":
                    summary_data = summary_docs[selected_summary]
                    summaries = summary_data['summaries']
                    st.info(f"📊 Document Summary : {summary_data['original_name']}")
                
                # Appel à votre fonction d'analyse
                try:
                    from utils.vulnerability_analyzer import analyze_vulnerabilities
                    results = analyze_vulnerabilities(raw_pages, summaries)
                    
                    st.success("✅ Analyse terminée !")
                    
                    # Affichage des résultats
                    with st.expander("Vulnérabilités détectées", expanded=True):
                        for i, result in enumerate(results, 1):
                            st.text(f"Page {i}: {result}")
                            
                except ImportError:
                    # Placeholder si le module n'existe pas encore
                    st.warning("Module d'analyse des vulnérabilités en développement")
                    st.write(f"- Pages brutes disponibles : {len(raw_pages)}")
                    st.write(f"- Résumés disponibles : {len(summaries)}")

def process_aloe_agent(uploaded_file):
    """Traite le fichier avec l'agent ALOE"""
    if uploaded_file is not None:
        st.success(f"Fichier '{uploaded_file.name}' chargé pour l'agent ALOE")
        st.info("Extraction des objets et attributs en cours...")
        
        st.markdown("### Méthode ALOE")
        st.write("Les objets et attributs extraits apparaîtront ici...")

def process_link_agent(uploaded_file):
    """Traite le fichier avec l'agent Link"""
    if uploaded_file is not None:
        st.success(f"Fichier '{uploaded_file.name}' chargé pour l'agent Link")
        st.info("Construction des liens hiérarchiques en cours...")
        
        st.markdown("### Liens hiérarchiques")
        st.write("Les liens entre objets apparaîtront ici...")

# ========== INTERFACE POUR CHAQUE AGENT ==========
def show_agent_interface(agent_type):
    """Affiche l'interface d'upload et de traitement pour un agent spécifique"""
    
    agent_configs = {
        "llamaparse": {
            "title": "LlamaParse Agent",
            "description": "Chargez un document pour l'analyser et extraire le contenu page par page",
            "processor": process_llamaparse_agent,
            "needs_file": True
        },
        "summary": {
            "title": "Summary Agent",
            "description": "Chargez un document pour générer un résumé page par page",
            "processor": process_summary_agent,
            "needs_file": True
        },
        "vulnerability": {
            "title": "Vulnerability and Threat Agent", 
            "description": "Analysez les vulnérabilités dans vos documents déjà traités",
            "processor": process_vulnerability_agent,
            "needs_file": False
        },
        "aloe": {
            "title": "ALOE Agent",
            "description": "Chargez un document pour extraire les objets et attributs (méthode ALOE)",
            "processor": process_aloe_agent,
            "needs_file": True
        },
        "link": {
            "title": "Link Agent",
            "description": "Chargez un document pour construire les liens hiérarchiques entre objets",
            "processor": process_link_agent,
            "needs_file": True
        }
    }
    
    if agent_type in agent_configs:
        config = agent_configs[agent_type]
        
        st.markdown(f"## {config['title']}")
        st.markdown(f"*{config['description']}*")
        
        if config['needs_file']:
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
        else:
            # Pour l'agent Vulnerability qui n'a pas besoin de fichier
            config['processor']()
            if st.button("Retour", key=f"back_{agent_type}"):
                st.session_state.selected_agent = None
                st.rerun()

# ========== CARTES INTERACTIVES ==========
def interactive_agent_cards_with_streamlit():
    """Cartes originales avec boutons Streamlit"""
    
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
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    agents = [
        {
            "html": """
            <div class="agent-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">LlamaParse Agent</div>
                <div class="feature-description">Parses documents and extracts content page by page with high accuracy.</div>
            </div>
            """,
            "button_text": "RUN LLAMAPARSE AGENT",
            "key": "btn_llamaparse",
            "agent_id": "llamaparse"
        },
        {
            "html": """
            <div class="agent-card">
                <div class="feature-icon">🧾</div>
                <div class="feature-title">Summary Agent</div>
                <div class="feature-description">Summarizes project content page by page.</div>
            </div>
            """,
            "button_text": "RUN SUMMARY AGENT",
            "key": "btn_summary",
            "agent_id": "summary"
        },
        {
            "html": """
            <div class="agent-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Vulnerability Agent</div>
                <div class="feature-description">Identifies vulnerabilities and threats in documents.</div>
            </div>
            """,
            "button_text": "RUN VULNERABILITY AGENT",
            "key": "btn_vulnerability", 
            "agent_id": "vulnerability"
        },
        {
            "html": """
            <div class="agent-card">
                <div class="feature-icon">🔗</div>
                <div class="feature-title">ALOE Agent</div>
                <div class="feature-description">Extracts project objects and attributes.</div>
            </div>
            """,
            "button_text": "RUN ALOE AGENT",
            "key": "btn_aloe",
            "agent_id": "aloe"
        },
        {
            "html": """
            <div class="agent-card">
                <div class="feature-icon">🕸️</div>
                <div class="feature-title">Link Agent</div>
                <div class="feature-description">Builds hierarchical links between objects.</div>
            </div>
            """,
            "button_text": "RUN LINK AGENT",
            "key": "btn_link",
            "agent_id": "link"
        }
    ]
    
    # Première ligne
    with col1:
        st.markdown(agents[0]["html"], unsafe_allow_html=True)
        if st.button(agents[0]["button_text"], key=agents[0]["key"]):
            st.session_state.selected_agent = agents[0]["agent_id"]
            st.rerun()
            
    with col2:
        st.markdown(agents[1]["html"], unsafe_allow_html=True)
        if st.button(agents[1]["button_text"], key=agents[1]["key"]):
            st.session_state.selected_agent = agents[1]["agent_id"]
            st.rerun()
    
    # Deuxième ligne
    with col1:
        st.markdown(agents[2]["html"], unsafe_allow_html=True)
        if st.button(agents[2]["button_text"], key=agents[2]["key"]):
            st.session_state.selected_agent = agents[2]["agent_id"]
            st.rerun()
            
    with col2:
        st.markdown(agents[3]["html"], unsafe_allow_html=True)
        if st.button(agents[3]["button_text"], key=agents[3]["key"]):
            st.session_state.selected_agent = agents[3]["agent_id"]
            st.rerun()
    
    # Troisième ligne (Link centré)
    col_empty, col_center, col_empty2 = st.columns([1, 2, 1])
    with col_center:
        st.markdown(agents[4]["html"], unsafe_allow_html=True)
        if st.button(agents[4]["button_text"], key=agents[4]["key"]):
            st.session_state.selected_agent = agents[4]["agent_id"]
            st.rerun()

# ========== UI PRINCIPALE ==========
def main_ui():
    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = None
    
    # Traitement direct avec le Summarizer
    if 'processing_with_summarizer' in st.session_state and st.session_state.processing_with_summarizer:
        process_direct_summarizer()
        return
    
    # Visualisation d'une page
    if 'viewing_page' in st.session_state and st.session_state.viewing_page:
        show_document_viewer()
        return
    
    # Affichage de l'agent sélectionné ou de l'accueil
    if st.session_state.selected_agent:
        show_agent_interface(st.session_state.selected_agent)
    else:
        st.title("AI Assistant for Risk Analysis")
        st.markdown("Welcome to your AI-enhanced risk assessment workspace.")
        
        interactive_agent_cards_with_streamlit()
        
        with st.expander("ℹ About this App", expanded=False):
            about_html = load_html("about.html")
            if about_html:
                st.markdown(about_html, unsafe_allow_html=True)
            else:
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

# ========== TRAITEMENT DIRECT AVEC SUMMARIZER ==========
def process_direct_summarizer():
    """Interface pour traiter directement un document LlamaParse avec le Summarizer"""
    if not UTILS_AVAILABLE:
        st.error("Les fonctions utilitaires ne sont pas disponibles")
        if st.button("← Annuler", key="cancel_direct_summarizer"):
            del st.session_state.processing_with_summarizer
            st.rerun()
        return
    
    data = st.session_state.processing_with_summarizer
    doc_name = data['doc_name']
    pages = data['pages']
    original_name = data['original_name']
    
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Annuler", key="cancel_direct_summarizer"):
            del st.session_state.processing_with_summarizer
            st.rerun()
    
    with col2:
        st.title(f"📊 Résumer : {original_name}")
        st.write(f"**Pages à traiter :** {len(pages)}")
    
    st.markdown("### Traitement avec l'agent Summarizer")
    st.info("Les pages ont déjà été extraites par LlamaParse. Le Summarizer va maintenant générer les résumés.")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    if st.button("🚀 Lancer le traitement Summarizer", key="start_direct_processing"):
        
        def update_progress(value):
            progress_bar.progress(value)
        
        def update_status(message):
            status_text.text(message)
        
        status_text.text("Initialisation du Summarizer Agent...")
        progress_bar.progress(10)
        
        result = process_existing_pages_with_summarizer(
            pages, doc_name, update_progress, update_status
        )
        
        if result:
            summaries, output_path, success_count, error_count = result
            
            save_summarizer_document(doc_name, summaries, output_path, original_name, success_count, error_count)
            
            progress_bar.progress(100)
            status_text.text("Traitement terminé !")
            
            st.markdown("### Résultats du traitement")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.metric("Pages traitées", success_count)
                st.metric("Pages avec erreur", error_count)
                st.metric("Total pages", len(pages))
            
            with col2:
                with st.expander("Aperçu des résumés générés", expanded=True):
                    if summaries:
                        selected_page = st.selectbox(
                            "Sélectionner une page", 
                            range(1, len(summaries) + 1),
                            format_func=lambda x: f"Page {x}",
                            key="preview_summary_page"
                        )
                        
                        if selected_page:
                            summary_data = next((s for s in summaries if s.get('page') == selected_page), None)
                            
                            if summary_data and 'error' not in summary_data:
                                st.text(f"Page {selected_page}:")
                                st.text(f"Section : {summary_data.get('sectionTitle', 'N/A')}")
                                st.text(f"Résumé : {summary_data.get('pageSummary', 'N/A')}")
                                st.text(f"Continuation : {'Oui' if summary_data.get('isContinuation', False) else 'Non'}")
                            else:
                                st.error(f"Erreur sur la page {selected_page}: {summary_data.get('error', 'Erreur inconnue')}")
            
            if error_count > 0:
                st.warning(f"Document '{original_name}' traité avec {success_count}/{len(summaries)} pages réussies")
            else:
                st.success(f"✅ Document '{original_name}' entièrement traité avec succès et ajouté à la sidebar!")
            
            if st.button("✅ Terminer", key="finish_direct_processing"):
                del st.session_state.processing_with_summarizer
                st.rerun()
        else:
            st.error("Échec du traitement. Vérifiez les logs ci-dessus.")
            if st.button("🔄 Réessayer", key="retry_direct_processing"):
                st.rerun()

# ========== VISUALISATEUR DE DOCUMENTS ==========
def show_document_viewer():
    """Affiche le visualisateur de document"""
    if not UTILS_AVAILABLE:
        st.error("Les fonctions utilitaires ne sont pas disponibles")
        if st.button("← Retour", key="back_from_page_error"):
            del st.session_state.viewing_page
            st.rerun()
        return
    
    page_data = st.session_state.viewing_page
    doc_name = page_data['doc_name']
    current_page = page_data['page_num']
    doc_type = page_data.get('type', 'llamaparse')
    
    # Récupérer les données
    if doc_type == 'summarizer':
        processed_docs = get_summarizer_documents()
        doc_data = processed_docs.get(doc_name, {})
        total_pages = len(doc_data.get('summaries', []))
        content_key = 'summaries'
    else:
        processed_docs = get_processed_documents()
        doc_data = processed_docs.get(doc_name, {})
        total_pages = len(doc_data.get('pages', []))
        content_key = 'pages'
    
    if not doc_data or not doc_data.get(content_key):
        st.error("Document non trouvé ou supprimé")
        if st.button("← Retour", key="back_from_missing_doc"):
            del st.session_state.viewing_page
            st.rerun()
        return
    
    # En-tête
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("← Retour", key="back_from_page"):
            del st.session_state.viewing_page
            st.rerun()
    
    with col2:
        if doc_type == 'summarizer':
            st.markdown(f"### 📊 {page_data['original_name']}")
            st.text(f"Résumé • Page {current_page} / {total_pages}")
        else:
            st.markdown(f"### 📄 {page_data['original_name']}")
            st.text(f"Document • Page {current_page} / {total_pages}")
    
    # Navigation
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])
    
    def navigate_to_page(target_page):
        if doc_type == 'summarizer':
            summary_data = next((s for s in doc_data['summaries'] if s.get('page') == target_page), None)
            content = summary_data
        else:
            content = doc_data['pages'][target_page - 1]
        
        st.session_state.viewing_page = {
            'doc_name': doc_name,
            'page_num': target_page,
            'content': content,
            'original_name': page_data['original_name'],
            'type': doc_type
        }
        st.rerun()
    
    with nav_col1:
        if current_page > 1 and st.button("⏮️", key="first_page"):
            navigate_to_page(1)
    
    with nav_col2:
        if current_page > 1 and st.button("⬅️", key="prev_page"):
            navigate_to_page(current_page - 1)
    
    with nav_col3:
        st.markdown(f"<div style='text-align: center;'>Page {current_page} sur {total_pages}</div>", unsafe_allow_html=True)
    
    with nav_col4:
        if current_page < total_pages and st.button("➡️", key="next_page"):
            navigate_to_page(current_page + 1)
    
    with nav_col5:
        if current_page < total_pages and st.button("⏭️", key="last_page"):
            navigate_to_page(total_pages)
    
    st.markdown("---")
    
    # Affichage du contenu
    if doc_type == 'summarizer':
        content = page_data['content']
        if 'error' in content:
            st.error("❌ Erreur de traitement")
            st.text(f"Erreur: {content.get('error', 'Erreur inconnue')}")
        else:
            st.text("📑 Section:")
            st.info(content.get('sectionTitle', 'N/A'))
            
            st.text("📝 Résumé de la page:")
            st.info(content.get('pageSummary', 'N/A'))
            
            st.text("🔗 Continuation:")
            if content.get('isContinuation', False):
                st.success("✅ Cette page continue la section précédente")
            else:
                st.info("🆕 Cette page commence une nouvelle section")
            
            with st.expander("🌐 Résumé global mis à jour"):
                st.text(content.get('updatedGlobalSummary', 'N/A')[:800])
    else:
        # Affichage pour LlamaParse
        content = page_data['content']
        st.text_area("Contenu de la page:", content, height=500, key=f"page_content_{current_page}")

# ========== MAIN ==========
def main():
    load_styles()
    sidebar()
    main_ui()

if __name__ == "__main__":
    main()
    
    
    
# utils/fonctions.py
import os
import re
import tempfile
import streamlit as st
from pathlib import Path
import sys
import json

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

# ========== CONFIGURATION ==========
PROCESSED_DIR = Path(__file__).parent.parent / "processed_documents"
PROCESSED_DIR.mkdir(exist_ok=True)

# ========== FONCTIONS UTILITAIRES LLAMAPARSE ==========

def extract_pages(text: str):
    """
    Extrait les pages en découpant sur chaque balise de fermeture </pageN>.
    """
    parts = re.split(r'</\s*page\s*\d+\s*>', text, flags=re.IGNORECASE)
    pages = []
    
    for part in parts:
        page = re.sub(r'<\s*page\s*\d+\s*>', '', part, flags=re.IGNORECASE).strip()
        if page:
            pages.append(page)
    
    return pages

def save_uploaded_file(uploaded_file):
    """Sauvegarde le fichier uploadé temporairement."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde du fichier : {e}")
        return None

def process_with_llamaparse(file_path, output_name):
    """Traite le fichier avec LlamaParse et retourne le contenu."""
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

def clean_filename(filename):
    """Nettoie le nom de fichier pour éviter les caractères problématiques."""
    clean_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    name_parts = clean_name.rsplit('.', 1)
    if len(name_parts) == 2:
        clean_name = name_parts[0].replace('.', '_') + '.' + name_parts[1]
    else:
        clean_name = clean_name.replace('.', '_')
    
    return clean_name

def format_file_size(size_bytes):
    """Formate la taille de fichier en unités lisibles."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_file_type(filename, allowed_types=None):
    """Valide le type de fichier."""
    if allowed_types is None:
        allowed_types = ['.pdf', '.docx', '.txt', '.doc']
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_types

def get_file_info(uploaded_file):
    """Extrait les informations du fichier uploadé."""
    return {
        "nom": uploaded_file.name,
        "taille": format_file_size(uploaded_file.size),
        "taille_bytes": uploaded_file.size,
        "type": uploaded_file.type,
        "extension": Path(uploaded_file.name).suffix.lower(),
        "nom_propre": clean_filename(uploaded_file.name)
    }

def cleanup_temp_file(file_path):
    """Supprime un fichier temporaire en toute sécurité."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception:
        pass

def save_processed_document(doc_name, pages, file_path, original_name):
    """Sauvegarde un document traité dans le session state."""
    if 'processed_documents' not in st.session_state:
        st.session_state.processed_documents = {}
    
    st.session_state.processed_documents[doc_name] = {
        'pages': pages,
        'file_path': str(file_path),
        'original_name': original_name,
        'num_pages': len(pages),
        'processed_at': str(Path().resolve())
    }

def get_processed_documents():
    """Récupère la liste des documents traités."""
    return st.session_state.get('processed_documents', {})

def delete_processed_document(doc_name):
    """Supprime un document traité du session state."""
    if 'processed_documents' in st.session_state and doc_name in st.session_state.processed_documents:
        doc_data = st.session_state.processed_documents[doc_name]
        file_path = doc_data.get('file_path')
        if file_path and os.path.exists(file_path):
            cleanup_temp_file(file_path)
        
        del st.session_state.processed_documents[doc_name]

def delete_page_from_document(doc_name, page_index):
    """Supprime une page spécifique d'un document traité."""
    if 'processed_documents' in st.session_state and doc_name in st.session_state.processed_documents:
        doc_data = st.session_state.processed_documents[doc_name]
        pages = doc_data['pages']
        
        if 0 <= page_index < len(pages):
            pages.pop(page_index)
            st.session_state.processed_documents[doc_name]['num_pages'] = len(pages)
            
            if len(pages) == 0:
                delete_processed_document(doc_name)

def get_page_statistics(pages):
    """Calcule des statistiques sur les pages."""
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

def process_with_summarizer(pages, doc_name, progress_callback=None, status_callback=None):
    """Traite les pages avec le Summarizer Agent"""
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
            return summaries, output_path, success_count, error_count
        else:
            return None
            
    except Exception as e:
        st.error(f"Erreur lors du traitement avec Summarizer : {e}")
        return None

def save_summarizer_document(doc_name, summaries, file_path, original_name, success_count, error_count):
    """Sauvegarde un document traité par le Summarizer dans le session state."""
    if 'summarizer_documents' not in st.session_state:
        st.session_state.summarizer_documents = {}
    
    st.session_state.summarizer_documents[doc_name] = {
        'summaries': summaries,
        'file_path': str(file_path),
        'original_name': original_name,
        'num_pages': len(summaries),
        'success_count': success_count,
        'error_count': error_count,
        'processed_at': str(Path().resolve())
    }

def get_summarizer_documents():
    """Récupère la liste des documents traités par le Summarizer."""
    return st.session_state.get('summarizer_documents', {})

def delete_summarizer_document(doc_name):
    """Supprime un document traité par le Summarizer du session state."""
    if 'summarizer_documents' in st.session_state and doc_name in st.session_state.summarizer_documents:
        doc_data = st.session_state.summarizer_documents[doc_name]
        file_path = doc_data.get('file_path')
        if file_path and os.path.exists(file_path):
            cleanup_temp_file(file_path)
        
        del st.session_state.summarizer_documents[doc_name]

def process_existing_pages_with_summarizer(pages, doc_name, progress_callback=None, status_callback=None):
    """Traite directement des pages déjà extraites avec le Summarizer Agent"""
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
    
    
# utils/vulnerability_analyzer.py
import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st

# Charger les variables d'environnement
load_dotenv()
llm_key = os.getenv("llm_key")

def analyze_vulnerabilities(raw_pages, summaries, progress_callback=None, status_callback=None):
    """
    Analyse les vulnérabilités dans les documents en utilisant les pages brutes et les résumés
    
    Args:
        raw_pages (list): Liste des pages extraites par LlamaParse
        summaries (list): Liste des résumés générés par Summary Agent
        progress_callback: Fonction pour mettre à jour la progression
        status_callback: Fonction pour afficher le statut
    
    Returns:
        list: Liste des vulnérabilités détectées pour chaque page
    """
    
    if not llm_key:
        st.error("Clé API LLM non configurée dans le fichier .env")
        return []
    
    results = []
    total_pages = max(len(raw_pages), len(summaries))
    
    for idx in range(total_pages):
        # Calculer la progression
        if progress_callback:
            progress = int(((idx + 1) / total_pages) * 100)
            progress_callback(progress)
        
        if status_callback:
            status_callback(f"Analyse de la page {idx + 1}/{total_pages}")
        
        # Récupérer le contenu de la page
        page_content = raw_pages[idx] if idx < len(raw_pages) else ""
        
        # Récupérer le résumé de la page
        if idx < len(summaries):
            summary_data = summaries[idx] if isinstance(summaries[idx], dict) else {}
            page_summary = summary_data.get("pageSummary", "")
            global_summary = summary_data.get("updatedGlobalSummary", "")
            section_title = summary_data.get("sectionTitle", "")
            is_continuation = summary_data.get("isContinuation", False)
            
            # Pour la première page, utiliser le résumé de la page elle-même
            if idx == 0:
                last_page_summary = page_summary
            else:
                # Sinon, utiliser le résumé de la page précédente
                prev_summary = summaries[idx-1] if idx > 0 and idx-1 < len(summaries) else {}
                last_page_summary = prev_summary.get("pageSummary", "") if isinstance(prev_summary, dict) else ""
        else:
            page_summary = ""
            global_summary = ""
            section_title = ""
            last_page_summary = ""
            is_continuation = False
        
        # Construction du prompt pour l'analyse des vulnérabilités
        prompt = """
Un **risque projet** est un événement futur incertain ayant un impact négatif sur les objectifs du projet (qualité, coût, délai).

---

##  Définitions fondamentales (à appliquer strictement) :

- **Élément vulnérable** : une composante du projet (ressource, activité, livrable, organisation, infrastructure…) qui, en raison de sa **fragilité**, **complexité**, ou **dépendance**, peut être affectée par une menace.  
   Il peut être fragilisé ou perturber le projet s’il est attaqué ou perturbé.

- **Menace** : un événement, facteur interne ou externe, qui pourrait **exploiter une vulnérabilité** pour provoquer un dommage.  
   Elle **agit sur un élément vulnérable**.

- **Conséquence** : l’impact que cela aurait sur les **objectifs du projet** (délai, coût, qualité).

- **Risque** : une **formulation logique complète** qui relie un élément vulnérable, une menace précise, et un impact.

---

##  Contexte de travail – Analyse page par page :

Tu vas analyser un **document de projet très long**.  
Tu dois donc travailler **page par page**, mais en gardant **la cohérence avec ce qui a déjà été traité auparavant**.

Tu reçois les informations suivantes à chaque étape :

- {globalSummary} : résumé cumulé des pages précédentes → il t’aide à ne **pas répéter** des éléments déjà identifiés.
- {lastPageSummary} : résumé détaillé de la dernière page analysée → pour rester dans le même fil logique.
- {pageContent} : contenu de la **page actuelle** à analyser.

 **Important** :
- Tu ne dois **jamais extraire deux fois** un même élément vulnérable ou une menace déjà citée dans les pages précédentes.
- Tu ne dois analyser **que le contenu de la page actuelle** (`pageContent`), en tenant compte du fil conducteur (`globalSummary` et `lastPageSummary`).
-Tu ne dois Extraire que les éléments qui sont **concrets, spécifiques et sensibles** qui peuvent impacter significativement le projet.

---

##  Objectif

Ta mission est structurée en deux étapes :

---

###  Étape 1 — Identifier les **éléments vulnérables** présents dans la page

- Ne garde que ceux qui sont **concrets, spécifiques, sensibles**, liés à des **ressources, activités, contraintes ou installations**.
- Chaque élément vulnérable doit être **justifié** par un **extrait** ou une **paraphrase du document**, avec une explication claire de **sa vulnérabilité**.

 **Format attendu** :
- Élément vulnérable : [nom synthétique]
  Justification : [extrait ou paraphrase + explication du pourquoi cet élément est fragile]

---

###  Étape 2 — Associer une ou plusieurs **menaces** à chaque élément vulnérable

- Pour chaque élément, propose **au moins une menace potentielle** qui pourrait l’exploiter.
- La menace peut venir :
  - d’un facteur externe (climat, acteur tiers, accident),
  - ou d’un facteur interne (erreur humaine, défaillance technique, etc.).

**Format attendu** :
- Élément vulnérable : [nom]
  Menace associée : [description claire]
  Justification : [lien logique entre menace et vulnérabilité]

---

##  ATTENTION :
ASSURE TOI:
- Toutes les **menaces** sont reliées à un **élément vulnérable clair**,
- Aucun élément n’est **vague ou redondant** avec ceux déjà dans `globalSummary`,
- Tu restes **strictement lié au contenu de la page actuelle**, avec le contexte en soutien, mais sans extrapolation excessive.
-REPOND EN FORMAT JSON BIEN STRUCTURÉ
Page 1
Étape 1 — Identifier les éléments vulnérables
Élément vulnérable : Planification tardive des autorisations administratives
Justification : Le document indique que « les demandes de permis de construire ont été déposées 3 mois après le démarrage de la phase de fondations » → le décalage entre mise en chantier et obtention des autorisations expose le projet à un arrêt des travaux si les délais réglementaires ne sont pas respectés.

Élément vulnérable : Budget de finition trop serré
Justification : « Le budget alloué aux finitions (peintures, revêtements de sol, équipements sportifs) représente seulement 5 % du coût total du projet » → cette marge réduite limite la flexibilité en cas de hausse des prix ou d’ajout de spécifications.

Élément vulnérable : Dépendance à un unique fournisseur de structure métallique
Justification : « Le prestataire X détient l’exclusivité de la charpente en acier » → toute défaillance ou retard de ce fournisseur bloque l’avancement des gros-œuvre.

Élément vulnérable : Coordination inter-équipes insuffisante
Justification : « Trois entreprises distinctes interviennent sur les réseaux, la maçonnerie et la charpente, sans réunion de synchronisation hebdomadaire » → ce manque de communication peut conduire à des conflits de planning et des malfaçons.

Étape 2 — Associer des menaces à chaque élément vulnérable
Élément vulnérable : Planification tardive des autorisations administratives
Menace associée : Blocage réglementaire des fondations
Justification : Si l’administration tarde à délivrer les permis, la direction des travaux doit suspendre les opérations de terrassement, générant des coûts de remobilisation et des retards sur l’ensemble du planning.

Élément vulnérable : Budget de finition trop serré
Menace associée : Dépassement des coûts de matériaux
Justification : Une inflation de 10 % sur les peintures et revêtements non prévue dans l’estimation initiale épuisera la ligne budgétaire, forçant à des arbitrages qui pourraient dégrader la qualité du centre sportif.

Élément vulnérable : Dépendance à un unique fournisseur de structure métallique
Menace associée : Rupture de stock ou faillite du fournisseur
Justification : Si le fournisseur X rencontre des difficultés (grève, insolvabilité), il devient impossible d’avancer sur la charpente, entraînant un retard en cascade sur les corps d’état secondaires (couverture, étanchéité).

Élément vulnérable : Coordination inter-équipes insuffisante
Menace associée : Conflits de planning et malfaçons
Justification : L’absence de réunions de coordination hebdomadaires peut conduire à des chevauchements de tâches (ex. : pose d’un réseau encastré avant coulage du dallage), nécessitant des reprises coûteuses et allongeant le délai global.

Souviens-toi : tu travailles **page par page**, en évitant les redites, et en construisant une analyse **cumulative, progressive et logique**.
"""
        
        # Appeler l'API LLM
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {llm_key}", 
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                    "temperature": 0.4,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content']
            
            results.append({
                'page': idx + 1,
                'analysis': result,
                'section': section_title,
                'has_content': bool(page_content),
                'has_summary': bool(page_summary)
            })
            
        except requests.RequestException as e:
            results.append({
                'page': idx + 1,
                'error': f"Erreur API: {e}",
                'section': section_title,
                'has_content': bool(page_content),
                'has_summary': bool(page_summary)
            })
        except KeyError as e:
            results.append({
                'page': idx + 1,
                'error': f"Erreur de format: {e}",
                'section': section_title,
                'has_content': bool(page_content),
                'has_summary': bool(page_summary)
            })
        except Exception as e:
            results.append({
                'page': idx + 1,
                'error': f"Erreur inattendue: {e}",
                'section': section_title,
                'has_content': bool(page_content),
                'has_summary': bool(page_summary)
            })
    
    if status_callback:
        status_callback("Analyse terminée!")
    
    return results

def save_vulnerability_report(results, output_path):
    """
    Sauvegarde le rapport de vulnérabilités
    
    Args:
        results (list): Résultats de l'analyse
        output_path (str/Path): Chemin du fichier de sortie
    
    Returns:
        bool: True si sauvegarde réussie
    """
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Rapport d'Analyse des Vulnérabilités\n\n")
            
            for result in results:
                f.write(f"---\n\n")
                f.write(f"## Page {result['page']}\n\n")
                
                if 'error' in result:
                    f.write(f"**Erreur:** {result['error']}\n\n")
                else:
                    f.write(f"**Section:** {result.get('section', 'N/A')}\n\n")
                    f.write(f"**Analyse:**\n{result.get('analysis', 'Aucune analyse disponible')}\n\n")
                
                f.write(f"**Données disponibles:**\n")
                f.write(f"- Contenu brut: {'✅' if result.get('has_content') else '❌'}\n")
                f.write(f"- Résumé: {'✅' if result.get('has_summary') else '❌'}\n\n")
        
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde du rapport: {e}")
        return False

def display_vulnerability_results(results):
    """
    Affiche les résultats de l'analyse de vulnérabilités dans Streamlit
    
    Args:
        results (list): Résultats de l'analyse
    """
    
    # Statistiques générales
    total_pages = len(results)
    pages_with_errors = sum(1 for r in results if 'error' in r)
    pages_analyzed = total_pages - pages_with_errors
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pages analysées", pages_analyzed)
    with col2:
        st.metric("Erreurs", pages_with_errors)
    with col3:
        st.metric("Total", total_pages)
    
    # Affichage détaillé
    for result in results:
        page_num = result.get('page', 0)
        
        with st.expander(f"📄 Page {page_num} - {result.get('section', 'Sans titre')}", expanded=False):
            if 'error' in result:
                st.error(f"Erreur: {result['error']}")
            else:
                analysis = result.get('analysis', 'Aucune analyse disponible')
                
                # Parser l'analyse pour une meilleure présentation
                lines = analysis.split('\n')
                for line in lines:
                    if 'VULNÉRABILITÉS' in line:
                        st.markdown(f"### 🔍 {line}")
                    elif 'NIVEAU DE RISQUE' in line:
                        if 'Critique' in line or 'Élevé' in line:
                            st.error(line)
                        elif 'Moyen' in line:
                            st.warning(line)
                        else:
                            st.info(line)
                    elif 'RECOMMANDATIONS' in line:
                        st.markdown(f"### 💡 {line}")
                    else:
                        st.text(line)
            
            # Informations sur les données disponibles
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if result.get('has_content'):
                    st.success("✅ Contenu brut disponible")
                else:
                    st.error("❌ Contenu brut manquant")
            with col2:
                if result.get('has_summary'):
                    st.success("✅ Résumé disponible")
                else:
                    st.error("❌ Résumé manquant")