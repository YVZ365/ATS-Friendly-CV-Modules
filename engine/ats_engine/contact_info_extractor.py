"""
ats_engine.contact_info_extractor — CV iletişim bilgisi çıkarımı.

Email, telefon, LinkedIn URL'si ve şehir bilgilerini regex/heuristik ile bulur.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import re

_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{8,}\d)")
_LINKEDIN_RE = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9-_%]+/?", re.IGNORECASE)
_CITY_LABEL_RE = re.compile(r"(?:city|location|şehir|sehir|konum)\s*[:|-]\s*([A-Za-zÇĞİÖŞÜçğıöşü .'-]+)", re.IGNORECASE)
_CITY_HINTS = (
    "istanbul",
    "ankara",
    "izmir",
    "bursa",
    "antalya",
    "kocaeli",
    "london",
    "berlin",
    "amsterdam",
    "paris",
    "new york",
    "san francisco",
    "toronto",
    "dubai",
)


def _normalize_phone(value: str) -> str:
    digits = re.sub(r"[^\d+]", "", value)
    if digits.startswith("00"):
        digits = f"+{digits[2:]}"
    return digits


def _detect_city(cv_text: str) -> str | None:
    labeled = _CITY_LABEL_RE.search(cv_text or "")
    if labeled:
        return labeled.group(1).strip(" ,")

    head = "\n".join((cv_text or "").splitlines()[:6]).lower()
    for city in _CITY_HINTS:
        if city in head:
            return city.title()
    return None


def extract_contact_info(cv_text: str) -> dict:
    """CV metninden temel iletişim alanlarını çıkarır."""
    emails = _EMAIL_RE.findall(cv_text or "")
    phones = [_normalize_phone(item) for item in _PHONE_RE.findall(cv_text or "")]
    linkedin_matches = [match.group(0) for match in _LINKEDIN_RE.finditer(cv_text or "")]
    linkedin = linkedin_matches[0] if linkedin_matches else None
    if linkedin and not linkedin.startswith("http"):
        linkedin = f"https://{linkedin}"

    unique_phones: list[str] = []
    for phone in phones:
        if phone not in unique_phones:
            unique_phones.append(phone)

    return {
        "email": emails[0] if emails else None,
        "phone": unique_phones[0] if unique_phones else None,
        "linkedin": linkedin,
        "city": _detect_city(cv_text),
        "emails": emails,
        "phones": unique_phones,
    }
