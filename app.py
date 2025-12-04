import streamlit as st
from app.handlers.config import setup_logging
from app.handlers.ui import apply_custom_styles, render_header, render_sidebar_footer
from app.handlers.data_handler import load_all_data, initialize_session_state
from app.handlers.analysis import run_analysis, calculate_nps_metrics
from app.handlers.filters import get_filter_options, apply_filters
from app.handlers.visualization import render_chart
from app.handlers.pdf_generator import generate_pdf

# konfiguracja logowania
logger = setup_logging()

# konfiguracja streamlit
st.set_page_config(
    page_title="Kluno NPS Prediction & Analytics Dashboard",
    initial_sidebar_state="expanded"
)

# stosowanie stylow
apply_custom_styles()

# renderowanie naglowka
render_header()

# sidebar wczytywanie danych
st.sidebar.header("Wczytaj dane do analizy")
uploaded_grafik = st.sidebar.file_uploader("Grafik doradców", type='csv')
uploaded_prognoza = st.sidebar.file_uploader("Prognoza spraw", type='csv')

if uploaded_grafik:
    logger.info(f"wczytano plik grafik {uploaded_grafik.name} {uploaded_grafik.size} bajtow")
if uploaded_prognoza:
    logger.info(f"wczytano plik prognoza {uploaded_prognoza.name} {uploaded_prognoza.size} bajtow")

# inicjalizacja session state
initialize_session_state()

# wczytanie danych historycznych i modeli
df_2024, model, encoder = load_all_data()

# uruchomienie analizy
if uploaded_grafik and uploaded_prognoza and st.sidebar.button("Rozpocznij analizę"):
    try:
        df = run_analysis(uploaded_grafik, uploaded_prognoza, df_2024, model, encoder)
        st.session_state['analiza_gotowa'] = True
        st.session_state['df_nps'] = df.copy()
        st.success("Analiza zakończona pomyślnie!")
    except Exception as e:
        logger.error(f"blad podczas analizy {e}", exc_info=True)
        st.error(f"wystapil blad podczas analizy {e}")

# widok po analizie
if st.session_state['analiza_gotowa']:
    df = st.session_state['df_nps']

    # obliczanie metryk nps
    nps_total_2025, nps_total_2024 = calculate_nps_metrics(df)

    # wyswietlanie metryk
    col1, col2 = st.columns(2)
    col1.metric("NPS 2025", f"{round(nps_total_2025, 2)}")
    col2.metric("NPS 2024", f"{round(nps_total_2024, 2)}")

    # pobieranie opcji filtrowania
    wszyscy_doradcy, wszystkie_skille, wszystkie_tagi = get_filter_options(df)

    # filtry
    wybrani_doradcy = st.multiselect("Filtruj po doradcach:", wszyscy_doradcy)
    wybrane_skille = st.multiselect("Filtruj po skillach:", wszystkie_skille)
    wybrane_tagi = st.multiselect("Filtruj po tagach:", wszystkie_tagi)

    # stosowanie filtrow
    df_filtered = apply_filters(df, wybrani_doradcy, wybrane_skille, wybrane_tagi)

    # wybor widoku wykresow
    widok = st.radio("Wybierz widok:", ["2025", "2024", "Porównanie", "Zmiana NPS"], horizontal=True)

    # renderowanie wykresu
    render_chart(widok, df_filtered, nps_total_2025, nps_total_2024)

    # tabela szczegolowa
    if not df_filtered.empty:
        nps_filtrowany = (df_filtered['Prognozowany_NPS'] * df_filtered['Przypisane_sprawy']).sum() / df_filtered['Przypisane_sprawy'].sum()
        st.metric("NPS po filtrach", f"{round(nps_filtrowany, 2)}")

        st.subheader("Dane szczegółowe")
        st.dataframe(df_filtered[['Imię nazwisko', 'Skille', 'Tagi', 'NPS_2024', 'Prognozowany_NPS', 'Zmiana_NPS']])

        # generowanie pdf
        if st.button("Pobierz raport PDF"):
            try:
                file_pdf = generate_pdf(df_filtered)
                with open(file_pdf, "rb") as f:
                    st.download_button("Pobierz PDF", data=f, file_name="raport_nps.pdf", mime="application/pdf")
            except Exception as e:
                logger.error(f"blad podczas przygotowania pdf do pobrania {e}", exc_info=True)
                st.error(f"wystapil blad podczas generowania pdf {e}")
    else:
        st.info("Brak danych po filtrze.")

else:
    st.info("Wgraj grafik i prognozę, aby rozpocząć analizę.")

# stopka sidebar
render_sidebar_footer()
