"""Text preprocessing utilities for email spam detection."""

import re
from html.parser import HTMLParser

class TextPreprocessor:
    def __init__(self):
        self.text = ""

    def strip_html_tags(self, html_text):
        self.text = re.sub(r"<[^>]+>", "", html_text)
        return self

    def replace_phone_numbers(self, html_text):
        phone_re = r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}"
        self.text = re.sub(phone_re, " [Phone Number] ", html_text)
        return self

    def replace_urls(self, html_text):
        self.text = re.sub(r'http[s]?://\S+', ' [URL] ', html_text)
        return self

    def normalize_whitespace(self, html_text):
        self.text = re.sub(r"\s+", " ", html_text).strip()
        return self

class HTMLTextExtractor(HTMLParser):
    """Strip HTML tags, skip style/script blocks, extract visible text only."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ("style", "script"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag.lower() in ("style", "script"):
            self._skip = False

    def handle_data(self, data):
        if self._skip:
            return
        stripped = data.strip()
        if stripped:
            self.text_parts.append(stripped)

    def get_text(self):
        return " ".join(self.text_parts)


def clean_text(text):
    """Clean and normalize text.

    Performs:
    - URL replacement with <URL> token
    - Email replacement with <EMAIL> token
    - Number replacement with <NUM> token
    - Punctuation removal
    - Lowercase conversion
    - Whitespace normalization

    Args:
        text: Raw text string

    Returns:
        Cleaned text string
    """
    if not isinstance(text, str):
        return ""  # Return empty string for non-string inputs
    
    # Convert to lowercase for consistency
    text = text.lower()  

    # Replace URLs with [URL] token
    text = re.sub(r'http[s]?://\S+', ' [URL] ', text)  

    # Replace email addresses with [EMAIL] token
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' [EMAIL] ', text)  

    # Replace standalone numbers with [NUM] token
    text = re.sub(r'\b\d+\b', ' [NUM] ', text)  

    # Remove punctuation (keep [URL], [EMAIL], [NUM] tokens)
    text = re.sub(r'[^\w\s<>]', '', text)  

    # Normalize whitespace (multiple spaces to single)
    text = re.sub(r"\s+", " ", text)  

    # Remove leading/trailing whitespace
    text = text.strip()  
    return text


def parse_eml(filepath):
    """Parse .eml email file and extract subject and body.

    Args:
        filepath: Path to .eml file

    Returns:
        tuple: (subject, body)
    """
    import email

    with open(filepath, "rb") as f:
        msg = email.message_from_bytes(f.read())

    subject = msg.get("Subject", "")

    plain_body = ""
    html_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            decoded = payload.decode("utf-8", errors="ignore")
            if content_type == "text/plain" and not plain_body:
                plain_body = decoded
            elif content_type == "text/html" and not html_body:
                html_body = decoded
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            plain_body = payload.decode("utf-8", errors="ignore")

    if plain_body.strip():
        body = plain_body
    else:
        extractor = HTMLTextExtractor()
        extractor.feed(html_body)
        body = extractor.get_text()

    body = re.sub(r"\s+", " ", body).strip()
    return subject, body


def prepare_email_text(subject, body):
    """Combine subject and body for model prediction.

    Args:
        subject: Email subject
        body: Email body

    Returns:
        Combined text string ready for prediction
    """
    eml_text = (str(subject) + " " + str(body)).lower()
    eml_text = re.sub(r"\s+", " ", eml_text).strip()
    return eml_text
