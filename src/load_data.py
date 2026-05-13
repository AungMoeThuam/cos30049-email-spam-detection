"""Data loading utilities for email spam datasets."""

import pandas as pd


def load_enron_spam(filepath, encoding="utf-8"):
    """Load the Enron spam dataset.

    Expected columns: 'Message ID', 'Subject', 'Message', 'Spam/Ham', 'Date'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.drop(columns=["Message ID", "Date"], errors="ignore")
    df = df.dropna(subset=["Message"])
    df["Subject"] = df["Subject"].fillna("")

    df["Spam/Ham"] = df["Spam/Ham"].astype(str).str.strip().str.lower()
    df["label"] = df["Spam/Ham"].map({"ham": 0, "spam": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["Subject"].astype(str) + " " + df["Message"].astype(str)

    return df[["text", "label"]]


def load_enron_spam_2(filepath, encoding="utf-8"):
    """Load the Enron spam dataset (version 2).

    Expected columns: 'subject', 'body', 'label'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.dropna(subset=["body"])
    df["subject"] = df["subject"].fillna("")

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["subject"].astype(str) + " " + df["body"].astype(str)

    return df[["text", "label"]]


def load_spam_assassin(filepath, encoding="utf-8"):
    """Load the SpamAssassin dataset.

    Expected columns: 'text', 'target'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.rename(columns={"target": "label"})
    df["label"] = df["label"].map({0: 0, 1: 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    return df[["text", "label"]]


def load_spam_assassin_2(filepath, encoding="utf-8"):
    """Load the SpamAssassin dataset (version 2).

    Expected columns: 'sender', 'receiver', 'date', 'subject', 'body', 'label', 'urls'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.dropna(subset=["body"])
    df["subject"] = df["subject"].fillna("")

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["subject"].astype(str) + " " + df["body"].astype(str)

    return df[["text", "label"]]


def load_email_spam_dataset(filepath, encoding="utf-8"):
    """Load the email spam dataset.

    Expected columns: 'email_text', 'label'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.rename(columns={"email_text": "text"})

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    return df[["text", "label"]]


def load_phishing_email(filepath, encoding="utf-8"):
    """Load the phishing email dataset.

    Expected columns: 'text_combined', 'label'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.rename(columns={"text_combined": "text"})

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    return df[["text", "label"]]


def load_sms_spam_dataset(filepath, encoding="utf-8"):
    """Load the SMS spam dataset.

    Expected columns: 'v1' (label), 'v2' (text)

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.rename(columns={"v1": "label", "v2": "text"})

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    return df[["text", "label"]]


def load_spam_email_detection_dataset(filepath, encoding="utf-8"):
    """Load the spam email detection dataset.

    Expected columns: 'subject', 'email_text', 'label', and others

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.dropna(subset=["email_text"])
    df["subject"] = df["subject"].fillna("")

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["subject"].astype(str) + " " + df["email_text"].astype(str)

    return df[["text", "label"]]


def load_250K_email_dataset(filepath, encoding="utf-8"):
    """Load the 250K+ email dataset.

    Expected columns: 'label', 'text'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    return df[["text", "label"]]


def load_190K_email_content(filepath, encoding="utf-8"):
    """Load the 190K+ email content dataset.

    Expected columns: 'label', 'text'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    return df[["text", "label"]]


def load_NLP_spam_ham_email(filepath, encoding="utf-8"):
    """Load the NLP spam ham email dataset.

    Expected columns: 'text', 'spam'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.rename(columns={"spam": "label"})

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["text", "label"])
    df["label"] = df["label"].astype(int)

    return df[["text", "label"]]


def load_ling_spam(filepath, encoding="utf-8"):
    """Load the ling spam dataset.

    Expected columns: 'subject', 'message', 'label'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.dropna(subset=["message"])
    df["subject"] = df["subject"].fillna("")

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["subject"].astype(str) + " " + df["message"].astype(str)

    return df[["text", "label"]]


def load_nigerian_fraud(filepath, encoding="utf-8"):
    """Load the Nigerian fraud dataset.

    Expected columns: 'sender', 'receiver', 'date', 'subject', 'body', 'urls', 'label'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.dropna(subset=["body"])
    df["subject"] = df["subject"].fillna("")

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["subject"].astype(str) + " " + df["body"].astype(str)

    return df[["text", "label"]]


def load_nazario(filepath, encoding="utf-8"):
    """Load the Nazario dataset.

    Expected columns: 'sender', 'receiver', 'date', 'subject', 'body', 'urls', 'label'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.dropna(subset=["body"])
    df["subject"] = df["subject"].fillna("")

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["subject"].astype(str) + " " + df["body"].astype(str)

    return df[["text", "label"]]


def load_CEAS_08(filepath, encoding="utf-8"):
    """Load the CEAS 08 dataset.

    Expected columns: 'sender', 'receiver', 'date', 'subject', 'body', 'label', 'urls'

    Returns:
        DataFrame with columns: 'text', 'label'
    """
    df = pd.read_csv(filepath, encoding=encoding)
    df = df.dropna(subset=["body"])
    df["subject"] = df["subject"].fillna("")

    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["label"] = df["label"].map({"ham": 0, "spam": 1, "0": 0, "1": 1})
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    df["text"] = df["subject"].astype(str) + " " + df["body"].astype(str)

    return df[["text", "label"]]