import csv
import random
from datetime import datetime, timedelta

# lista doradcow
imiona_nazwiska = [
    "Anna Kowalska", "Piotr Nowak", "Maria Wiśniewska", "Tomasz Wójcik",
    "Katarzyna Kozłowska", "Michał Jankowski", "Agnieszka Mazur", "Jakub Krawczyk",
    "Monika Piotrowska", "Paweł Grabowski", "Joanna Nowakowska", "Marcin Pawłowski",
    "Magdalena Michalska", "Krzysztof Adamczyk", "Aleksandra Dudek", "Łukasz Zając",
    "Ewelina Wieczorek", "Bartosz Jabłoński", "Natalia Sobczak", "Damian Król"
]

# komentarze
komentarze = [
    "Świetna obsługa, bardzo dziękuję!",
    "Nie mam zastrzeżeń – wszystko sprawnie.",
    "Konsultant był pomocny i miły.",
    "Zdecydowanie polecam – profesjonalne podejście.",
    "Obsługa na najwyższym poziomie.",
    "Dostałem odpowiedź na wszystkie pytania.",
    "Kontakt szybki i konkretny.",
    "Bardzo dobra rozmowa, dziękuję.",
    "Miło, rzeczowo, konkretnie – super!",
    "Rozwiązano mój problem od razu.",
    "Obsługa poprawna, ale bez zachwytu.",
    "Było w porządku, choć bez fajerwerków.",
    "Neutralna rozmowa, nie mam uwag.",
    "Nie było problemu, ale też bez zaangażowania.",
    "Zwyczajna rozmowa – nic szczególnego.",
    "Rozmowa trwała długo, ale zakończona sukcesem.",
    "Nie jestem w pełni usatysfakcjonowany.",
    "Odpowiedź wymagała doprecyzowania.",
    "Nie wszystkie kwestie zostały wyjaśnione.",
    "Mogło być lepiej, ale doceniam starania.",
    "Długo czekałem na połączenie.",
    "Nie udało się rozwiązać mojego problemu.",
    "Brak konkretnej odpowiedzi.",
    "Zbyt ogólne informacje – nie pomogło.",
    "Konsultant był nieprzygotowany.",
    "Rozmowa nieprzyjemna i nerwowa.",
    "Niezadowolony z poziomu obsługi.",
    "Zgłoszenie zostało zignorowane.",
    "Otrzymałem sprzeczne informacje.",
    "Brak empatii i zrozumienia.",
    "Czułem się zbywany.",
    "Świetne podejście – aż miło było rozmawiać!",
    "Rewelacyjna pomoc – problem rozwiązany w minutę.",
    "Doceniam szybkie działanie.",
    "Bardzo rzeczowo i konkretnie.",
    "Konsultant z wiedzą i empatią.",
    "Jestem bardzo zadowolony z rozmowy.",
    "Kontakt pierwsza klasa!",
    "Zaskakująco dobra obsługa.",
    "W końcu ktoś mi pomógł!",
    "Pomocna rozmowa, ale trwała zbyt długo.",
    "Miło, ale nie wszystko zostało wyjaśnione.",
    "Trochę chaotyczna obsługa.",
    "Długi czas oczekiwania, ale reszta ok.",
    "Konsultant był wyrozumiały, ale bez konkretów.",
    "Dużo słów, mało rozwiązań.",
    "Nie polecam – strata czasu.",
    "Zignorowano moje pytania.",
    "Obsługa była nieuprzejma.",
    "Nie wrócę więcej – bardzo słabo."
]

# tagi do skilli
skill_tag_map = {
    "Skill_A": ["TAG_1", "TAG_2", "TAG_3", "TAG_4"],
    "Skill_B": ["TAG_5", "TAG_6", "TAG_7", "TAG_8"],
    "Skill_C": ["TAG_9", "TAG_10", "TAG_11", "TAG_12"],
    "Skill_D": ["TAG_13", "TAG_14", "TAG_15", "TAG_16"],
    "Skill_E": ["TAG_17", "TAG_18", "TAG_19", "TAG_20"],
    "Skill_F": ["TAG_21", "TAG_22", "TAG_23", "TAG_24"],
    "Skill_G": ["TAG_25", "TAG_26", "TAG_27", "TAG_28"],
    "Skill_H": ["TAG_29", "TAG_30", "TAG_31", "TAG_32"]
}

