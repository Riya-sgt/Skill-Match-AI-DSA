"""Shared, transparent weighted skill-matching engine for web and CLI.

This is rule-based scoring, not a trained machine-learning prediction.
"""
from skill_utils import normalize_skill

SOFT_SKILLS = {
    "communication", "teamwork", "leadership", "problem-solving",
    "problem solving", "negotiation", "stakeholders", "relationship building",
    "creativity", "critical thinking", "time management", "training",
}


class WeightedMatchingEngine:
    """Calculate weighted career fit consistently across all app interfaces."""

    def skill_weight(self, skill, job=None):
        overrides = (job or {}).get("skill_weights", {})
        key = normalize_skill(skill)
        for label, weight in overrides.items():
            if normalize_skill(label) == key:
                try:
                    value = int(weight)
                    if value > 0:
                        return value
                except (TypeError, ValueError):
                    pass
        soft_keys = {normalize_skill(s) for s in SOFT_SKILLS}
        return 1 if key in soft_keys else 2

    def analyze(self, profile, job):
        user_keys = {
            normalize_skill(s) for s in (profile.get("skills", []) or [])
            if normalize_skill(s)
        }
        required = [
            s for s in (job.get("skills", []) or []) if normalize_skill(s)
        ]
        matched, missing, details = [], [], []
        earned_weight = total_weight = 0
        for skill in required:
            weight = self.skill_weight(skill, job)
            is_matched = normalize_skill(skill) in user_keys
            total_weight += weight
            if is_matched:
                earned_weight += weight
                matched.append(skill)
            else:
                missing.append(skill)
            details.append({"skill": skill, "weight": weight, "matched": is_matched})
        score = round(earned_weight / total_weight * 100, 1) if total_weight else 0.0
        return {
            "score": score, "matched": matched, "missing": missing,
            "details": details, "earned_weight": earned_weight,
            "total_weight": total_weight,
        }
