# src/app.py
import streamlit as st
from pathlib import Path
import base64
import sys
import json
import re

# ========== CONFIG (DOIT ÊTRE EN PREMIER) ==========
st.set_page_config(
    page_title="Risk Analyst Hub", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Ajouter le chemin vers les modules
sys.path.append(str(Path(__file__).parent))

# Initialiser les variables globales
UTILS_AVAILABLE = False

# Fonctions de fallback si les modules ne sont pas disponibles
def get_processed_documents():
    return st.session_state.get('processed_documents', {})

def get_summarizer_documents():
    return st.session_state.get('summarizer_documents', {})

def delete_processed_document(doc_name):
    if 'processed_documents' in st.session_state and doc_name in st.session_state.processed_documents:
        del st.session_state.processed_documents[doc_name]

def delete_summarizer_document(doc_name):
    if 'summarizer_documents' in st.session_state and doc_name in st.session_state.summarizer_documents:
        del st.session_state.summarizer_documents[doc_name]

def save_processed_document(doc_name, pages, file_path, original_name):
    if 'processed_documents' not in st.session_state:
        st.session_state.processed_documents = {}
    st.session_state.processed_documents[doc_name] = {
        'pages': pages,
        'file_path': str(file_path),
        'original_name': original_name,
        'num_pages': len(pages),
        'type': 'llamaparse'
    }

def save_summarizer_document(doc_name, summaries, file_path, original_name, success_count, error_count):
    if 'summarizer_documents' not in st.session_state:
        st.session_state.summarizer_documents = {}
    st.session_state.summarizer_documents[doc_name] = {
        'summaries': summaries,
        'file_path': str(file_path),
        'original_name': original_name,
        'num_pages': len(summaries),
        'success_count': success_count,
        'error_count': error_count,
        'type': 'summarizer'
    }

# Fonctions de fallback pour les autres fonctions nécessaires
def extract_pages(text):
    parts = re.split(r'</\s*page\s*\d+\s*>', text, flags=re.IGNORECASE)
    pages = []
    for part in parts:
        page = re.sub(r'<\s*page\s*\d+\s*>', '', part, flags=re.IGNORECASE).strip()
        if page:
            pages.append(page)
    return pages or [text] if text else []

def save_uploaded_file(uploaded_file):
    return None

def process_with_llamaparse(file_path, doc_name):
    return None

def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)[:50]

def get_file_info(uploaded_file):
    return {"nom": uploaded_file.name}

def cleanup_temp_file(file_path):
    pass

def delete_page_from_document(doc_name, page_index):
    return False

def get_page_statistics(pages):
    return {}

def process_with_summarizer(pages, doc_name):
    return None

def process_existing_pages_with_summarizer(pages, doc_name):
    return None

# Importer les fonctions utilitaires
try:
    from srcc.utils.function import (
        extract_pages as _extract_pages,
        save_uploaded_file as _save_uploaded_file,
        process_with_llamaparse as _process_with_llamaparse,
        clean_filename as _clean_filename,
        get_file_info as _get_file_info,
        cleanup_temp_file as _cleanup_temp_file,
        save_processed_document as _save_processed_document,
        get_processed_documents as _get_processed_documents,
        delete_processed_document as _delete_processed_document,
        delete_page_from_document as _delete_page_from_document,
        get_page_statistics as _get_page_statistics,
        process_with_summarizer as _process_with_summarizer,
        save_summarizer_document as _save_summarizer_document,
        get_summarizer_documents as _get_summarizer_documents,
        delete_summarizer_document as _delete_summarizer_document,
        process_existing_pages_with_summarizer as _process_existing_pages_with_summarizer
    )
    # Remplacer les fonctions de fallback par les vraies
    extract_pages = _extract_pages
    save_uploaded_file = _save_uploaded_file
    process_with_llamaparse = _process_with_llamaparse
    clean_filename = _clean_filename
    get_file_info = _get_file_info
    cleanup_temp_file = _cleanup_temp_file
    save_processed_document = _save_processed_document
    get_processed_documents = _get_processed_documents
    delete_processed_document = _delete_processed_document
    delete_page_from_document = _delete_page_from_document
    get_page_statistics = _get_page_statistics
    process_with_summarizer = _process_with_summarizer
    save_summarizer_document = _save_summarizer_document
    get_summarizer_documents = _get_summarizer_documents
    delete_summarizer_document = _delete_summarizer_document
    process_existing_pages_with_summarizer = _process_existing_pages_with_summarizer
    UTILS_AVAILABLE = True
except ImportError as e:
    st.error(f"Erreur d'importation: {e}")
    UTILS_AVAILABLE = False

# Configuration des chemins
STATIC_DIR = Path(__file__).parent / "static"
PROCESSED_DIR = Path(__file__).parent.parent / "processed_documents"

