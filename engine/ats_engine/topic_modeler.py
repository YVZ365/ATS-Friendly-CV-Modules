"""
ats_engine.topic_modeler — İş ilanı topic kümeleme yardımcıları.

Tam LDA kütüphanesi olmadan çalışabilmek için stdlib tabanlı, LDA-esintili bir
fallback yaklaşımı kullanır: önceden tanımlı topic taksonomileri üzerinden JD
metnindeki baskın konu kümelerini çıkarır.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

from .text import tr_lower

_TOPIC_TAXONOMY = {
    "technical": ["python", "typescript", "react", "next.js", "graphql", "rest api", "docker", "kubernetes", "postgresql"],
    "delivery": ["agile", "scrum", "ci/cd", "github actions", "tdd", "sprint", "release", "automation"],
    "leadership": ["lead", "mentor", "stakeholder", "roadmap", "strategy", "team", "ownership"],
    "product": ["okr", "kpi", "backlog", "user story", "go-to-market", "ab testing", "nps"],
    "data": ["sql", "analytics", "reporting", "dashboard", "experimentation", "metrics"],
    "soft_skills": ["communication", "collaboration", "problem solving", "cross-functional", "presentation"],
}


def cluster_job_topics(jd_text: str, top_n: int = 5) -> dict:
    """JD metnindeki baskın konu kümelerini sıralar."""
    normalized = tr_lower(jd_text or "")
    dominant_topics: list[dict] = []

    for topic, keywords in _TOPIC_TAXONOMY.items():
        matches = [keyword for keyword in keywords if keyword in normalized]
        if not matches:
            continue
        score = sum(normalized.count(keyword) for keyword in matches)
        dominant_topics.append(
            {
                "topic": topic,
                "score": score,
                "keywords": sorted(set(matches)),
            }
        )

    dominant_topics.sort(key=lambda item: (-item["score"], item["topic"]))
    return {
        "method": "heuristic_lda_fallback",
        "dominant_topics": dominant_topics[:top_n],
        "topic_count": len(dominant_topics),
    }
