"""
ats_engine.section_strength_scorer — Bölüm bazlı ATS güç skoru.

Summary, Experience, Education, Skills, Projects ve Certifications bölümlerini
bulur; içerik doluluğu, yapı ve ölçülebilir kanıt sinyallerine göre 0-100 arası
skorlar üretir.

Bağımlılık: yalnızca standart kütüphane + ats_engine.text.
"""

from __future__ import annotations

import re

from .text import has_quantification

_SECTION_HEADINGS = {
    "summary": {"summary", "profile", "professional summary", "özet", "profil"},
    "experience": {"experience", "work experience", "professional experience", "deneyim", "iş deneyimi"},
    "education": {"education", "eğitim"},
    "skills": {"skills", "technical skills", "competencies", "yetenekler", "beceriler"},
    "projects": {"projects", "projeler"},
    "certifications": {"certifications", "certificates", "sertifikalar", "sertifikalar ve belgeler"},
}
_DATE_RE = re.compile(r"\b(?:19|20)\d{2}\b")


def split_cv_sections(cv_text: str) -> dict[str, str]:
    """CV metnini standart ATS bölümlerine ayırır."""
    sections = {name: [] for name in _SECTION_HEADINGS}
    current: str | None = None

    for raw_line in (cv_text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        normalized = line.strip(" :#-").lower()
        matched = next((name for name, labels in _SECTION_HEADINGS.items() if normalized in labels), None)
        if matched:
            current = matched
            continue
        if current:
            sections[current].append(line)

    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def _score_single_section(name: str, content: str) -> dict:
    if not content:
        return {"score": 0, "signals": ["missing"]}

    score = 20
    signals: list[str] = ["present"]
    words = len(content.split())

    if words >= 12:
        score += 15
        signals.append("sufficient_length")
    if words >= 35:
        score += 10
    if name in {"experience", "projects"} and has_quantification(content):
        score += 25
        signals.append("quantified")
    if name in {"experience", "education", "certifications"} and _DATE_RE.search(content):
        score += 15
        signals.append("dated")
    if "\n" in content:
        score += 10
        signals.append("multi_line")
    if name == "skills" and len(re.split(r",|\n|•", content)) >= 5:
        score += 20
        signals.append("keyword_list")
    if name == "summary" and 25 <= words <= 120:
        score += 20
        signals.append("ats_friendly_length")
    if name == "certifications" and any(token in content.lower() for token in ("cert", "aws", "pmp", "scrum")):
        score += 10
        signals.append("credential_signal")

    return {"score": min(score, 100), "signals": signals}


def score_cv_sections(cv_text: str) -> dict:
    """CV bölümlerini skorlayıp özet döndürür."""
    sections = split_cv_sections(cv_text)
    per_section = {name: _score_single_section(name, content) for name, content in sections.items()}
    overall = round(sum(item["score"] for item in per_section.values()) / max(len(per_section), 1), 1)
    return {
        "overall_score": overall,
        "sections": per_section,
        "detected_sections": [name for name, content in sections.items() if content],
    }