# skille do strumieni
skill_stream_map = {
    "Skill_A": "Stream1", "Skill_B": "Stream1",
    "Skill_C": "Stream2", "Skill_D": "Stream2",
    "Skill_E": "Stream3", "Skill_F": "Stream3",
    "Skill_G": "Stream4", "Skill_H": "Stream4"
}

# skille dla oosb
osoba_skill_map = {
    "Anna Kowalska": ("Skill_A", "Skill_B"), "Piotr Nowak": ("Skill_A", "Skill_B"),
    "Maria Wiśniewska": ("Skill_A", "Skill_B"), "Tomasz Wójcik": ("Skill_A", "Skill_B"),
    "Katarzyna Kozłowska": ("Skill_C", "Skill_D"), "Michał Jankowski": ("Skill_C", "Skill_D"),
    "Agnieszka Mazur": ("Skill_C", "Skill_D"), "Jakub Krawczyk": ("Skill_C", "Skill_D"),
    "Monika Piotrowska": ("Skill_E", "Skill_F"), "Paweł Grabowski": ("Skill_E", "Skill_F"),
    "Joanna Nowakowska": ("Skill_E", "Skill_F"), "Marcin Pawłowski": ("Skill_E", "Skill_F"),
    "Magdalena Michalska": ("Skill_G", "Skill_H"), "Krzysztof Adamczyk": ("Skill_G", "Skill_H"),
    "Aleksandra Dudek": ("Skill_G", "Skill_H"), "Łukasz Zając": ("Skill_G", "Skill_H"),
    "Ewelina Wieczorek": ("Skill_A", "Skill_B"), "Bartosz Jabłoński": ("Skill_A", "Skill_B"),
    "Natalia Sobczak": ("Skill_A", "Skill_B"), "Damian Król": ("Skill_A", "Skill_B")
}

# losowanei dat
def generuj_losowa_date():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

# liczba rekordow
TOTAL = 2000

# zakres losowania w % per stream
stream_percent_ranges = {
    "Stream1": (15, 25),
    "Stream2": (30, 40),
    "Stream3": (10, 20),
    "Stream4": (25, 35),
}

# losowanie do 100%
while True:
    stream_percents = {
        stream: random.randint(min_p, max_p)
        for stream, (min_p, max_p) in stream_percent_ranges.items()
    }
    if sum(stream_percents.values()) == 100:
        break

# % na liczbe rekordow
stream_targets = {
    stream: round((percent / 100) * TOTAL)
    for stream, percent in stream_percents.items()
}

# grupowanie osob wg streamow
stream_osoby = {
    "Stream1": [o for o in imiona_nazwiska if any(s in ("Skill_A", "Skill_B") for s in osoba_skill_map[o])],
    "Stream2": [o for o in imiona_nazwiska if any(s in ("Skill_C", "Skill_D") for s in osoba_skill_map[o])],
    "Stream3": [o for o in imiona_nazwiska if any(s in ("Skill_E", "Skill_F") for s in osoba_skill_map[o])],
    "Stream4": [o for o in imiona_nazwiska if any(s in ("Skill_G", "Skill_H") for s in osoba_skill_map[o])],
}

# generowanie danych nps
dane = []
id_counter = 1
for stream, target_count in stream_targets.items():
    for _ in range(target_count):
        osoba = random.choice(stream_osoby[stream])
        skill_options = [s for s in osoba_skill_map[osoba] if skill_stream_map[s] == stream]
        skill = random.choice(skill_options)
        tag = random.choice(skill_tag_map[skill])
        komentarz = random.choice(komentarze)
        data = generuj_losowa_date()

        dane.append({
            "ID": id_counter,
            "Imie_Nazwisko": osoba,
            "Ocena_NPS": random.randint(0, 10),
            "Data": data,
            "Komentarz": komentarz,
            "Skill": skill,
            "Tag": tag,
            "Stream": stream
        })
        id_counter += 1

# zapisywanie do csv
with open("DATA/nps_2024.csv", 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ID', 'Imie_Nazwisko', 'Ocena_NPS', 'Data', 'Komentarz', 'Skill', 'Tag', 'Stream']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dane)
