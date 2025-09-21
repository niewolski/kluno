import pandas as pd
import streamlit as st
import plotly.express as px
import joblib
from fpdf import FPDF
from PIL import Image
import base64

# streamlit config
st.set_page_config(
    page_title="Kluno NPS Prediction & Analytics Dashboard",
    initial_sidebar_state="expanded"
)

# styl css streamlita
st.markdown("""
    <style>
        /* Tło i font */
        .main {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Nagłówek */
        h1 {
            color: #6a4c93 !important;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }
        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: #e6e0f8;
            padding: 1.5rem;
        }
        /* Metryki */
        .stMetricValue {
            font-size: 32px !important;
            color: #3a2f6d;
            font-weight: 600;
        }
        .stMetricLabel {
            color: #5f5482;
            font-weight: 500;
        }
        /* Przyciski */
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
        /* Tabela */
        .stDataFrame table {
            border-radius: 8px;
            overflow: hidden;
            border-collapse: separate !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        /* Layout kolumn */
        .css-1d391kg {
            gap: 1.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)



# logo
logo_path = "dashboard/kluno_logo2.png"

def load_logo_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        return encoded

logo_base64 = load_logo_base64(logo_path)

# logo z tytulem na srodku
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


# sidebar
st.sidebar.header("Wczytaj dane do analizy")
uploaded_grafik = st.sidebar.file_uploader("Grafik doradców", type='csv')
uploaded_prognoza = st.sidebar.file_uploader("Prognoza spraw", type='csv')

# inicjalizacja session_state
if 'analiza_gotowa' not in st.session_state:
    st.session_state['analiza_gotowa'] = False
if 'df_nps' not in st.session_state:
    st.session_state['df_nps'] = None

# wczytanie danych historycznych modelu i encoderow
df_2024 = pd.read_csv('prepared_data/dane_treningowe.csv')[
    ['Imię nazwisko', 'Skille', 'Tagi', 'NPS', 'Przypisane_sprawy']
]
df_2024.rename(columns={
    'NPS': 'NPS_2024',
    'Przypisane_sprawy': 'Przypisane_sprawy_2024'
}, inplace=True)
model = joblib.load('models/model_nps.pkl')
encoder = joblib.load('models/skille_encoder.pkl')

# uruchomienie analizy
if uploaded_grafik and uploaded_prognoza and st.sidebar.button("Rozpocznij analizę"):
    grafik = pd.read_csv(uploaded_grafik)
    prognoza = pd.read_csv(uploaded_prognoza)

    grafik['Roczna_liczba_godzin'] = grafik.iloc[:, 1:].select_dtypes(include='number').sum(axis=1)
    total_godziny = grafik['Roczna_liczba_godzin'].sum()
    total_spraw = prognoza['Liczba_rekordow'].sum()
    sprawy_na_godzine = total_spraw / total_godziny
    grafik['Przypisane_sprawy'] = (grafik['Roczna_liczba_godzin'] * sprawy_na_godzine).round().astype(int)

    df_pred = pd.merge(
        grafik[['Imię nazwisko', 'Roczna_liczba_godzin', 'Przypisane_sprawy']],
        df_2024[['Imię nazwisko', 'Skille']],
        on='Imię nazwisko', how='left'
    )

    df_pred['Skille_lista'] = df_pred['Skille'].fillna('').apply(lambda x: x.split(', ') if x else [])
    X_skille = pd.DataFrame(encoder.transform(df_pred['Skille_lista']), columns=encoder.classes_)
    X_pred = pd.concat([df_pred[['Roczna_liczba_godzin', 'Przypisane_sprawy']].reset_index(drop=True), X_skille], axis=1)

    df_pred['Prognozowany_NPS'] = model.predict(X_pred).round(2)

    df = pd.merge(df_pred, df_2024, on='Imię nazwisko', how='left')
    df.drop(columns=['Skille_x'], errors='ignore', inplace=True)
    df.rename(columns={'Skille_y': 'Skille'}, inplace=True)
    df['Zmiana_NPS'] = (df['Prognozowany_NPS'] - df['NPS_2024']).round(2)

    st.session_state['analiza_gotowa'] = True
    st.session_state['df_nps'] = df.copy()

# widok po analizie
if st.session_state['analiza_gotowa']:
    df = st.session_state['df_nps']

    nps_total_2025 = (df['Prognozowany_NPS'] * df['Przypisane_sprawy']).sum() / df['Przypisane_sprawy'].sum()
    nps_total_2024 = (df['NPS_2024'] * df['Przypisane_sprawy_2024']).sum() / df['Przypisane_sprawy_2024'].sum()

    col1, col2 = st.columns(2)
    col1.metric("NPS 2025", f"{round(nps_total_2025, 2)}")
    col2.metric("NPS 2024", f"{round(nps_total_2024, 2)}")

    wszyscy_doradcy = sorted(df['Imię nazwisko'].dropna().unique())
    wybrani_doradcy = st.multiselect("Filtruj po doradcach:", wszyscy_doradcy)

    wszystkie_skille = sorted({s for row in df['Skille'].dropna().apply(lambda x: x.split(', ')) for s in row})
    wybrane_skille = st.multiselect("Filtruj po skillach:", wszystkie_skille)

    wszystkie_tagi = sorted({t.strip() for tags in df['Tagi'].dropna() for t in tags.split(',')})
    wybrane_tagi = st.multiselect("Filtruj po tagach:", wszystkie_tagi)

    # filtry danych
    df_filtered = df.copy()
    if wybrani_doradcy:
        df_filtered = df_filtered[df_filtered['Imię nazwisko'].isin(wybrani_doradcy)]
    if wybrane_skille:
        df_filtered = df_filtered[df_filtered['Skille'].fillna('').apply(lambda x: any(skill in x for skill in wybrane_skille))]
    if wybrane_tagi:
        df_filtered = df_filtered[df_filtered['Tagi'].fillna('').apply(lambda x: any(tag in x for tag in wybrane_tagi))]

    # widok wykresow
    widok = st.radio("Wybierz widok:", ["2025", "2024", "Porównanie", "Zmiana NPS"], horizontal=True)

    if widok == "2025":
        fig = px.bar(df_filtered.sort_values('Prognozowany_NPS', ascending=False),
                     x='Imię nazwisko', y='Prognozowany_NPS', color='Prognozowany_NPS',
                     color_continuous_scale='RdYlGn', title="Prognozowany NPS 2025")
        fig.add_hline(y=nps_total_2025, line_dash='dash', line_color='red')
        st.plotly_chart(fig, use_container_width=True)

    elif widok == "2024":
        fig = px.bar(df_filtered.sort_values('NPS_2024', ascending=False),
                     x='Imię nazwisko', y='NPS_2024', color='NPS_2024',
                     color_continuous_scale='RdYlGn', title="Rzeczywisty NPS 2024")
        fig.add_hline(y=nps_total_2024, line_dash='dash', line_color='blue')
        st.plotly_chart(fig, use_container_width=True)

    elif widok == "Porównanie":
        df_melted = df_filtered.melt(id_vars='Imię nazwisko',
                                     value_vars=['NPS_2024', 'Prognozowany_NPS'],
                                     var_name='Rok', value_name='NPS')
        fig = px.bar(df_melted, x='Imię nazwisko', y='NPS', color='Rok',
                     barmode='group', title='Porównanie NPS 2024 vs 2025')
        st.plotly_chart(fig, use_container_width=True)

    elif widok == "Zmiana NPS":
        fig = px.bar(df_filtered.sort_values('Zmiana_NPS', ascending=False),
                     x='Imię nazwisko', y='Zmiana_NPS',
                     color='Zmiana_NPS', color_continuous_scale='RdYlGn',
                     title='Zmiana NPS: 2025 - 2024')
        st.plotly_chart(fig, use_container_width=True)

    # tabela szczegolowa
    if not df_filtered.empty:
        nps_filtrowany = (df_filtered['Prognozowany_NPS'] * df_filtered['Przypisane_sprawy']).sum() / df_filtered['Przypisane_sprawy'].sum()
        st.metric("NPS po filtrach", f"{round(nps_filtrowany, 2)}")

        st.subheader("Dane szczegółowe")
        st.dataframe(df_filtered[['Imię nazwisko', 'Skille', 'Tagi', 'NPS_2024', 'Prognozowany_NPS', 'Zmiana_NPS']])

        if st.button("Pobierz raport PDF"):
            filepath = "prepared_data/raport_nps.pdf"

            def generate_pdf(dataframe: pd.DataFrame, filename=filepath):
                pdf = FPDF()
                pdf.add_page()
                font_path = "dashboard/fonts/DejaVuSans.ttf"
                pdf.add_font("DejaVu", "", font_path, uni=True)
                pdf.set_font("DejaVu", size=12)
                pdf.cell(200, 10, txt="Raport NPS 2025", ln=True, align='C')
                pdf.ln(5)
                for _, row in dataframe.iterrows():
                    line = f"{row['Imię nazwisko']}: 2024 = {row['NPS_2024']}, 2025 = {row['Prognozowany_NPS']}, Zmiana = {row['Zmiana_NPS']}"
                    pdf.cell(0, 8, txt=line, ln=True)
                pdf.output(filename)
                return filename

            file_pdf = generate_pdf(df_filtered)
            with open(file_pdf, "rb") as f:
                st.download_button("Pobierz PDF", data=f, file_name="raport_nps.pdf", mime="application/pdf")
    else:
        st.info("Brak danych po filtrze.")

else:
    st.info("Wgraj grafik i prognozę, aby rozpocząć analizę.")

# wersja apki na dole sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align:center; color: gray;'>Wersja 1.1.2</p>", unsafe_allow_html=True)
