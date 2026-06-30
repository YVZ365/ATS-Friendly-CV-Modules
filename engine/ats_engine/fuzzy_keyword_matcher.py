"""
ats_engine.fuzzy_keyword_matcher — Kısmi/fuzzy anahtar kelime eşleştirme.

string_score yaklaşımına benzer biçimde normalize edilmiş substring, kısaltma ve
sekans benzerliği sinyallerini birleştirerek 0-1 arası skor üretir.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher

from .text import tr_lower

_ALIAS_MAP = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "pm": "product management",
    "react.js": "react",
    "react js": "react",
    "node.js": "nodejs",
    "ci cd": "ci/cd",
}


def _normalize(text: str) -> str:
    lowered = tr_lower(text or "")
    lowered = lowered.replace(".js", " js")
    lowered = re.sub(r"[^a-z0-9çğıöşü+/ ]+", " ", lowered)
    lowered = " ".join(lowered.split())
    return _ALIAS_MAP.get(lowered, lowered)


def _initialism(text: str) -> str:
    parts = [part for part in _normalize(text).replace("/", " ").split() if part]
    return "".join(part[0] for part in parts)


def score_keyword_match(keyword: str, candidate: str) -> float:
    """İki terim arasındaki fuzzy eşleşme skorunu döndürür."""
    left = _normalize(keyword)
    right = _normalize(candidate)
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    if left in right or right in left:
        return 0.96
    if _initialism(left) and (_initialism(left) == right or _initialism(right) == left):
        return 0.93

    left_tokens = set(left.replace("/", " ").split())
    right_tokens = set(right.replace("/", " ").split())
    overlap = len(left_tokens & right_tokens) / max(len(left_tokens | right_tokens), 1)
    ratio = SequenceMatcher(None, left, right).ratio()
    return round(max(ratio * 0.7 + overlap * 0.3, overlap), 3)


def find_fuzzy_matches(keywords: list[str], text: str, threshold: float = 0.8) -> list[dict]:
    """Metin içinde eşik üstü fuzzy eşleşmeleri döndürür."""
    results: list[dict] = []
    normalized_text = _normalize(text)
    tokens = normalized_text.replace("/", " ").split()
    fragments = [normalized_text]
    for size in range(1, min(5, len(tokens)) + 1):
        for index in range(len(tokens) - size + 1):
            fragments.append(" ".join(tokens[index : index + size]))

    for keyword in keywords:
        score = max(score_keyword_match(keyword, fragment) for fragment in fragments)
        if score >= threshold:
            results.append({"keyword": keyword, "score": score, "matched_text": text})
    return results
