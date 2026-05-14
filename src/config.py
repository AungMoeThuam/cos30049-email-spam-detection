"""Configuration for email spam detection project."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Data directories:
# - Raw CSV files → data/raw/
# - Processed CSV files → data/processed/
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DATA_PATHS = {
    "enron": RAW_DATA_DIR / "enron_spam.csv",
    "enron_2": RAW_DATA_DIR / "enron_spam_2.csv",
    "spam_assassin": RAW_DATA_DIR / "spam_assassin.csv",
    "spam_assassin_2": RAW_DATA_DIR / "spam_assassin_2.csv",
    "email_spam_dataset": RAW_DATA_DIR / "email_spam_dataset.csv",
    "phishing_email":RAW_DATA_DIR / "phishing_email.csv",
    "sms_spam_dataset": RAW_DATA_DIR / "sms_spam_dataset.csv",
    "spam_email_detection_dataset": RAW_DATA_DIR / "spam_email_detection_dataset.csv",
    "250K_email_dataset": RAW_DATA_DIR / "250K+_email_dataset.csv",
    "190K_email_content": RAW_DATA_DIR / "190K+_email_content.csv",
    "NLP_spam_ham_email": RAW_DATA_DIR / "NLP_spam_ham_email.csv",
    "ling_spam": RAW_DATA_DIR / "ling_spam.csv",
    "nigerian_fraud": RAW_DATA_DIR / "nigerian_fraud.csv",
    "nazario": RAW_DATA_DIR / "nazario.csv",
    "CEAS_08": RAW_DATA_DIR / "CEAS_08.csv",
}

MODEL_OUTPUT_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"


def setup_directories():
    """Create all required project directories if they don't exist."""
    for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODEL_OUTPUT_DIR, RESULTS_DIR]:
        os.makedirs(dir_path, exist_ok=True)


setup_directories()