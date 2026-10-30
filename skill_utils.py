"""Shared skill normalization helpers for consistent matching across modules."""
import re

ALIASES = {
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "powerbi": "power bi",
    "power-bi": "power bi",
    "js": "javascript",
    "c plus plus": "c++",
    "cpp": "c++",
    "ui ux": "ui/ux",
    "user interface": "user interface",
    "user experience": "user experience",
}


def normalize_skill(skill):
    """Return a comparable skill key; tolerate None and surrounding whitespace."""
    if not isinstance(skill, str):
        return ""
    key = re.sub(r"\s+", " ", skill.strip().lower())
    return ALIASES.get(key, key)


def unique_skills(skills):
    """Return non-empty skills, preserving the first display spelling."""
    result = []
    seen = set()
    for skill in skills:
        display = skill.strip() if isinstance(skill, str) else ""
        key = normalize_skill(display)
        if key and key not in seen:
            seen.add(key)
            result.append(display)
    return result
