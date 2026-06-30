"""
ats_engine.keyword_gap_ranker — Eksik anahtar kelime sıralayıcı.

Job description içindeki önemli anahtar kelimeleri, CV'de geçmiyorsa
frekans × önem mantığıyla puanlayıp sıralar.

Bağımlılık: yalnızca standart kütüphane + fuzzy_keyword_matcher.
"""

from __future__ import annotations

from collections import Counter

from .fuzzy_keyword_matcher import find_fuzzy_matches
from .text import sentences, tokenize, tr_lower

_PRIORITY_HINTS = {
    "must": 1.0,
    "required": 1.0,
    "requirement": 1.0,
    "zorunlu": 1.0,
    "need": 0.95,
    "preferred": 0.6,
    "plus": 0.5,
    "nice": 0.5,
    "tercih": 0.6,
}


def _importance_for_sentence(sentence: str) -> float:
    score = 0.4
    lowered = tr_lower(sentence)
    for hint, weight in _PRIORITY_HINTS.items():
        if hint in lowered:
            score = max(score, weight)
    return score


def _default_keywords(jd_text: str) -> list[str]:
    counts = Counter(tokenize(jd_text, ngram_max=3, drop_stopwords=True))
    ranked = [term for term, count in counts.items() if count >= 1 and len(term) > 3 and any(ch.isalpha() for ch in term)]
    ranked.sort(key=lambda item: (-counts[item], -len(item.split()), item))
    return ranked[:20]


def rank_keyword_gaps(jd_text: str, cv_text: str, keywords: list[str] | None = None) -> list[dict]:
    """CV'de eksik kalan JD anahtar kelimelerini önem sırasına göre döndürür."""
    candidates = keywords or _default_keywords(jd_text)
    jd_sentences = sentences(jd_text)
    gaps: list[dict] = []

    for keyword in candidates:
        if find_fuzzy_matches([keyword], cv_text, threshold=0.84):
            continue
        frequency = tr_lower(jd_text).count(tr_lower(keyword)) or 1
        sentence_weights = [
            _importance_for_sentence(sentence)
            for sentence in jd_sentences
            if tr_lower(keyword) in tr_lower(sentence)
        ]
        importance = max(sentence_weights) if sentence_weights else 0.5
        gap_score = round(frequency * importance, 2)
        gaps.append(
            {
                "keyword": keyword,
                "frequency": frequency,
                "importance": importance,
                "gap_score": gap_score,
            }
        )

    gaps.sort(key=lambda item: (-item["gap_score"], -item["frequency"], item["keyword"]))
    return gaps
