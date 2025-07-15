import pandas as pd
import joblib
import os

# 1. Wczytanie danych
grafik = pd.read_csv('DATA_FUTURE/grafik_2025.csv')
prognoza = pd.read_csv('DATA_FUTURE/prognoza_2025.csv')
skille_2024 = pd.read_csv('prepared_data/dane_treningowe.csv')[['Imię nazwisko', 'Skille']]

# 2. Oblicz roczną liczbę godzin
grafik['Roczna_liczba_godzin'] = grafik.iloc[:, 1:].sum(axis=1)

# 3. Łączna liczba godzin
total_godziny = grafik['Roczna_liczba_godzin'].sum()

# 4. Łączna liczba spraw
total_spraw = prognoza['Liczba_rekordow'].sum()
sprawy_na_godzine = total_spraw / total_godziny
grafik['Przypisane_sprawy'] = (grafik['Roczna_liczba_godzin'] * sprawy_na_godzine).round().astype(int)

# 5. Dołącz skille z 2024
dane_pred = pd.merge(
    grafik[['Imię nazwisko', 'Roczna_liczba_godzin', 'Przypisane_sprawy']],
    skille_2024,
    on='Imię nazwisko',
    how='left'
)

# 6. Zakodowanie skillów
dane_pred['Skille_lista'] = dane_pred['Skille'].fillna('').apply(lambda x: x.split(', ') if x else [])

mlb = joblib.load('models/skille_encoder.pkl')
X_skille_df = pd.DataFrame(mlb.transform(dane_pred['Skille_lista']), columns=mlb.classes_)

# 7. Przygotowanie danych X
X_pred = pd.concat([
    dane_pred[['Roczna_liczba_godzin', 'Przypisane_sprawy']].reset_index(drop=True),
    X_skille_df.reset_index(drop=True)
], axis=1)

# 8. Wczytaj model i przewiduj
model = joblib.load('models/model_nps.pkl')
dane_pred['Prognozowany_NPS'] = model.predict(X_pred).round(2)

# 9. Oblicz totalny NPS ważony liczbą spraw
total_nps = (dane_pred['Prognozowany_NPS'] * dane_pred['Przypisane_sprawy']).sum() / dane_pred['Przypisane_sprawy'].sum()
total_nps = round(total_nps, 2)
print(f"📊 Prognozowany NPS (total): {total_nps}")

# 10. Dodaj kolumnę pomocniczą z wartością total
dane_pred['Prognozowany_NPS_TOTAL'] = total_nps

# 11. Zapisz wyniki
output_path = 'prepared_data/predykcja_2025.csv'
dane_pred.to_csv(output_path, index=False)
print(f"✅ Prognoza zapisana do: {output_path}")
