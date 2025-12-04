# generator raportow pdf
import pandas as pd
from fpdf import FPDF
import logging
import os

logger = logging.getLogger(__name__)

def generate_pdf(dataframe: pd.DataFrame, filename=None):
    # generuje raport pdf z danymi nps
    if filename is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        filename = os.path.join(base_dir, "prepared_data", "raport_nps.pdf")
    
    try:
        logger.info(f"generowanie raportu pdf dla {len(dataframe)} rekordow")
        pdf = FPDF()
        pdf.add_page()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        font_path = os.path.join(base_dir, "app", "assets", "fonts", "DejaVuSans.ttf")
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt="Raport NPS 2025", ln=True, align='C')
        pdf.ln(5)
        for _, row in dataframe.iterrows():
            line = f"{row['Imię nazwisko']}: 2024 = {row['NPS_2024']}, 2025 = {row['Prognozowany_NPS']}, Zmiana = {row['Zmiana_NPS']}"
            pdf.cell(0, 8, txt=line, ln=True)
        pdf.output(filename)
        logger.info(f"raport pdf wygenerowany pomyslnie {filename}")
        return filename
    except Exception as e:
        logger.error(f"blad podczas generowania pdf {e}", exc_info=True)
        raise
