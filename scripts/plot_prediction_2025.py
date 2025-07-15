import pandas as pd
import matplotlib.pyplot as plt
import os

# Wczytaj dane z predykcji
df = pd.read_csv('prepared_data/predykcja_2025.csv')

# Sortuj po NPS
df_sorted = df.sort_values('Prognozowany_NPS', ascending=False)

# Dane do wykresu
labels = df_sorted['Imię nazwisko']
values = df_sorted['Prognozowany_NPS']
nps_total = df_sorted['Prognozowany_NPS_TOTAL'].iloc[0]

# Rozmiar wykresu
plt.figure(figsize=(12, 6))

# Słupki
bars = plt.bar(labels, values)

# Linia total
plt.axhline(nps_total, color='red', linestyle='--', label=f'NPS total = {nps_total}')

# Etykiety i wygląd
plt.title('Prognozowany NPS per doradca – 2025')
plt.ylabel('NPS')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend()

# Zapis
output_path = 'prepared_data/wykres_nps_2025.png'
plt.savefig(output_path)
plt.close()

print(f"✅ Zapisano wykres do: {output_path}")
