import pandas as pd

# Wczytaj dane
df = pd.read_csv("DATA/nps_2024.csv")

# Funkcja obliczająca szczegóły NPS
def oblicz_nps(grupa):
    liczba = len(grupa)
    if liczba == 0:
        return pd.Series({
            "Liczba": 0,
            "Promotorzy_%": 0,
            "Neutralni_%": 0,
            "Krytycy_%": 0,
            "NPS": 0
        })

    promotorzy = len(grupa[grupa["Ocena_NPS"] >= 9])
    neutralni = len(grupa[(grupa["Ocena_NPS"] >= 7) & (grupa["Ocena_NPS"] <= 8)])
    krytycy = len(grupa[grupa["Ocena_NPS"] <= 6])

    promotorzy_pct = round((promotorzy / liczba) * 100, 2)
    neutralni_pct = round((neutralni / liczba) * 100, 2)
    krytycy_pct = round((krytycy / liczba) * 100, 2)
    nps_score = round(promotorzy_pct - krytycy_pct, 2)

    return pd.Series({
        "Liczba": liczba,
        "Promotorzy_%": promotorzy_pct,
        "Neutralni_%": neutralni_pct,
        "Krytycy_%": krytycy_pct,
        "NPS": nps_score
    })

# NPS per Skill
nps_per_skill = df.groupby("Skill").apply(oblicz_nps).reset_index()
nps_per_skill["Poziom"] = "SKILL"
nps_per_skill["Tag"] = ""
nps_per_skill["Imie_Nazwisko"] = ""

# NPS per Tag
nps_per_tag = df.groupby(["Skill", "Tag"]).apply(oblicz_nps).reset_index()
nps_per_tag["Poziom"] = "TAG"
nps_per_tag["Imie_Nazwisko"] = ""

# NPS per Agent
nps_per_agent = df.groupby("Imie_Nazwisko").apply(oblicz_nps).reset_index()
nps_per_agent["Poziom"] = "DORADCA"
nps_per_agent["Skill"] = ""
nps_per_agent["Tag"] = ""

# TOTAL – globalne podsumowanie
total_nps = oblicz_nps(df)
total_row = pd.DataFrame([{
    "Poziom": "TOTAL",
    "Skill": "",
    "Tag": "",
    "Imie_Nazwisko": "",
    **total_nps
}])

# Łączymy wszystkie dane
raport = pd.concat([nps_per_skill, nps_per_tag, nps_per_agent, total_row], ignore_index=True)

# Kolejność kolumn
raport = raport[[ 
    "Poziom", "Skill", "Tag", "Imie_Nazwisko", 
    "Liczba", "Promotorzy_%", "Neutralni_%", "Krytycy_%", "NPS"
]]

# Zapisz do pliku
raport.to_csv("DATA/nps_wynik.csv", index=False)
