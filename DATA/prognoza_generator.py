import pandas as pd

# wczytywanie danych
df = pd.read_csv("DATA/nps_2024.csv")

# liczenie liczby rekordow per stream
liczba_per_stream = df["Stream"].value_counts().sort_index()

# liczenie %
procent_per_stream = (liczba_per_stream / len(df) * 100).round(2)

# laczenie w jedna tabele
podsumowanie = pd.DataFrame({
    "Liczba_rekordow": liczba_per_stream,
    "Procent": procent_per_stream
})
# zapisanie do csv
podsumowanie.to_csv("DATA/prognoza_streamow.csv")
