"""
ats_engine.experience_year_extractor — Tarih aralıklarından toplam deneyim yılı çıkarımı.

CV metnindeki yıl/ay bazlı deneyim aralıklarını yakalar, çakışan dönemleri
birleştirir ve toplam deneyimi ay/yıl cinsinden hesaplar.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import re
from datetime import date

_MONTHS = {
    "jan": 1,
    "january": 1,
    "oca": 1,
    "ocak": 1,
    "feb": 2,
    "february": 2,
    "şub": 2,
    "sub": 2,
    "şubat": 2,
    "subat": 2,
    "mar": 3,
    "march": 3,
    "mart": 3,
    "apr": 4,
    "april": 4,
    "nis": 4,
    "nisan": 4,
    "may": 5,
    "mayıs": 5,
    "mayis": 5,
    "jun": 6,
    "june": 6,
    "haz": 6,
    "haziran": 6,
    "jul": 7,
    "july": 7,
    "tem": 7,
    "temmuz": 7,
    "aug": 8,
    "august": 8,
    "ağu": 8,
    "agu": 8,
    "ağustos": 8,
    "agustos": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "eyl": 9,
    "eylül": 9,
    "eylul": 9,
    "oct": 10,
    "october": 10,
    "eki": 10,
    "ekim": 10,
    "nov": 11,
    "november": 11,
    "kas": 11,
    "kasım": 11,
    "kasim": 11,
    "dec": 12,
    "december": 12,
    "ara": 12,
    "aralık": 12,
    "aralik": 12,
}
_PRESENT = {"present", "current", "now", "halen", "devam", "ongoing"}
_RANGE_RE = re.compile(
    r"(?P<start>(?:[A-Za-zÇĞİÖŞÜçğıöşü]+ +)?\d{4})\s*(?:-|–|—|to|until)\s*(?P<end>present|current|now|halen|devam|ongoing|(?:[A-Za-zÇĞİÖŞÜçğıöşü]+ +)?\d{4})",
    re.IGNORECASE,
)


def _month_index(value: date) -> int:
    return value.year * 12 + value.month


def _parse_date_token(token: str, *, is_end: bool, today: date) -> date | None:
    cleaned = " ".join((token or "").strip().lower().split())
    if not cleaned:
        return None
    if cleaned in _PRESENT:
        return date(today.year, today.month, 1)

    parts = cleaned.split()
    if len(parts) == 1 and parts[0].isdigit() and len(parts[0]) == 4:
        year = int(parts[0])
        month = 12 if is_end else 1
        return date(year, month, 1)

    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 4:
        month = _MONTHS.get(parts[0])
        if month is None:
            return None
        return date(int(parts[1]), month, 1)

    return None


def extract_experience_ranges(cv_text: str, today: date | None = None) -> list[tuple[date, date]]:
    """CV metninden tarih aralıklarını yakalar."""
    reference = today or date.today()
    ranges: list[tuple[date, date]] = []
    for match in _RANGE_RE.finditer(cv_text or ""):
        start = _parse_date_token(match.group("start"), is_end=False, today=reference)
        end = _parse_date_token(match.group("end"), is_end=True, today=reference)
        if start is None or end is None or end < start:
            continue
        ranges.append((start, end))
    return ranges


def _merge_ranges(ranges: list[tuple[date, date]]) -> list[tuple[date, date]]:
    if not ranges:
        return []

    sorted_ranges = sorted(ranges, key=lambda item: item[0])
    merged: list[tuple[date, date]] = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if _month_index(start) <= _month_index(last_end) + 1:
            if end > last_end:
                merged[-1] = (last_start, end)
            continue
        merged.append((start, end))

    return merged


def calculate_experience_years(cv_text: str, today: date | None = None) -> dict:
    """Toplam benzersiz deneyim süresini yıl/ay olarak hesaplar."""
    ranges = extract_experience_ranges(cv_text, today=today)
    merged = _merge_ranges(ranges)
    total_months = sum(_month_index(end) - _month_index(start) + 1 for start, end in merged)

    return {
        "total_months": total_months,
        "total_years": round(total_months / 12, 1),
        "range_count": len(merged),
        "ranges": [
            {"start": f"{start.year:04d}-{start.month:02d}", "end": f"{end.year:04d}-{end.month:02d}"}
            for start, end in merged
        ],
    }
