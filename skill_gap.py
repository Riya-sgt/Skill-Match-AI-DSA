from skill_utils import normalize_skill


class SkillGapAnalyzer:
    def find_gap(self, target_job, user_skills, jobs):
        target = (target_job or "").strip().casefold()
        user_set = {normalize_skill(s) for s in user_skills}
        user_set.discard("")

        for job in jobs:
            if job["title"].strip().casefold() == target:
                missing = [
                    skill for skill in job["skills"]
                    if normalize_skill(skill) not in user_set
                ]
                print("\n===== SKILL GAP ANALYSIS =====")
                print("Target Job :", job["title"])
                if missing:
                    print("Missing Skills:")
                    for skill in missing:
                        print("-", skill)
                else:
                    print("You Have All Required Skills")
                return missing

        print("\nJob Not Found")
        return None
