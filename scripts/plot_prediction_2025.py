import pandas as pd
import matplotlib.pyplot as plt
import os

# wczytanie danych z predykcji
df = pd.read_csv('prepared_data/predykcja_2025.csv')

# sortowanie po nps
df_sorted = df.sort_values('Prognozowany_NPS', ascending=False)

# dane do wykresu
labels = df_sorted['Imię nazwisko']
values = df_sorted['Prognozowany_NPS']
nps_total = df_sorted['Prognozowany_NPS_TOTAL'].iloc[0]

# rozmiar wykresu
plt.figure(figsize=(12, 6))

# slupki
bars = plt.bar(labels, values)

# linia total
plt.axhline(nps_total, color='red', linestyle='--', label=f'NPS total = {nps_total}')

# etykietyu i wyglad
plt.title('Prognozowany NPS per doradca – 2025')
plt.ylabel('NPS')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend()

# zapis wykresu
output_path = 'prepared_data/wykres_nps_2025.png'
plt.savefig(output_path)
plt.close()

print(f"Zapisano wykres do: {output_path}")
