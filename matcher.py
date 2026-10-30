from skill_utils import normalize_skill


class SkillMatcher:
    """Set-based skill matching engine with consistent alias handling."""

    def calculate_match(self, user_skills, job_skills):
        user_set = {normalize_skill(s) for s in user_skills}
        user_set.discard("")
        job_set = {normalize_skill(s) for s in job_skills}
        job_set.discard("")
        if not job_set:
            return 0.0
        return round(len(user_set.intersection(job_set)) / len(job_set) * 100, 2)

    def matched_skills(self, user_skills, job_skills):
        user_set = {normalize_skill(s) for s in user_skills}
        user_set.discard("")
        return [skill for skill in job_skills if normalize_skill(skill) in user_set]
