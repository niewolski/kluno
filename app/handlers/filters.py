# filtrowanie danych
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def get_filter_options(df):
    # pobiera opcje do filtrowania
    wszyscy_doradcy = sorted(df['Imię nazwisko'].dropna().unique())
    wszystkie_skille = sorted({s for row in df['Skille'].dropna().apply(lambda x: x.split(', ')) for s in row})
    wszystkie_tagi = sorted({t.strip() for tags in df['Tagi'].dropna() for t in tags.split(',')})
    return wszyscy_doradcy, wszystkie_skille, wszystkie_tagi

def apply_filters(df, wybrani_doradcy=None, wybrane_skille=None, wybrane_tagi=None):
    # stosuje filtry do danych
    df_filtered = df.copy()
    initial_count = len(df_filtered)
    
    if wybrani_doradcy:
        df_filtered = df_filtered[df_filtered['Imię nazwisko'].isin(wybrani_doradcy)]
        logger.info(f"filtrowanie po doradcach {len(wybrani_doradcy)} wybranych {len(df_filtered)} rekordow po filtrze")
    
    if wybrane_skille:
        df_filtered = df_filtered[df_filtered['Skille'].fillna('').apply(lambda x: any(skill in x for skill in wybrane_skille))]
        logger.info(f"filtrowanie po skillach {len(wybrane_skille)} wybranych {len(df_filtered)} rekordow po filtrze")
    
    if wybrane_tagi:
        df_filtered = df_filtered[df_filtered['Tagi'].fillna('').apply(lambda x: any(tag in x for tag in wybrane_tagi))]
        logger.info(f"filtrowanie po tagach {len(wybrane_tagi)} wybranych {len(df_filtered)} rekordow po filtrze")
    
    if len(df_filtered) != initial_count:
        logger.info(f"filtrowanie zakonczone {initial_count} -> {len(df_filtered)} rekordow")
    
    return df_filtered
