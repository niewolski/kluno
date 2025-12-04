# komponenty ui style css logo header
import streamlit as st
import base64
import logging
import os

logger = logging.getLogger(__name__)

def apply_custom_styles():
    # dodaje style css do aplikacji
    st.markdown("""
        <style>
            .main {
                background-color: #f0f2f6;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            h1 {
                color: #6a4c93 !important;
                font-weight: 700;
                margin-bottom: 0.3rem;
            }
            .sidebar .sidebar-content {
                background-color: #e6e0f8;
                padding: 1.5rem;
            }
            .stMetricValue {
                font-size: 32px !important;
                color: #3a2f6d;
                font-weight: 600;
            }
            .stMetricLabel {
                color: #5f5482;
                font-weight: 500;
            }
            div.stButton > button {
                background-color: #6a4c93;
                color: white;
                border-radius: 8px;
                border: none;
                padding: 0.5rem 1rem;
                font-weight: 600;
                transition: background-color 0.3s ease;
            }
            div.stButton > button:hover {
                background-color: #553a75;
                cursor: pointer;
            }
            .stDataFrame table {
                border-radius: 8px;
                overflow: hidden;
                border-collapse: separate !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            }
            .css-1d391kg {
                gap: 1.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

def load_logo_base64(path):
    # laduje logo i konwertuje do base64
    try:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            logger.info(f"logo zaladowane pomyslnie {path}")
            return encoded
    except Exception as e:
        logger.error(f"blad podczas ladowania logo {e}")
        raise

def render_header(logo_path=None):
    # rysuje naglowek z logo
    if logo_path is None:
        # proba 1: sciezka wzgledna do pliku ui.py
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(base_dir, "app", "assets", "kluno_logo2.png")
        
        # proba 2: sciezka wzgledna do biezacego katalogu roboczego
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.getcwd(), "app", "assets", "kluno_logo2.png")
        
        # proba 3: prosta sciezka wzgledna
        if not os.path.exists(logo_path):
            logo_path = "app/assets/kluno_logo2.png"
        
        # jesli nadal nie istnieje to None
        if not os.path.exists(logo_path):
            logger.warning(f"nie znaleziono logo w {logo_path} probowano tez {os.path.join(os.getcwd(), 'app', 'assets', 'kluno_logo2.png')}")
            logo_path = None
    
    if logo_path and os.path.exists(logo_path):
        try:
            logo_base64 = load_logo_base64(logo_path)
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2.5rem;">
                    <img src="data:image/png;base64,{logo_base64}" width="180" style="margin-right: 1px;" />
                    <h1 style="color: #6a4c93; font-weight: 700; font-size: 2.4rem; margin: 0;">
                        Kluno NPS Prediction & Analytics Dashboard
                    </h1>
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            logger.warning(f"nie udalo sie zaladowac logo {e}")
            logo_path = None
    
    if not logo_path:
        # jesli logo sie nie zaladowalo pokaz tylko tekst
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2.5rem;">
                <h1 style="color: #6a4c93; font-weight: 700; font-size: 2.4rem; margin: 0;">
                    Kluno NPS Prediction & Analytics Dashboard
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_sidebar_footer(version="1.1.3"):
    # rysuje stopke w sidebarze z wersja
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"<p style='text-align:center; color: gray;'>Wersja {version}</p>", unsafe_allow_html=True)
