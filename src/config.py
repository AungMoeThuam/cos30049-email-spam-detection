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
    "enron": DATA_DIR / "enron_spam.csv",
    "enron_2": DATA_DIR / "enron_spam_2.csv",
    "spam_assassin": DATA_DIR / "spam_assassin.csv",
    "spam_assassin_2": DATA_DIR / "spam_assassin_2.csv",
    "email_spam_dataset": DATA_DIR / "email_spam_dataset.csv",
    "phishing_email": DATA_DIR / "phishing_email.csv",
    "sms_spam_dataset": DATA_DIR / "sms_spam_dataset.csv",
    "spam_email_detection_dataset": DATA_DIR / "spam_email_detection_dataset.csv",
    "250K_email_dataset": DATA_DIR / "250K+_email_dataset.csv",
    "190K_email_content": DATA_DIR / "190K+_email_content.csv",
    "NLP_spam_ham_email": DATA_DIR / "NLP_spam_ham_email.csv",
    "ling_spam": DATA_DIR / "ling_spam.csv",
    "nigerian_fraud": DATA_DIR / "nigerian_fraud.csv",
    "nazario": DATA_DIR / "nazario.csv",
    "CEAS_08": DATA_DIR / "CEAS_08.csv",
}

MODEL_OUTPUT_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"