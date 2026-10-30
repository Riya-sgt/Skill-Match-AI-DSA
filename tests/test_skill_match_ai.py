import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from database import Database
from matcher import SkillMatcher
from recommendation import RecommendationEngine
from skill_gap import SkillGapAnalyzer
from skill_utils import normalize_skill, unique_skills
from job import Job
from user import User
from course_recommender import CourseRecommender
from matching_engine import WeightedMatchingEngine


class SkillUtilityTests(unittest.TestCase):
    def test_alias_normalization(self):
        self.assertEqual(normalize_skill(" ML "), "machine learning")
        self.assertEqual(normalize_skill("PowerBI"), "power bi")

    def test_unique_skills_preserves_first_spelling(self):
        self.assertEqual(unique_skills(["Python", " python ", "SQL", ""]), ["Python", "SQL"])

    def test_empty_and_non_string_skills_are_safe(self):
        self.assertEqual(normalize_skill(None), "")
        self.assertEqual(SkillMatcher().calculate_match([None, " "], ["Python"]), 0.0)


class MatchingTests(unittest.TestCase):
    def setUp(self):
        self.matcher = SkillMatcher()

    def test_match_percentage(self):
        self.assertEqual(self.matcher.calculate_match(["Python", "SQL"], ["Python", "SQL", "Excel"]), 66.67)

    def test_aliases_match(self):
        self.assertEqual(self.matcher.calculate_match(["ML", "PowerBI"], ["Machine Learning", "Power BI"]), 100.0)

    def test_empty_job_skills_returns_zero(self):
        self.assertEqual(self.matcher.calculate_match(["Python"], []), 0.0)

    def test_duplicate_skills_do_not_inflate_score(self):
        self.assertEqual(self.matcher.calculate_match(["Python", "python"], ["Python", "Python"]), 100.0)

    def test_matched_skills_uses_aliases(self):
        self.assertEqual(self.matcher.matched_skills(["ML"], ["Machine Learning", "Python"]), ["Machine Learning"])

    def test_recommendations_sorted_and_limited(self):
        results = [
            {"title": "B role", "score": 50},
            {"title": "A role", "score": 50},
            {"title": "Top", "score": 100},
            {"title": "Zero", "score": 0},
        ]
        self.assertEqual([r["title"] for r in RecommendationEngine().recommend(results, limit=2)], ["Top", "A role"])

    def test_recommendation_limit_zero(self):
        self.assertEqual(RecommendationEngine().recommend([{"title": "A", "score": 50}], limit=0), [])

    def test_course_recommender_accepts_skill_aliases(self):
        courses = CourseRecommender()
        self.assertEqual(courses.recommend_course("ML"), "Machine Learning A-Z")
        self.assertEqual(courses.recommend_course("PowerBI"), "Power BI Data Analytics")

    def test_skill_gap_alias_and_unknown_job(self):
        jobs = [{"title": "ML Engineer", "skills": ["Python", "Machine Learning"]}]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(SkillGapAnalyzer().find_gap("ml engineer", ["Python", "ML"], jobs), [])
            self.assertIsNone(SkillGapAnalyzer().find_gap("missing", ["Python"], jobs))


class WeightedMatchingEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = WeightedMatchingEngine()

    def test_weighted_score_and_missing_skills(self):
        result = self.engine.analyze(
            {"skills": ["Python", "ML"]},
            {"title": "Data Scientist", "skills": ["Python", "Machine Learning", "SQL"]}
        )
        self.assertEqual(result["score"], 66.7)
        self.assertEqual(result["matched"], ["Python", "Machine Learning"])
        self.assertEqual(result["missing"], ["SQL"])
        self.assertEqual(result["earned_weight"], 4)
        self.assertEqual(result["total_weight"], 6)

    def test_soft_skill_has_lower_default_weight(self):
        result = self.engine.analyze(
            {"skills": ["Python", "Communication"]},
            {"title": "Example", "skills": ["Python", "Communication", "SQL"]}
        )
        self.assertEqual(result["score"], 60.0)
        self.assertEqual([d["weight"] for d in result["details"]], [2, 1, 2])

    def test_job_can_override_skill_weight(self):
        result = self.engine.analyze(
            {"skills": ["Python"]},
            {"title": "Example", "skills": ["Python", "SQL"],
             "skill_weights": {"Python": 5, "SQL": 1}}
        )
        self.assertEqual(result["score"], 83.3)
        self.assertEqual([d["weight"] for d in result["details"]], [5, 1])

    def test_aliases_match_in_weighted_engine(self):
        result = self.engine.analyze(
            {"skills": ["ML", "PowerBI"]},
            {"title": "Example", "skills": ["Machine Learning", "Power BI"]}
        )
        self.assertEqual(result["score"], 100.0)


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = Database(str(Path(self.temp_dir.name) / "test.db"))

    def tearDown(self):
        self.db.close_connection()
        self.temp_dir.cleanup()

    def test_user_and_skill_persistence(self):
        user_id = self.db.add_user("Riya")
        self.db.add_skill(user_id, "Python")
        self.assertEqual(self.db.get_user_profile(user_id), {"id": user_id, "name": "Riya", "education": "", "interests": "", "target_job": "", "skills": ["Python"]})

    def test_duplicate_skill_is_ignored_case_insensitively(self):
        user_id = self.db.add_user("Riya")
        self.assertTrue(self.db.add_skill(user_id, "Python"))
        self.assertFalse(self.db.add_skill(user_id, " python "))
        self.assertEqual(self.db.get_skills(user_id), ["Python"])

    def test_user_lookup_is_case_insensitive(self):
        self.db.add_user("Riya")
        self.assertEqual(self.db.get_user_by_name("riya")[1], "Riya")

    def test_jobs_are_unique_by_title(self):
        self.db.save_job("Data Analyst", ["Python", "SQL"])
        self.db.save_job("Data Analyst", ["Excel"])
        self.assertEqual(len(self.db.get_jobs()), 1)

    def test_applications_persist_and_filter_by_user(self):
        first = self.db.add_user("First")
        second = self.db.add_user("Second")
        self.db.add_application(first, "Data Analyst")
        self.db.add_application(second, "Web Developer")
        self.assertEqual(len(self.db.get_applications(first)), 1)
        self.assertEqual(len(self.db.get_applications()), 2)

    def test_load_profile_restores_stack(self):
        user_id = self.db.add_user("Riya")
        self.db.add_skill(user_id, "Python")
        user = User(self.db)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(user.load_profile(user_id))
        self.assertEqual(user.name, "Riya")
        self.assertEqual(user.skills, ["Python"])
        self.assertFalse(user.skill_stack.is_empty())

    def test_job_module_loads_twenty_roles(self):
        jobs = Job(self.db).get_jobs()
        self.assertEqual(len(jobs), 20)
        self.assertTrue(all("title" in item and "skills" in item for item in jobs))


if __name__ == "__main__":
    unittest.main(verbosity=2)
