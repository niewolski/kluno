# konfiguracja logowania
import logging
import os
from datetime import datetime

def setup_logging():
    # ustawia logowanie do pliku i konsoli
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    logger.info("="*50)
    logger.info("Aplikacja Kluno NPS Dashboard uruchomiona")
    logger.info(f"Data uruchomienia: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return logger
