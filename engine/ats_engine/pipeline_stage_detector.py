"""
ats_engine.pipeline_stage_detector — Kariyer/pipeline aşaması tespiti.

CV metnindeki unvan sinyalleri ve toplam deneyim yılına göre adayın yaklaşık
kariyer aşamasını junior/mid/senior/lead olarak sınıflandırır.

Bağımlılık: yalnızca standart kütüphane + experience_year_extractor.
"""

from __future__ import annotations

from .experience_year_extractor import calculate_experience_years
from .text import tr_lower

_STAGE_ORDER = {"junior": 0, "mid": 1, "senior": 2, "lead": 3}
_STAGE_KEYWORDS = {
    "junior": ["junior", "entry level", "intern", "trainee", "new graduate"],
    "mid": ["mid-level", "mid level", "associate", "specialist", "engineer"],
    "senior": ["senior", "sr ", "staff", "principal", "uzman"],
    "lead": ["lead", "head", "manager", "director", "architect", "team lead", "principal engineer"],
}


def map_experience_to_stage(years_experience: float) -> str:
    """Deneyim yılına göre kariyer aşaması döndürür."""
    if years_experience < 2:
        return "junior"
    if years_experience < 5:
        return "mid"
    if years_experience < 8:
        return "senior"
    return "lead"


def detect_pipeline_stage(cv_text: str, years_experience: float | None = None) -> dict:
    """CV metninden kariyer aşaması tespiti yapar."""
    normalized = tr_lower(cv_text or "")
    explicit_stage: str | None = None
    title_hits: list[str] = []

    for stage in ("junior", "mid", "senior", "lead"):
        hits = [keyword for keyword in _STAGE_KEYWORDS[stage] if keyword in normalized]
        if hits:
            title_hits.extend(hits)
            if explicit_stage is None or _STAGE_ORDER[stage] > _STAGE_ORDER[explicit_stage]:
                explicit_stage = stage

    years = years_experience
    if years is None:
        years = calculate_experience_years(cv_text).get("total_years", 0.0)

    experience_stage = map_experience_to_stage(years)
    stage = explicit_stage or experience_stage

    if explicit_stage and explicit_stage == experience_stage:
        confidence = 0.95
    elif explicit_stage:
        confidence = 0.82
    elif years > 0:
        confidence = 0.78
    else:
        confidence = 0.6

    return {
        "stage": stage,
        "years_experience": round(years, 1),
        "confidence": round(confidence, 2),
        "signals": {
            "title_keywords": title_hits,
            "experience_stage": experience_stage,
        },
    }
