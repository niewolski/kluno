import pandas as pd

# Wczytaj dane
df = pd.read_csv("DATA/nps_2024.csv")

# Zlicz liczbę rekordów per Stream
liczba_per_stream = df["Stream"].value_counts().sort_index()

# Oblicz procenty
procent_per_stream = (liczba_per_stream / len(df) * 100).round(2)

# Połącz do jednej tabeli
podsumowanie = pd.DataFrame({
    "Liczba_rekordow": liczba_per_stream,
    "Procent": procent_per_stream
})
# Zapisz do CSV
podsumowanie.to_csv("DATA/prognoza_streamow.csv")
