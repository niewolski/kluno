# logika analizy nps predykcje
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def calculate_annual_hours(grafik):
    # liczy roczna liczbe godzin dla kazdego doradcy
    grafik['Roczna_liczba_godzin'] = grafik.iloc[:, 1:].select_dtypes(include='number').sum(axis=1)
    return grafik

def assign_cases(grafik, prognoza):
    # przypisuje sprawy do doradcow na podstawie godzin
    total_godziny = grafik['Roczna_liczba_godzin'].sum()
    total_spraw = prognoza['Liczba_rekordow'].sum()
    sprawy_na_godzine = total_spraw / total_godziny
    logger.info(f"calkowita liczba godzin {total_godziny} spraw na godzine {sprawy_na_godzine:.2f}")
    
    grafik['Przypisane_sprawy'] = (grafik['Roczna_liczba_godzin'] * sprawy_na_godzine).round().astype(int)
    logger.info(f"przypisano sprawy do {len(grafik)} doradcow")
    return grafik

def prepare_prediction_data(grafik, df_2024, encoder):
    # przygotowuje dane do predykcji nps
    logger.info("laczenie danych z danymi historycznymi")
    df_pred = pd.merge(
        grafik[['Imię nazwisko', 'Roczna_liczba_godzin', 'Przypisane_sprawy']],
        df_2024[['Imię nazwisko', 'Skille']],
        on='Imię nazwisko', how='left'
    )
    logger.info(f"polaczono dane dla {len(df_pred)} doradcow")

    logger.info("przygotowanie danych do predykcji")
    df_pred['Skille_lista'] = df_pred['Skille'].fillna('').apply(lambda x: x.split(', ') if x else [])
    X_skille = pd.DataFrame(encoder.transform(df_pred['Skille_lista']), columns=encoder.classes_)
    X_pred = pd.concat([df_pred[['Roczna_liczba_godzin', 'Przypisane_sprawy']].reset_index(drop=True), X_skille], axis=1)
    
    return df_pred, X_pred

def predict_nps(df_pred, X_pred, model):
    # robi predykcje nps
    logger.info("wykonywanie predykcji nps")
    df_pred['Prognozowany_NPS'] = model.predict(X_pred).round(2)
    logger.info(f"wygenerowano prognozy nps dla {len(df_pred)} doradcow")
    logger.info(f"sredni prognozowany nps {df_pred['Prognozowany_NPS'].mean():.2f}")
    return df_pred

def merge_with_historical_data(df_pred, df_2024):
    # laczy dane predykcyjne z danymi historycznymi
    logger.info("finalne laczenie danych")
    df = pd.merge(df_pred, df_2024, on='Imię nazwisko', how='left')
    df.drop(columns=['Skille_x'], errors='ignore', inplace=True)
    df.rename(columns={'Skille_y': 'Skille'}, inplace=True)
    df['Zmiana_NPS'] = (df['Prognozowany_NPS'] - df['NPS_2024']).round(2)
    return df

def run_analysis(uploaded_grafik, uploaded_prognoza, df_2024, model, encoder):
    # glowna funkcja robiaca cala analize
    try:
        logger.info("rozpoczecie analizy nps")
        logger.info(f"wczytywanie grafik {uploaded_grafik.name}")
        grafik = pd.read_csv(uploaded_grafik)
        logger.info(f"wczytano {len(grafik)} rekordow z grafiku")
        
        logger.info(f"wczytywanie prognozy {uploaded_prognoza.name}")
        prognoza = pd.read_csv(uploaded_prognoza)
        logger.info(f"wczytano {len(prognoza)} rekordow z prognozy")

        grafik = calculate_annual_hours(grafik)
        grafik = assign_cases(grafik, prognoza)
        df_pred, X_pred = prepare_prediction_data(grafik, df_2024, encoder)
        df_pred = predict_nps(df_pred, X_pred, model)
        df = merge_with_historical_data(df_pred, df_2024)
        
        logger.info("analiza zakonczona pomyslnie")
        return df
        
    except Exception as e:
        logger.error(f"blad podczas analizy {e}", exc_info=True)
        raise

def calculate_nps_metrics(df):
    # liczy metryki nps dla 2024 i 2025
    nps_total_2025 = (df['Prognozowany_NPS'] * df['Przypisane_sprawy']).sum() / df['Przypisane_sprawy'].sum()
    nps_total_2024 = (df['NPS_2024'] * df['Przypisane_sprawy_2024']).sum() / df['Przypisane_sprawy_2024'].sum()
    return nps_total_2025, nps_total_2024