# ========== STYLES CSS GLOBAUX ==========
def load_global_styles():
    st.markdown("""
    <style>
    /* Styles améliorés pour la navigation */
    .agent-workflow {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        border: 2px solid #e9ecef;
    }
    
    .workflow-steps {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 20px 0;
    }
    
    .workflow-step {
        text-align: center;
        flex: 1;
        padding: 15px;
        border-radius: 8px;
        background: white;
        margin: 0 5px;
        border: 2px solid #dee2e6;
        transition: all 0.3s ease;
    }
    
    .workflow-step.active {
        border-color: #007bff;
        background: #007bff;
        color: white;
        transform: scale(1.05);
    }
    
    .workflow-step.completed {
        border-color: #28a745;
        background: #28a745;
        color: white;
    }
    
    .step-number {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .step-title {
        font-size: 0.9em;
        font-weight: bold;
    }
    
    .workflow-connector {
        flex: 0.1;
        text-align: center;
        color: #6c757d;
        font-size: 1.5em;
    }
    
    /* Amélioration des cartes d'agents */
    .agent-card-enhanced {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .agent-card-enhanced:hover {
        border-color: #007bff;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,123,255,0.1);
    }
    
    .agent-card-enhanced.active {
        border-color: #007bff;
        background: #f8fbff;
    }
    
    .agent-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .agent-icon {
        font-size: 2em;
        margin-right: 15px;
    }
    
    .agent-status {
        margin-top: 10px;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    .status-ready {
        background: #d4edda;
        color: #155724;
    }
    
    .status-pending {
        background: #fff3cd;
        color: #856404;
    }
    
    /* Styles PDF améliorés */
    /* .pdf-viewer supprimé pour fond blanc pur */
    
    .pdf-page {
        background: white;
        width: 900px;
        min-height: 600px;
        padding: 32px 24px 48px 24px;
        margin: 0 auto 24px auto;
        box-shadow: 0 0 10px rgba(0,0,0,0.08);
        font-family: 'Times New Roman', serif;
        font-size: 15px;
        line-height: 1.7;
        color: #000;
        position: relative;
    }
    
    .pdf-content {
        font-family: 'Times New Roman', serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #000;
    }
    
    .pdf-content h1, .pdf-content h2, .pdf-content h3 {
        color: #000;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .pdf-content p {
        margin-bottom: 10px;
        text-align: justify;
    }
    
    .page-number {
        position: absolute;
        bottom: 20mm;
        right: 20mm;
        font-size: 10pt;
        color: #666;
    }
    
    .pdf-header {
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .pdf-title {
        font-size: 18pt;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .pdf-subtitle {
        font-size: 11pt;
        color: #666;
    }
    
    /* Navigation PDF */
    .pdf-navigation {
        background: #2c2f33;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    
    .pdf-nav-button {
        background: #5865f2;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 3px;
        cursor: pointer;
        transition: background 0.3s;
    }
    
    .pdf-nav-button:hover {
        background: #4752c4;
    }
    
    .pdf-nav-button:disabled {
        background: #40444b;
        cursor: not-allowed;
    }
    
    .page-indicator {
        color: white;
        font-weight: bold;
        padding: 0 15px;
    }
    
    /* Nettoyage du markdown */
    .clean-markdown {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    .clean-markdown code {
        background: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: monospace;
    }
    
    .clean-markdown pre {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
    }
    
    /* Styles pour l'agent Vulnerability */
    .vulnerability-card {
        background: #f8f9fa;
        border-left: 4px solid #dc3545;
        padding: 15px;
        margin: 15px 0;
        border-radius: 0 5px 5px 0;
    }
    
    .vulnerability-title {
        font-weight: bold;
        color: #dc3545;
        margin-bottom: 10px;
    }
    
    .threat-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 15px 0;
        border-radius: 0 5px 5px 0;
    }
    
    .threat-title {
        font-weight: bold;
        color: #856404;
        margin-bottom: 10px;
    }
    
    /* Réduire padding dans la sidebar */
    .css-1d391kg {
        padding: 1rem 0.5rem;
    }
    
    /* Cards compactes dans la sidebar */
    .sidebar-card {
        background: #f0f2f6;
        padding: 8px;
        margin: 5px 0;
        border-radius: 5px;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

def load_styles():
    load_global_styles()

# ========== FONCTIONS UTILITAIRES AMÉLIORÉES ==========
def clean_markdown_content(content):
    """Nettoie le contenu markdown des balises indésirables"""
    if not content:
        return ""
    
    # Si c'est une chaîne de caractères
    if isinstance(content, str):
        # Supprimer les blocs de code markdown
        content = re.sub(r'```json\s*\{.*?\}\s*```', '', content, flags=re.DOTALL)
        content = re.sub(r'```\w*\s*', '', content)
        
        # Nettoyer les retours à la ligne multiples
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # Échapper le HTML pour sécurité
        content = content.replace('<', '&lt;').replace('>', '&gt;')
    
    return content

# ========== SIDEBAR CORRIGÉE ==========
def sidebar():
    """Sidebar compacte pour la navigation"""
    with st.sidebar:
        st.markdown("### 🎯 Risk Analyst Hub")
        st.markdown("---")
        
        if UTILS_AVAILABLE:
            # Documents LlamaParse
            processed_docs = get_processed_documents()
            if processed_docs:
                st.markdown("**📄 Documents Extraits**")
                for doc_name, doc_data in processed_docs.items():
                    with st.expander(f"📄 {doc_data['original_name'][:20]}...", expanded=False):
                        st.text(f"Pages: {doc_data['num_pages']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("👁 Voir", key=f"view_{doc_name}"):
                                st.session_state.viewing_page = {
                                    'doc_name': doc_name,
                                    'page_num': 1,
                                    'content': doc_data['pages'][0] if doc_data['pages'] else "",
                                    'original_name': doc_data['original_name'],
                                    'type': 'llamaparse'
                                }
                                st.rerun()
                        with col2:
                            if st.button("🗑 Suppr", key=f"del_{doc_name}"):
                                delete_processed_document(doc_name)
                                st.rerun()
            
            # Documents Summarizer
            summarizer_docs = get_summarizer_documents()
            if summarizer_docs:
                st.markdown("**📊 Résumés Générés**")
                for doc_name, doc_data in summarizer_docs.items():
                    with st.expander(f"📊 {doc_data['original_name'][:20]}...", expanded=False):
                        st.text(f"✅ {doc_data['success_count']} / ❌ {doc_data['error_count']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("👁 Voir", key=f"view_s_{doc_name}"):
                                summary_data = doc_data['summaries'][0] if doc_data['summaries'] else {}
                                st.session_state.viewing_page = {
                                    'doc_name': doc_name,
                                    'page_num': 1,
                                    'content': summary_data,
                                    'original_name': doc_data['original_name'],
                                    'type': 'summarizer'
                                }
                                st.rerun()
                        with col2:
                            if st.button("🗑 Suppr", key=f"del_s_{doc_name}"):
                                delete_summarizer_document(doc_name)
                                st.rerun()
            
            # Documents Vulnerability
            if 'vulnerability_results' in st.session_state and st.session_state.vulnerability_results:
                vuln_docs = st.session_state.vulnerability_results
                if vuln_docs:
                    st.markdown("**🔍 Analyses de Vulnérabilités**")
                    for doc_name, doc_data in vuln_docs.items():
                        with st.expander(f"🔍 {doc_data['original_name'][:20]}...", expanded=False):
                            st.text(f"Pages: {doc_data['num_pages']}")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("👁 Voir", key=f"view_v_{doc_name}"):
                                    result_data = doc_data['results'][0] if doc_data['results'] else {}
                                    st.session_state.viewing_page = {
                                        'doc_name': doc_name,
                                        'page_num': 1,
                                        'content': result_data,
                                        'original_name': doc_data['original_name'],
                                        'type': 'vulnerability'
                                    }
                                    st.rerun()
                            with col2:
                                if st.button("🗑 Suppr", key=f"del_v_{doc_name}"):
                                    del st.session_state.vulnerability_results[doc_name]
                                    st.rerun()

# ========== WORKFLOW AMÉLIORÉ ==========
def show_workflow_navigation():
    """Affiche la navigation par workflow"""
    
    # État du workflow
    if 'workflow_step' not in st.session_state:
        st.session_state.workflow_step = 1  # 1: LlamaParse, 2: Summary, 3: Vulnerability
    
    steps = [
        {"number": 1, "title": "LlamaParse", "description": "Extraction du document", "icon": "📄"},
        {"number": 2, "title": "Summary", "description": "Résumé du contenu", "icon": "📊"},
        {"number": 3, "title": "Vulnerability", "description": "Analyse des risques", "icon": "🔍"}
    ]
    
    st.markdown('<div class="agent-workflow">', unsafe_allow_html=True)
    st.markdown("### 🚀 Workflow d'Analyse")
    st.markdown("Suivez les étapes pour analyser vos documents:")
    
    # Afficher les étapes
    st.markdown('<div class="workflow-steps">', unsafe_allow_html=True)
    
    for i, step in enumerate(steps):
        col1, col2 = st.columns([4, 1])
        with col1:
            status_class = ""
            if st.session_state.workflow_step == step["number"]:
                status_class = "active"
            elif st.session_state.workflow_step > step["number"]:
                status_class = "completed"
            
            st.markdown(f'''
            <div class="workflow-step {status_class}">
                <div class="step-number">{step["icon"]}</div>
                <div class="step-title">{step["title"]}</div>
                <div style="font-size:0.8em">{step["description"]}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            if i < len(steps) - 1:
                st.markdown('<div class="workflow-connector">→</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Boutons de navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.workflow_step > 1:
            if st.button("◀ Étape précédente", use_container_width=True):
                st.session_state.workflow_step -= 1
                st.session_state.selected_agent = steps[st.session_state.workflow_step - 1]["title"].lower()
                st.rerun()
    
    with col2:
        current_step = steps[st.session_state.workflow_step - 1]
        st.info(f"Étape {st.session_state.workflow_step}: {current_step['description']}")
    
    with col3:
        if st.session_state.workflow_step < len(steps):
            if st.button("Étape suivante ▶", use_container_width=True):
                # Vérifier si l'étape actuelle est complétée
                if is_step_completed(st.session_state.workflow_step):
                    st.session_state.workflow_step += 1
                    st.session_state.selected_agent = steps[st.session_state.workflow_step - 1]["title"].lower()
                    st.rerun()
                else:
                    st.warning("Veuillez compléter l'étape actuelle avant de continuer.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def is_step_completed(step_number):
    """Vérifie si une étape du workflow est complétée"""
    if step_number == 1:  # LlamaParse
        return len(get_processed_documents()) > 0
    elif step_number == 2:  # Summary
        return len(get_summarizer_documents()) > 0
    elif step_number == 3:  # Vulnerability
        return 'vulnerability_results' in st.session_state and bool(st.session_state.vulnerability_results)
    return False

# ========== FONCTIONS DE TRAITEMENT ==========
def process_llamaparse_agent(uploaded_file):
    """Traite le fichier avec LlamaParse"""
    if not UTILS_AVAILABLE:
        st.error("Modules non disponibles")
        return
        
    if uploaded_file is not None:
        file_info = get_file_info(uploaded_file)
        
        with st.spinner("Traitement en cours..."):
            temp_file = save_uploaded_file(uploaded_file)
            if not temp_file:
                return
            
            doc_name = clean_filename(uploaded_file.name).replace('.', '_')
            result = process_with_llamaparse(temp_file, doc_name)
            
            if result:
                full_text, output_path = result
                pages = extract_pages(full_text)
                save_processed_document(doc_name, pages, output_path, uploaded_file.name)
                
                st.success(f"✅ Document traité: {len(pages)} pages extraites")
                
                # Bouton pour voir en PDF
                if st.button("📖 Voir le document", key="view_llama_pdf"):
                    st.session_state.viewing_page = {
                        'doc_name': doc_name,
                        'page_num': 1,
                        'content': pages[0] if pages else "",
                        'original_name': uploaded_file.name,
                        'type': 'llamaparse'
                    }
                    st.rerun()
            
            cleanup_temp_file(temp_file)

def process_summary_agent(uploaded_file):
    """Traite le fichier avec Summary Agent - Version améliorée"""
    if not UTILS_AVAILABLE:
        st.error("❌ Modules non disponibles")
        return
        
    if uploaded_file is not None:
        with st.spinner("🔄 Traitement en cours avec Summary Agent..."):
            # Barre de progression
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            temp_file = save_uploaded_file(uploaded_file)
            if not temp_file:
                return
            
            doc_name = clean_filename(uploaded_file.name).replace('.', '_')
            
            # Étape 1: LlamaParse
            status_text.text("📄 Extraction du contenu avec LlamaParse...")
            llamaparse_result = process_with_llamaparse(temp_file, doc_name)
            progress_bar.progress(30)
            
            if llamaparse_result:
                full_text, _ = llamaparse_result
                pages = extract_pages(full_text)
                
                if pages:
                    # Étape 2: Summarizer
                    status_text.text("📊 Génération des résumés...")
                    result = process_with_summarizer(pages, doc_name)
                    progress_bar.progress(80)
                    
                    if result:
                        summaries, output_path, success_count, error_count = result
                        save_summarizer_document(doc_name, summaries, output_path, uploaded_file.name, success_count, error_count)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Traitement terminé!")
                        
                        st.success(f"""
                        **Résumé du traitement:**
                        - 📄 Pages traitées: {success_count}
                        - ⚠️ Erreurs: {error_count}
                        - 💾 Document sauvegardé
                        """)
                        
                        # Bouton pour voir les résultats
                        if summaries:
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("📖 Voir les résumés", use_container_width=True):
                                    st.session_state.viewing_page = {
                                        'doc_name': doc_name,
                                        'page_num': 1,
                                        'content': summaries[0],
                                        'original_name': uploaded_file.name,
                                        'type': 'summarizer'
                                    }
                                    st.rerun()
                            with col2:
                                if st.button("➡️ Passer à l'analyse des vulnérabilités", use_container_width=True):
                                    st.session_state.workflow_step = 3
                                    st.session_state.selected_agent = "vulnerability"
                                    st.rerun()
            
            cleanup_temp_file(temp_file)

def process_vulnerability_agent():
    """Traite les documents avec l'agent Vulnerability avec affichage PDF corrigé"""
    st.markdown("### 🔍 Agent Vulnerability and Threat")
    
    llama_docs = get_processed_documents() if UTILS_AVAILABLE else {}
    summary_docs = get_summarizer_documents() if UTILS_AVAILABLE else {}
    
    if not llama_docs and not summary_docs:
        st.warning("Aucun document disponible. Veuillez d'abord traiter un document.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Documents LlamaParse")
        selected_llama = st.selectbox(
            "Sélectionner:", 
            options=["Aucun"] + list(llama_docs.keys()),
            format_func=lambda x: llama_docs[x]['original_name'] if x != "Aucun" and x in llama_docs else x,
            key=f"vuln_llama_select_{id(llama_docs)}"
        )
    
    with col2:
        st.markdown("#### Documents Summary")
        selected_summary = st.selectbox(
            "Sélectionner:", 
            options=["Aucun"] + list(summary_docs.keys()),
            format_func=lambda x: summary_docs[x]['original_name'] if x != "Aucun" and x in summary_docs else x,
            key=f"vuln_summary_select_{id(summary_docs)}"
        )
    
    if st.button("🔍 Analyser les vulnérabilités", type="primary"):
        if selected_llama == "Aucun" and selected_summary == "Aucun":
            st.error("Veuillez sélectionner au moins un document")
        else:
            with st.spinner("Analyse en cours..."):
                raw_pages = []
                summaries = []
                
                if selected_llama != "Aucun":
                    raw_pages = llama_docs[selected_llama]['pages']
                
                if selected_summary != "Aucun":
                    summaries = summary_docs[selected_summary]['summaries']
                
                try:
                    from utils.vulnerability_analyzer import analyze_vulnerabilities
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(value):
                        progress_bar.progress(value / 100)
                    
                    def update_status(message):
                        status_text.text(message)
                    
                    results = analyze_vulnerabilities(
                        raw_pages, summaries, 
                        update_progress, update_status
                    )
                    
                    if results:
                        # CORRECTION: Créer des pages structurées pour l'affichage
                        formatted_results = []
                        
                        for i, result in enumerate(results):
                            # Structurer chaque résultat comme une page
                            page_data = {
                                'page_number': i + 1,
                                'section': result.get('section', f'Section {i+1}'),
                                'analysis': result.get('analysis', ''),
                                'vulnerabilities': extract_vulnerabilities_from_analysis(result.get('analysis', '')),
                                'threats': extract_threats_from_analysis(result.get('analysis', ''))
                            }
                            formatted_results.append(page_data)
                        
                        # Sauvegarder les résultats formatés
                        doc_name = f"vuln_{selected_llama}_{selected_summary}"
                        if 'vulnerability_results' not in st.session_state:
                            st.session_state.vulnerability_results = {}
                        
                        st.session_state.vulnerability_results[doc_name] = {
                            'results': formatted_results,
                            'original_name': f"Vulnérabilités - {llama_docs[selected_llama]['original_name'] if selected_llama != 'Aucun' else summary_docs[selected_summary]['original_name']}",
                            'num_pages': len(formatted_results)
                        }
                        
                        st.success(f"✅ Analyse terminée! {len(formatted_results)} pages analysées")
                        
                        # Bouton pour voir les résultats
                        if st.button("📖 Voir les résultats en mode PDF", key="view_vuln_pdf"):
                            st.session_state.viewing_page = {
                                'doc_name': doc_name,
                                'page_num': 1,
                                'content': formatted_results[0] if formatted_results else {},
                                'original_name': st.session_state.vulnerability_results[doc_name]['original_name'],
                                'type': 'vulnerability'
                            }
                            st.rerun()
                    
                except ImportError as e:
                    st.error(f"Module vulnerability_analyzer non disponible: {e}")
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse: {e}")

def extract_vulnerabilities_from_analysis(analysis):
    """Extrait les vulnérabilités de l'analyse de manière robuste"""
    vulnerabilities = []
    
    try:
        # Méthodes multiples d'extraction du JSON
        json_str = None
        
        if '```json' in analysis:
            json_str = analysis.split('```json')[1].split('```')[0].strip()
        elif '```' in analysis:
            parts = analysis.split('```')
            if len(parts) >= 2:
                json_str = parts[1].strip()
        
        # Si pas de blocs de code, chercher directement du JSON
        if not json_str:
            brace_start = analysis.find('{')
            brace_end = analysis.rfind('}')
            if brace_start != -1 and brace_end != -1:
                json_str = analysis[brace_start:brace_end+1]
        
        if json_str:
            data = json.loads(json_str)
            
            # Chercher les vulnérabilités avec différentes clés possibles
            for key in data.keys():
                key_lower = key.lower().replace(' ', '').replace('_', '')
                if key_lower in ['etape1', 'étape1', 'step1', 'vulnerabilities', 'vulnérabilités']:
                    if isinstance(data[key], list):
                        vulnerabilities = data[key]
                        break
                        
    except Exception as e:
        # En cas d'erreur, chercher dans le texte brut
        lines = analysis.split('\n')
        current_vuln = {}
        
        for line in lines:
            line = line.strip()
            if 'Élément_vulnérable' in line or 'Élément vulnérable' in line:
                if current_vuln:
                    vulnerabilities.append(current_vuln)
                current_vuln = {'Élément_vulnérable': line.split(':')[-1].strip()}
            elif 'Justification' in line and current_vuln:
                current_vuln['Justification'] = line.split(':')[-1].strip()
        
        if current_vuln:
            vulnerabilities.append(current_vuln)
    
    return vulnerabilities

def extract_threats_from_analysis(analysis):
    """Extrait les menaces de l'analyse de manière robuste"""
    threats = []
    
    try:
        # Méthodes multiples d'extraction du JSON
        json_str = None
        
        if '```json' in analysis:
            json_str = analysis.split('```json')[1].split('```')[0].strip()
        elif '```' in analysis:
            parts = analysis.split('```')
            if len(parts) >= 2:
                json_str = parts[1].strip()
        
        if not json_str:
            brace_start = analysis.find('{')
            brace_end = analysis.rfind('}')
            if brace_start != -1 and brace_end != -1:
                json_str = analysis[brace_start:brace_end+1]
        
        if json_str:
            data = json.loads(json_str)
            
            # Chercher les menaces avec différentes clés possibles
            for key in data.keys():
                key_lower = key.lower().replace(' ', '').replace('_', '')
                if key_lower in ['etape2', 'étape2', 'step2', 'threats', 'menaces']:
                    if isinstance(data[key], list):
                        threats = data[key]
                        break
                        
    except Exception as e:
        # Parsing alternatif si JSON échoue
        lines = analysis.split('\n')
        current_threat = {}
        
        for line in lines:
            line = line.strip()
            if 'Menace_associée' in line or 'Menace associée' in line:
                if current_threat:
                    threats.append(current_threat)
                current_threat = {'Menace_associée': line.split(':')[-1].strip()}
            elif 'Élément_vulnérable' in line and 'Menace' not in line and current_threat:
                current_threat['Élément_vulnérable'] = line.split(':')[-1].strip()
            elif 'Justification' in line and current_threat:
                current_threat['Justification'] = line.split(':')[-1].strip()
        
        if current_threat:
            threats.append(current_threat)
    
    return threats

# ========== INTERFACE AGENT AMÉLIORÉE ==========
def show_agent_interface(agent_type):
    """Interface améliorée pour chaque agent"""
    
    agent_configs = {
        "llamaparse": {
            "title": "📄 LlamaParse Agent",
            "description": "Extraction et parsing de documents PDF",
            "icon": "📄",
            "processor": process_llamaparse_agent,
            "needs_file": True
        },
        "summary": {
            "title": "📊 Summary Agent", 
            "description": "Résumé automatique page par page",
            "icon": "📊",
            "processor": process_summary_agent,
            "needs_file": True
        },
        "vulnerability": {
            "title": "🔍 Vulnerability Agent",
            "description": "Analyse des vulnérabilités et menaces",
            "icon": "🔍",
            "processor": process_vulnerability_agent,
            "needs_file": False
        }
    }
    
    if agent_type in agent_configs:
        config = agent_configs[agent_type]
        
        # En-tête de l'agent
        st.markdown(f"## {config['title']}")
        st.markdown(f"*{config['description']}*")
        
        # Information sur les prérequis
        if agent_type == "summary" and not get_processed_documents():
            st.warning("📋 Prérequis: Vous devez d'abord traiter un document avec LlamaParse")
        elif agent_type == "vulnerability" and not get_summarizer_documents():
            st.warning("📋 Prérequis: Vous devez d'abord traiter un document avec Summary Agent")
        
        # Interface de traitement
        if config['needs_file']:
            uploaded_file = st.file_uploader(
                "📎 Choisir un fichier PDF",
                type=['pdf'],
                key=f"uploader_{agent_type}"
            )
            
            if uploaded_file:
                st.success(f"✅ Fichier sélectionné: {uploaded_file.name}")
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("🚀 Lancer l'analyse", type="primary", use_container_width=True):
                        config['processor'](uploaded_file)
                with col2:
                    if st.button("🔄 Retour à l'accueil", use_container_width=True):
                        st.session_state.selected_agent = None
                        st.session_state.workflow_step = 1
                        st.rerun()
        else:
            # Agents sans fichier (comme Vulnerability)
            config['processor']()
            
            if st.button("🔄 Retour à l'accueil", use_container_width=True):
                st.session_state.selected_agent = None
                st.session_state.workflow_step = 1
                st.rerun()

# ========== VISUALISATEUR PDF AMÉLIORÉ ==========
def show_document_viewer():
    """Affiche le document en style PDF avec édition"""
    if not UTILS_AVAILABLE:
        st.error("Les fonctions utilitaires ne sont pas disponibles")
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
        pages_content = doc_data.get('summaries', [])
    elif doc_type == 'vulnerability':
        processed_docs = st.session_state.get('vulnerability_results', {})
        doc_data = processed_docs.get(doc_name, {})
        total_pages = len(doc_data.get('results', []))
        pages_content = doc_data.get('results', [])
    else:
        processed_docs = get_processed_documents()
        doc_data = processed_docs.get(doc_name, {})
        total_pages = len(doc_data.get('pages', []))
        pages_content = doc_data.get('pages', [])
    
    if not doc_data or not pages_content:
        st.error("Document non trouvé")
        if st.button("← Retour"):
            del st.session_state.viewing_page
            st.rerun()
        return
    
    # Navigation en haut
    st.markdown(f"""
    <div class="pdf-navigation">
        <span class="page-indicator">📄 {page_data['original_name']}</span>
        <span class="page-indicator">Page {current_page} / {total_pages}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Boutons de navigation
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Accueil", key="home"):
            del st.session_state.viewing_page
            st.rerun()
    
    with col2:
        if current_page > 1 and st.button("⏮ Début", key="first"):
            st.session_state.viewing_page['page_num'] = 1
            st.rerun()
    
    with col3:
        if current_page > 1 and st.button("◀ Précédent", key="prev"):
            st.session_state.viewing_page['page_num'] = current_page - 1
            st.rerun()
    
    with col4:
        # Sélecteur de page
        new_page = st.selectbox(
            "Aller à:",
            range(1, total_pages + 1),
            index=current_page - 1,
            key=f"page_selector_{doc_name}_{doc_type}"
        )
        if new_page != current_page:
            st.session_state.viewing_page['page_num'] = new_page
            st.rerun()
    
    with col5:
        if current_page < total_pages and st.button("Suivant ▶", key="next"):
            st.session_state.viewing_page['page_num'] = current_page + 1
            st.rerun()
    
    with col6:
        if current_page < total_pages and st.button("Fin ⏭", key="last"):
            st.session_state.viewing_page['page_num'] = total_pages
            st.rerun()
    
    with col7:
        # Mode édition
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        
        if st.button("✏️ Éditer" if not st.session_state.edit_mode else "💾 Sauver", key="edit_toggle"):
            if st.session_state.edit_mode:
                # Sauvegarder les modifications
                if doc_type == 'llamaparse':
                    doc_data['pages'][current_page - 1] = st.session_state.edited_content
                elif doc_type == 'summarizer':
                    doc_data['summaries'][current_page - 1] = st.session_state.edited_content
                st.success("Modifications sauvegardées!")
            st.session_state.edit_mode = not st.session_state.edit_mode
            st.rerun()
    
    # Affichage du contenu
    if doc_type == 'vulnerability':
        # Sécuriser l'accès à la page
        if 1 <= current_page <= len(pages_content):
            current_content = pages_content[current_page - 1]
            if isinstance(current_content, dict):
                # Afficher dans le viewer PDF
                st.markdown('<div class="pdf-viewer">', unsafe_allow_html=True)
                render_vulnerability_page(current_content, current_page)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Format de contenu invalide pour les vulnérabilités")
        else:
            st.error("Page non disponible")
    elif doc_type == 'summarizer':
        current_content = pages_content[current_page - 1] if current_page <= len(pages_content) else {}
        st.markdown('<div class="pdf-viewer">', unsafe_allow_html=True)
        render_summary_page(current_content, current_page, st.session_state.edit_mode)
        st.markdown('</div>', unsafe_allow_html=True)
    else:  # llamaparse
        st.markdown('<div class="pdf-viewer">', unsafe_allow_html=True)
        current_content = pages_content[current_page - 1] if current_page <= len(pages_content) else ""
        render_llamaparse_page(current_content, current_page, st.session_state.edit_mode)
        st.markdown('</div>', unsafe_allow_html=True)

def render_llamaparse_page(content, page_num, edit_mode):
    """Rendu d'une page LlamaParse en style PDF"""
    if edit_mode:
        st.markdown('<div class="content-editor">', unsafe_allow_html=True)
        edited_content = st.text_area(
            "Éditer le contenu:",
            value=content,
            height=600,
            key="edit_area"
        )
        st.session_state.edited_content = edited_content
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Affichage en style PDF
        content_html = clean_markdown_content(content).replace('\n', '<br>')
        st.markdown(f"""
        <div class="pdf-page">
            <div class="pdf-header">
                <div class="pdf-title">Document Extrait</div>
                <div class="pdf-subtitle">Page {page_num}</div>
            </div>
            <div class="pdf-content">
                {content_html}
            </div>
            <div class="page-number">Page {page_num}</div>
        </div>
        """, unsafe_allow_html=True)

def render_summary_page(content, page_num, edit_mode):
    """Rendu amélioré d'une page Summary"""
    if isinstance(content, dict):
        # Nettoyer et formater le contenu
        section = content.get('sectionTitle', 'Section sans titre')
        summary = content.get('pageSummary', 'Aucun résumé disponible')
        is_continuation = content.get('isContinuation', False)
        global_summary = content.get('updatedGlobalSummary', 'Aucun résumé global disponible')
        
        if edit_mode:
            # Mode édition
            st.markdown("### ✏️ Édition du résumé")
            new_section = st.text_input("Titre de la section:", value=section)
            new_summary = st.text_area("Résumé de la page:", value=summary, height=150)
            new_continuation = st.checkbox("Continuation de la section précédente", value=is_continuation)
            new_global = st.text_area("Résumé global:", value=global_summary, height=200)
            st.session_state.edited_content = {
                'sectionTitle': new_section,
                'pageSummary': new_summary,
                'isContinuation': new_continuation,
                'updatedGlobalSummary': new_global
            }
        else:
            # Affichage stylé façon PDF uniquement dans le visualiseur
            st.markdown(f"""
            <div class="pdf-page">
                <div class="pdf-header">
                    <div class="pdf-title">Résumé Analytique</div>
                    <div class="pdf-subtitle">Page {page_num} - {section}</div>
                </div>
                <div class="pdf-content">
                    <h3>📝 Résumé de la page</h3>
                    <div class="clean-markdown">{summary}</div>

                    
                    <h3>🌐 Vue d'ensemble</h3>
                    <div class="clean-markdown">{global_summary}</div>
                </div>
                <div class="page-number">Page {page_num}</div>
            </div>
            """, unsafe_allow_html=True)

def render_vulnerability_page(content, page_num):
    """Rendu amélioré d'une page de vulnérabilités avec données structurées"""
    
    # Vérifier le format des données
    if isinstance(content, dict):
        # Nouvelles données structurées
        if 'vulnerabilities' in content and 'threats' in content:
            vulnerabilities = content['vulnerabilities']
            threats = content['threats']
            section = content.get('section', 'N/A')
        else:
            # Ancien format - parser l'analyse
            analysis = content.get('analysis', '')
            section = content.get('section', 'N/A')
            vulnerabilities = extract_vulnerabilities_from_analysis(analysis)
            threats = extract_threats_from_analysis(analysis)
    else:
        # Format non reconnu
        vulnerabilities = []
        threats = []
        section = 'N/A'
    
    # Affichage en style PDF propre
    st.markdown(f"""
    <div class="pdf-page">
        <div class="pdf-header">
            <div class="pdf-title">Analyse des Vulnérabilités et Menaces</div>
            <div class="pdf-subtitle">Page {page_num} - Section: {section}</div>
        </div>
        <div class="pdf-content">
    """, unsafe_allow_html=True)
    
    # Section Vulnérabilités
    st.markdown("<h3 style='color: #dc3545; border-bottom: 2px solid #dc3545; padding-bottom: 10px;'>🔍 Vulnérabilités Identifiées</h3>", unsafe_allow_html=True)
    
    if vulnerabilities:
        for i, vuln in enumerate(vulnerabilities, 1):
            element = vuln.get('Élément_vulnérable', vuln.get('Élément vulnérable', 'N/A'))
            justif = vuln.get('Justification', 'N/A')
            
            st.markdown(f"""
            <div style="background: #f8f9fa; border-left: 4px solid #dc3545; padding: 15px; margin: 15px 0; border-radius: 0 5px 5px 0;">
                <div style="font-weight: bold; color: #dc3545; margin-bottom: 8px;">
                    Vulnérabilité #{i}: {element}
                </div>
                <div style="color: #333; line-height: 1.5;">{justif}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='background: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; color: #6c757d;'>Aucune vulnérabilité identifiée sur cette page</div>", unsafe_allow_html=True)
    
    # Section Menaces
    st.markdown("<h3 style='color: #856404; border-bottom: 2px solid #ffc107; padding-bottom: 10px; margin-top: 30px;'>⚠️ Menaces Associées</h3>", unsafe_allow_html=True)
    
    if threats:
        for i, threat in enumerate(threats, 1):
            element = threat.get('Élément_vulnérable', threat.get('Élément vulnérable', 'N/A'))
            menace = threat.get('Menace_associée', threat.get('Menace associée', 'N/A'))
            justif = threat.get('Justification', 'N/A')
            
            st.markdown(f"""
            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; border-radius: 0 5px 5px 0;">
                <div style="font-weight: bold; color: #856404; margin-bottom: 8px;">
                    Menace #{i}: {element} → {menace}
                </div>
                <div style="color: #333; line-height: 1.5;">{justif}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='background: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; color: #6c757d;'>Aucune menace identifiée sur cette page</div>", unsafe_allow_html=True)
    
    # Bouton pour voir le PDF original
    st.markdown("<div style='margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
    
    if st.button("📄 Voir le contenu original de cette page", key=f"see_original_{page_num}"):
        current_doc_name = st.session_state.viewing_page.get('doc_name', '')
        if current_doc_name.startswith('vuln_'):
            parts = current_doc_name.split('_')
            if len(parts) >= 2:
                llama_doc_name = parts[1]
                processed_docs = get_processed_documents()
                
                if llama_doc_name in processed_docs:
                    llama_doc = processed_docs[llama_doc_name]
                    if page_num <= len(llama_doc['pages']):
                        st.session_state.viewing_page = {
                            'doc_name': llama_doc_name,
                            'page_num': page_num,
                            'content': llama_doc['pages'][page_num-1],
                            'original_name': llama_doc['original_name'],
                            'type': 'llamaparse'
                        }
                        st.rerun()
                    else:
                        st.error("Page non disponible dans le document original")
                else:
                    st.error("Document original non trouvé")
            else:
                st.error("Format de nom de document invalide")
        else:
            st.error("Ce document n'est pas un rapport de vulnérabilité")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Numéro de page
    st.markdown(f"<div class='page-number'>Page {page_num}</div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# ========== UI PRINCIPALE AMÉLIORÉE ==========
def main_ui():
    # Initialisation des états de session
    if 'selected_agent' not in st.session_state:
        st.session_state.selected_agent = None
    if 'workflow_step' not in st.session_state:
        st.session_state.workflow_step = 1
    
    # Visualisation d'une page
    if 'viewing_page' in st.session_state and st.session_state.viewing_page:
        show_document_viewer()
        return
    
    # Header principal
    st.title("🎯 Plateforme d'Analyse de Risques IA")
    st.markdown("### Workflow intégré pour l'analyse documentaire")
    
    # Navigation par workflow
    show_workflow_navigation()
    
    # Interface agent ou sélection
    if st.session_state.selected_agent:
        show_agent_interface(st.session_state.selected_agent)
    else:
        # Cartes des agents avec statut
        st.markdown("### 🤖 Sélectionnez un agent pour commencer")
        
        agents = [
            {
                "id": "llamaparse", 
                "name": "LlamaParse", 
                "icon": "📄", 
                "desc": "Extraction de contenu PDF",
                "status": "ready" if UTILS_AVAILABLE else "pending"
            },
            {
                "id": "summary", 
                "name": "Summary", 
                "icon": "📊", 
                "desc": "Résumé automatique",
                "status": "ready" if get_processed_documents() else "pending"
            },
            {
                "id": "vulnerability", 
                "name": "Vulnerability", 
                "icon": "🔍", 
                "desc": "Analyse des risques", 
                "status": "ready" if get_summarizer_documents() else "pending"
            }
        ]
        
        for agent in agents:
            status_class = "status-ready" if agent["status"] == "ready" else "status-pending"
            status_text = "Prêt" if agent["status"] == "ready" else "En attente"
            
            st.markdown(f'''
            <div class="agent-card-enhanced">
                <div class="agent-header">
                    <div class="agent-icon">{agent['icon']}</div>
                    <div>
                        <h3>{agent['name']} Agent</h3>
                        <p>{agent['desc']}</p>
                    </div>
                </div>
                <div class="agent-status {status_class}">{status_text}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"Lancer {agent['name']}", key=f"btn_{agent['id']}", use_container_width=True):
                    if agent["status"] == "ready":
                        st.session_state.selected_agent = agent['id']
                        st.session_state.workflow_step = ["llamaparse", "summary", "vulnerability"].index(agent['id']) + 1
                        st.rerun()
                    else:
                        st.warning(f"Prérequis manquants pour {agent['name']}")
            with col2:
                if agent["id"] == "llamaparse" and get_processed_documents():
                    if st.button("📊 Voir", key=f"view_{agent['id']}", use_container_width=True):
                        docs = get_processed_documents()
                        if docs:
                            first_doc = list(docs.keys())[0]
                            st.session_state.viewing_page = {
                                'doc_name': first_doc,
                                'page_num': 1,
                                'content': docs[first_doc]['pages'][0],
                                'original_name': docs[first_doc]['original_name'],
                                'type': 'llamaparse'
                            }
                            st.rerun()

# ========== MAIN ==========
def main():
    load_styles()
    sidebar()
    main_ui()

if __name__ == "__main__":
    main()