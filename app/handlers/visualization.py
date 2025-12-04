# generowanie wykresow
import pandas as pd
import plotly.express as px
import streamlit as st
import logging

logger = logging.getLogger(__name__)

def create_nps_2025_chart(df_filtered, nps_total_2025):
    # tworzy wykres nps 2025
    fig = px.bar(df_filtered.sort_values('Prognozowany_NPS', ascending=False),
                 x='Imię nazwisko', y='Prognozowany_NPS', color='Prognozowany_NPS',
                 color_continuous_scale='RdYlGn', title="Prognozowany NPS 2025")
    fig.add_hline(y=nps_total_2025, line_dash='dash', line_color='red')
    return fig

def create_nps_2024_chart(df_filtered, nps_total_2024):
    # tworzy wykres nps 2024
    fig = px.bar(df_filtered.sort_values('NPS_2024', ascending=False),
                 x='Imię nazwisko', y='NPS_2024', color='NPS_2024',
                 color_continuous_scale='RdYlGn', title="Rzeczywisty NPS 2024")
    fig.add_hline(y=nps_total_2024, line_dash='dash', line_color='blue')
    return fig

def create_comparison_chart(df_filtered):
    # tworzy wykres porownawczy 2024 vs 2025
    df_melted = df_filtered.melt(id_vars='Imię nazwisko',
                                 value_vars=['NPS_2024', 'Prognozowany_NPS'],
                                 var_name='Rok', value_name='NPS')
    fig = px.bar(df_melted, x='Imię nazwisko', y='NPS', color='Rok',
                 barmode='group', title='Porownanie NPS 2024 vs 2025')
    return fig

def create_change_chart(df_filtered):
    # tworzy wykres zmiany nps
    fig = px.bar(df_filtered.sort_values('Zmiana_NPS', ascending=False),
                 x='Imię nazwisko', y='Zmiana_NPS',
                 color='Zmiana_NPS', color_continuous_scale='RdYlGn',
                 title='Zmiana NPS: 2025 - 2024')
    return fig

def render_chart(widok, df_filtered, nps_total_2025, nps_total_2024):
    # rysuje odpowiedni wykres w zaleznosci od widoku
    logger.info(f"wybrano widok {widok}")
    
    if widok == "2025":
        fig = create_nps_2025_chart(df_filtered, nps_total_2025)
    elif widok == "2024":
        fig = create_nps_2024_chart(df_filtered, nps_total_2024)
    elif widok == "Porównanie":
        fig = create_comparison_chart(df_filtered)
    elif widok == "Zmiana NPS":
        fig = create_change_chart(df_filtered)
    else:
        return None
    
    st.plotly_chart(fig, use_container_width=True)
