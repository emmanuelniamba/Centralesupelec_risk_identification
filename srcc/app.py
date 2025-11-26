import streamlit as st
import os
import tempfile
import time
from pathlib import Path

# --- IMPORTS ---
try:
    from utils.content_extraction import Content_Extractor
    from utils.agents import SummarizerAgent, VulnerabilityAgent
    from prompt.templates import prompt_context, prompt_de_base
except ImportError:
    prompt_context = ""
    prompt_de_base = ""

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Risk Detection Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS PRO (CORRECTION VISIBILITÉ LOGIN)
# ==========================================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* --- FOND PRINCIPAL --- */
    .stApp { background-color: #343541; color: #ECECF1; }
    
    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] { 
        background-color: #171717; 
        border-right: 1px solid #333;
    }
    section[data-testid="stSidebar"] * { color: #ECECF1 !important; }

    /* --- INPUTS LOGIN (Visible !) --- */
    /* Le Label (Titre du champ) en BLANC */
    .stTextInput label p {
        color: #FFFFFF !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    
    /* La Boîte de saisie (Gris foncé / Texte Blanc) */
    .stTextInput input {
        background-color: #40414F !important;
        color: #FFFFFF !important;
        border: 1px solid #565869 !important;
        border-radius: 6px;
    }
    .stTextInput input:focus {
        border-color: #10a37f !important;
    }

    /* --- EDITOR STYLE "A4 PAPER" --- */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-family: 'Georgia', serif;
        font-size: 16px;
        line-height: 1.6;
        padding: 40px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        border-radius: 2px !important;
        border: none !important;
    }
    .stTextArea label { display: none; }

    /* --- BOUTONS --- */
    /* Primaire (Vert) */
    button[kind="primary"] {
        background-color: #10a37f !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 600 !important;
    }
    button[kind="primary"]:hover {
        opacity: 0.9;
    }
    
    /* Secondaire (Gris/Blanc) */
    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #E5E7EB !important;
        font-weight: 600 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #F3F4F6 !important;
        border-color: #D1D5DB !important;
    }

    /* Fix spécifique pour le bouton Submit du form Login */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #10a37f !important;
        color: #FFFFFF !important;
        border: none !important;
        width: 100%;
    }

    /* --- ONGLETS (TABS) --- */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #565869; }
    .stTabs [data-baseweb="tab"] { color: #9CA3AF; }
    .stTabs [aria-selected="true"] { 
        color: #FFFFFF !important;
        border-bottom: 3px solid #10a37f !important;
    }

    /* --- RISK CARDS --- */
    .vuln-card {
        background-color: #450a0a;
        border: 1px solid #ef4444;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .threat-card {
        background-color: #431407;
        border: 1px solid #f97316;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 10px;
        margin-left: 20px;
    }

    /* --- DASHBOARD CARDS --- */
    .dash-card {
        background-color: #202123;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #4D4D4F;
        text-align: center;
        height: 100%;
    }
    .dash-title { color: #fff; font-size: 1.1rem; font-weight: 600; margin-bottom: 10px; }
    .dash-desc { color: #9ca3af; font-size: 0.9rem; line-height: 1.5; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. SESSION & LOGIN
# ==========================================
def init_session():
    if 'parsed_pages' not in st.session_state: st.session_state.parsed_pages = []
    if 'current_page_idx' not in st.session_state: st.session_state.current_page_idx = 0
    if 'context_results' not in st.session_state: st.session_state.context_results = []
    if 'risk_results' not in st.session_state: st.session_state.risk_results = []
    if 'api_keys_set' not in st.session_state: st.session_state.api_keys_set = False

def show_login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        # En-tête simplifié
        st.markdown("""
        <div style="background-color: #202123; padding: 30px; border-radius: 12px; border: 1px solid #4D4D4F; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <h1 style="color: white; margin-bottom: 0px;">🔐 Risk Assistant</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            # Champs renommés explicitement
            key_llm = st.text_input("OpenRouter API Key", type="password", help="Format: sk-or-v1-...")
            key_llama = st.text_input("LlamaCloud API Key", type="password", help="Format: llx-...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Bouton vert forcé
            submitted = st.form_submit_button("🚀 Accéder au Système", type="primary")
            
            if submitted:
                if key_llm and key_llama:
                    st.session_state['api_key_llm'] = key_llm
                    st.session_state['api_key_llama'] = key_llama
                    os.environ["llm_key"] = key_llm
                    os.environ["OPENAI_API_KEY"] = key_llm
                    os.environ["LLAMA_CLOUD_API_KEY"] = key_llama
                    st.session_state.api_keys_set = True
                    st.rerun()
                else:
                    st.error("Veuillez remplir les deux champs.")

        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: #2A2B32; border-left: 3px solid #10a37f; color: #cfcfd1; font-size: 0.85rem;">
            <strong>ℹ️ Prototype Enterprise</strong><br>
            Cet outil assiste les professionnels du risque dans l'analyse documentaire via IA.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR
# ==========================================
def setup_sidebar():
    st.sidebar.markdown("""
        <div style="margin-bottom:20px;">
            <h3 style='color:#FFFFFF; margin:0; letter-spacing:1px;'>RISK DETECT</h3>
            <p style='color:#10a37f; font-size:11px; font-weight:700;'>ENTERPRISE PROTOTYPE</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### NAVIGATION")
    mode = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Document Extraction", "Context Analysis", "Risk Analysis"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Bouton deconnexion (Style secondaire : Blanc/Noir -> Rouge au survol)
    if st.sidebar.button("Se déconnecter", use_container_width=True, type="secondary"):
        st.session_state.api_keys_set = False
        st.session_state.parsed_pages = []
        st.rerun()

    return mode

# ==========================================
# 3. EXTRACTION
# ==========================================
def show_extraction_interface():
    st.markdown("## Document Workspace")
    
    if not st.session_state.parsed_pages:
        st.markdown("""
        <div style="border: 1px dashed #565869; padding: 40px; text-align: center; border-radius: 8px; background-color: #202123;">
            <h4 style="color:white;">Espace de travail vide</h4>
            <p style="color:#8e8ea0;">Importez un PDF pour générer la vue document.</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload PDF", type=['pdf'], label_visibility="collapsed")
        
        if uploaded_file and st.button("Lancer l'extraction structurée", type="primary"):
            with st.status("Traitement du document...", expanded=True) as status:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.getvalue())
                        path = tmp.name
                    
                    extractor = Content_Extractor()
                    text = extractor.extract_content_from_file(path)
                    data = extractor.parse_pages_from_text(text)
                    
                    if data:
                        st.session_state.parsed_pages = data
                        st.session_state.current_page_idx = 0
                        st.rerun()
                    else:
                        st.error("Échec de l'extraction.")
                except Exception as e:
                    st.error(f"Erreur technique: {e}")
    else:
        col_nav, col_paper = st.columns([1, 4])
        
        with col_nav:
            st.markdown("**EXPLORATEUR**")
            if st.button("Effacer tout", use_container_width=True, type="secondary"):
                st.session_state.parsed_pages = []
                st.session_state.context_results = []
                st.session_state.risk_results = []
                st.rerun()
            
            st.markdown("---")
            for i, page in enumerate(st.session_state.parsed_pages):
                label = f"Page {page['page']}"
                if st.button(label, key=f"btn_p{i}", use_container_width=True):
                    st.session_state.current_page_idx = i
                    st.rerun()

        with col_paper:
            if st.session_state.parsed_pages:
                if st.session_state.current_page_idx >= len(st.session_state.parsed_pages):
                    st.session_state.current_page_idx = 0
                
                current_page = st.session_state.parsed_pages[st.session_state.current_page_idx]
                
                c1, c2 = st.columns([4, 1])
                with c1: st.caption(f"ÉDITION / VUE - PAGE {current_page['page']}")
                with c2:
                    if st.button("Suppr. Page", key="del_page", use_container_width=True, type="secondary"):
                        st.session_state.parsed_pages.pop(st.session_state.current_page_idx)
                        if st.session_state.current_page_idx > 0: st.session_state.current_page_idx -= 1
                        st.rerun()

                new_content = st.text_area(
                    "Content",
                    value=current_page['content'],
                    height=800,
                    key=f"editor_{current_page['page']}"
                )
                if new_content != current_page['content']:
                    st.session_state.parsed_pages[st.session_state.current_page_idx]['content'] = new_content

# ==========================================
# 4. CONTEXT ANALYSIS
# ==========================================
def show_context_interface():
    st.markdown("## Context Analysis")
    
    if not st.session_state.parsed_pages:
        st.warning("Aucun document disponible pour l'analyse.")
        return

    if not st.session_state.context_results:
        st.info(f"Document prêt : {len(st.session_state.parsed_pages)} pages à analyser.")
        if st.button("Lancer l'analyse contextuelle", type="primary"):
            run_context_analysis()

    else:
        c_nav, c_act = st.columns([3, 1])
        with c_nav:
            pages_list = [f"Page {r['page']}" for r in st.session_state.context_results]
            selected = st.selectbox("Navigation rapide :", pages_list, label_visibility="collapsed")
        
        with c_act:
            if st.button("🔄 Relancer l'analyse", use_container_width=True, type="secondary"):
                st.session_state.context_results = []
                st.rerun()
        
        if pages_list:
            idx = pages_list.index(selected)
            data = st.session_state.context_results[idx]
            
            st.markdown(f"### {data.get('sectionTitle', 'Section Sans Titre')}")
            
            t1, t2 = st.tabs(["Résumé de la Page", "Contexte Global"])
            
            with t1:
                st.text_area("Résumé", value=data.get('pageSummary'), height=500, key=f"summary_{data['page']}")
            with t2:
                st.text_area("Contexte", value=data.get('updatedGlobalSummary'), height=600, key=f"global_{data['page']}")

def run_context_analysis():
    try:
        agent = SummarizerAgent()
        bar = st.progress(0, text="Initialisation...")
        def update_progress(p):
            bar.progress(p, text=f"Analyse sémantique en cours... {p}%")
        
        res = agent.process_document(
            st.session_state.parsed_pages, 
            system_prompt=prompt_context, 
            temperature=0.2,
            progress_callback=update_progress
        )
        bar.progress(100, text="Terminé !")
        time.sleep(0.5)
        st.session_state.context_results = res
        st.rerun()
    except Exception as e:
        st.error(f"Erreur: {e}")

# ==========================================
# 5. RISK ASSESSMENT
# ==========================================
def show_risk_interface():
    st.markdown("## Risk Assessment")
    
    if not st.session_state.context_results:
        st.warning("L'analyse contextuelle est requise avant le scan.")
        return

    if not st.session_state.risk_results:
        if st.button("Démarrer le scan de risques", type="primary"):
            try:
                agent = VulnerabilityAgent()
                bar = st.progress(0, text="Scan démarré...")
                def update_progress(p):
                    bar.progress(p, text=f"Identification des menaces... {p}%")
                
                res = agent.process_risks(
                    st.session_state.context_results,
                    system_prompt=prompt_de_base,
                    temperature=0.2,
                    progress_callback=update_progress
                )
                bar.progress(100, text="Terminé !")
                time.sleep(0.5)
                st.session_state.risk_results = res
                st.rerun()
            except Exception as e:
                st.error(f"Erreur: {e}")
    else:
        for r in st.session_state.risk_results:
            with st.expander(f"Page {r['page']} - Rapport de Risques", expanded=True):
                vulns = r.get('vulnerabilities', [])
                threats = r.get('threats', [])
                
                if not vulns and not threats:
                    st.success("✅ Aucun risque critique identifié sur cette page.")
                
                # Vulnérabilités
                if vulns:
                    st.markdown("#### 🔓 Vulnérabilités")
                    for v in vulns:
                        el = v.get('element') if isinstance(v, dict) else v.element
                        ju = v.get('justification') if isinstance(v, dict) else v.justification
                        
                        st.markdown(f"""
                        <div class="vuln-card">
                            <strong style="color:#fca5a5; font-size:1.05rem;">❌ {el}</strong><br>
                            <span style="color:#e5e7eb; display:block; margin-top:5px;">{ju}</span>
                        </div>
                        """, unsafe_allow_html=True)

                # Menaces
                if threats:
                    st.markdown("#### ☠️ Menaces")
                    for t in threats:
                        el = t.get('element') if isinstance(t, dict) else t.element
                        th = t.get('threat') if isinstance(t, dict) else t.threat
                        cons = t.get('consequence') if isinstance(t, dict) else t.consequence
                        
                        st.markdown(f"""
                        <div class="threat-card">
                            <strong style="color:#fdba74;">⚠️ {el}</strong><br>
                            <em style="color:#fff;">{th}</em><br>
                            <span style="color:#9ca3af; font-size:0.9rem;">Conséquence: {cons}</span>
                        </div>
                        """, unsafe_allow_html=True)

# ==========================================
# DASHBOARD
# ==========================================
def show_dashboard():
    st.markdown("<h1 style='text-align:center; color:#ECECF1; margin-bottom: 40px;'>Tableau de Bord</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-title">1. Extraction Structurée</div>
            <div class="dash-desc">
                Nous récupérons les contenus textuels et la mise en page tout en conservant la structure native du document.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-title">2. Compréhension Sémantique</div>
            <div class="dash-desc">
                Analyse du document dans sa globalité et localement (page par page) pour assurer une cohérence contextuelle.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="dash-card">
            <div class="dash-title">3. Scan de Risques</div>
            <div class="dash-desc">
                Détection des vulnérabilités critiques et modélisation des menaces basée sur le contexte établi.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# MAIN
# ==========================================
def main():
    load_css()
    init_session()

    if not st.session_state.api_keys_set:
        show_login_screen()
    else:
        mode = setup_sidebar()
        
        if mode == "Dashboard": show_dashboard()
        elif mode == "Document Extraction": show_extraction_interface()
        elif mode == "Context Analysis": show_context_interface()
        elif mode == "Risk Analysis": show_risk_interface()

if __name__ == "__main__":
    main()