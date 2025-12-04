# wczytywanie danych i modeli
import pandas as pd
import joblib
import streamlit as st
import logging

logger = logging.getLogger(__name__)

def load_historical_data():
    # wczytuje dane z 2024
    try:
        logger.info("wczytywanie danych historycznych")
        df_2024 = pd.read_csv('prepared_data/dane_treningowe.csv')[
            ['Imię nazwisko', 'Skille', 'Tagi', 'NPS', 'Przypisane_sprawy']
        ]
        df_2024.rename(columns={
            'NPS': 'NPS_2024',
            'Przypisane_sprawy': 'Przypisane_sprawy_2024'
        }, inplace=True)
        logger.info(f"wczytano {len(df_2024)} rekordow danych historycznych")
        return df_2024
    except Exception as e:
        logger.error(f"blad podczas wczytywania danych historycznych {e}", exc_info=True)
        raise

def load_models():
    # wczytuje model nps i encoder skilli
    try:
        logger.info("wczytywanie modelu nps")
        model = joblib.load('models/model_nps.pkl')
        logger.info("model nps zaladowany pomyslnie")
        
        logger.info("wczytywanie encodera skilli")
        encoder = joblib.load('models/skille_encoder.pkl')
        logger.info("encoder skilli zaladowany pomyslnie")
        
        return model, encoder
    except Exception as e:
        logger.error(f"blad podczas wczytywania modelu encodera {e}", exc_info=True)
        raise

def load_all_data():
    # wczytuje wszystkie dane i modele
    try:
        df_2024 = load_historical_data()
        model, encoder = load_models()
        return df_2024, model, encoder
    except Exception as e:
        st.error(f"blad podczas wczytywania danych {e}")
        st.stop()
        return None, None, None

def initialize_session_state():
    # ustawia poczatkowe wartosci w session state
    if 'analiza_gotowa' not in st.session_state:
        st.session_state['analiza_gotowa'] = False
    if 'df_nps' not in st.session_state:
        st.session_state['df_nps'] = None
