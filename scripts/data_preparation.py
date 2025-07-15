import pandas as pd
import os

# Ścieżki
grafik_path = 'DATA/grafik_2024.csv'
nps_path = 'DATA/nps_2024.csv'
prognoza_path = 'DATA/prognoza_streamow.csv'
output_path = 'prepared_data/dane_treningowe.csv'

# Wczytanie danych
grafik = pd.read_csv(grafik_path)
nps = pd.read_csv(nps_path)
prognoza = pd.read_csv(prognoza_path)

# --- 1. Obliczenie godzin i spraw ---
grafik['Roczna_liczba_godzin'] = grafik.iloc[:, 1:].sum(axis=1)
total_godziny = grafik['Roczna_liczba_godzin'].sum()
total_spraw = prognoza['Liczba_rekordow'].sum()
sprawy_na_godzine = total_spraw / total_godziny
grafik['Przypisane_sprawy'] = (grafik['Roczna_liczba_godzin'] * sprawy_na_godzine).round().astype(int)

# --- 2. Obliczenie prawdziwego NPS ---
def policz_nps(grupa):
    total = len(grupa)
    if total == 0:
        return pd.Series({'NPS': None})
    promotorzy = (grupa['Ocena_NPS'] >= 9).sum() / total * 100
    krytycy = (grupa['Ocena_NPS'] <= 6).sum() / total * 100
    return pd.Series({'NPS': round(promotorzy - krytycy, 2)})

nps_roczny = nps.groupby('Imie_Nazwisko').apply(policz_nps).reset_index()

# --- 3. Skille per doradca ---
skille_doradcow = nps[['Imie_Nazwisko', 'Skill']].drop_duplicates()
skille_zbiorcze = skille_doradcow.groupby('Imie_Nazwisko')['Skill'].apply(lambda x: ', '.join(sorted(x.unique()))).reset_index()
skille_zbiorcze.columns = ['Imię nazwisko', 'Skille']

# --- 4. Tagi per doradca ---
if 'Tag' in nps.columns:
    tagi_doradcow = nps[['Imie_Nazwisko', 'Tag']].dropna().drop_duplicates()
    tagi_zbiorcze = tagi_doradcow.groupby('Imie_Nazwisko')['Tag'].apply(lambda x: ', '.join(sorted(x.unique()))).reset_index()
    tagi_zbiorcze.columns = ['Imię nazwisko', 'Tagi']
else:
    tagi_zbiorcze = pd.DataFrame(columns=['Imię nazwisko', 'Tagi'])

# --- 5. Połączenie wszystkich danych ---
dane_treningowe = pd.merge(
    grafik[['Imię nazwisko', 'Roczna_liczba_godzin', 'Przypisane_sprawy']],
    nps_roczny,
    left_on='Imię nazwisko',
    right_on='Imie_Nazwisko',
    how='left'
).drop(columns=['Imie_Nazwisko'])

dane_treningowe = pd.merge(
    dane_treningowe,
    skille_zbiorcze,
    on='Imię nazwisko',
    how='left'
)

dane_treningowe = pd.merge(
    dane_treningowe,
    tagi_zbiorcze,
    on='Imię nazwisko',
    how='left'
)

# --- 6. Zapis do pliku ---
if not os.path.exists('prepared_data'):
    os.makedirs('prepared_data')

dane_treningowe.to_csv(output_path, index=False)
print(f"✅ Zapisano dane do: {output_path}")
