import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from database import Database
from roadmap import build_daily_roadmap


class RoadmapTaskTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "roadmap_test.db")
        self.db = Database(self.db_path)
        self.user_id = self.db.add_user("Roadmap Tester", "Student", "Data", "Data Analyst")

    def tearDown(self):
        self.db.close_connection()
        self.temp_dir.cleanup()

    def test_roadmap_has_30_distinct_daily_tasks(self):
        roadmap = build_daily_roadmap(["SQL", "Python"], "Data Scientist")
        self.assertEqual(len(roadmap), 30)
        self.assertEqual([item["day"] for item in roadmap], list(range(1, 31)))
        self.assertEqual(len({item["title"] for item in roadmap}), 30)
        self.assertEqual(len({item["instructions"] for item in roadmap}), 30)
        self.assertEqual(len({item["exercise"] for item in roadmap}), 30)
        self.assertEqual(len({item["learning_objective"] for item in roadmap}), 30)
        self.assertEqual(len({item["explanation"] for item in roadmap}), 30)
        self.assertEqual(len({item["practical_activity"] for item in roadmap}), 30)
        self.assertEqual(len({item["expected_outcome"] for item in roadmap}), 30)
        self.assertTrue(all(item["title"] and item["learning_objective"] for item in roadmap))
        self.assertTrue(all(item["explanation"] and item["practical_activity"] for item in roadmap))
        self.assertTrue(all(item["expected_outcome"] for item in roadmap))
        self.assertTrue(all(item["duration"] > 0 for item in roadmap))
        self.assertTrue(all("completed" in item for item in roadmap))
        self.assertEqual(
            [roadmap[index - 1]["phase"] for index in (1, 7, 8, 14, 15, 21, 22, 26, 27, 30)],
            ["Foundations and setup", "Foundations and setup",
             "Guided practice and core exercises", "Guided practice and core exercises",
             "Applied tasks and mini-project development",
             "Applied tasks and mini-project development",
             "Integrated project implementation", "Integrated project implementation",
             "Testing, improvements, documentation and portfolio",
             "Final assessment, project review and next steps"],
        )

    def test_career_curricula_include_role_specific_topics(self):
        devops = build_daily_roadmap(["Linux", "Docker", "AWS"], "DevOps Engineer")
        data_science = build_daily_roadmap(
            ["Statistics", "SQL", "Python", "Machine Learning"], "Data Scientist"
        )
        analyst = build_daily_roadmap(
            ["Excel", "SQL", "Python"], "Data Analyst"
        )
        self.assertTrue(any("Docker" in item["title"] for item in devops))
        self.assertTrue(any("CI" in item["title"] for item in devops))
        self.assertTrue(any("deploy" in item["title"].casefold() for item in devops))
        self.assertTrue(any("statistics" in item["title"].casefold() for item in data_science))
        self.assertTrue(any("SQL" in item["title"] for item in data_science))
        self.assertTrue(any("model" in item["title"].casefold() for item in data_science))
        analyst_titles = " ".join(item["title"].casefold() for item in analyst)
        self.assertIn("spreadsheet", analyst_titles)
        self.assertIn("sql", analyst_titles)
        self.assertIn("dashboard", analyst_titles)
        self.assertIn("portfolio", analyst_titles)
        self.assertEqual(
            analyst[29]["phase"],
            "Final assessment, project review and next steps",
        )
        self.assertFalse(any("linux" in item["title"].casefold() for item in analyst))

    def test_other_careers_get_gap_and_career_specific_daily_content(self):
        roadmap = build_daily_roadmap(
            ["HTML", "CSS", "JavaScript"], "Web Developer"
        )
        self.assertEqual(len(roadmap), 30)
        self.assertTrue(all("Web Developer" in item["title"] for item in roadmap))
        self.assertTrue(all(
            item["skill"] in {"HTML", "CSS", "JavaScript"} for item in roadmap
        ))
        self.assertTrue(all("Web Developer" in item["explanation"] for item in roadmap))

    def test_weighted_missing_skills_are_prioritized(self):
        roadmap = build_daily_roadmap(
            ["SQL", "Python"], "Data Scientist", {"SQL": 1, "Python": 5}
        )
        self.assertEqual(roadmap[0]["skill"], "Python")
        self.assertEqual(roadmap[4]["skill"], "Python")
        self.assertEqual(roadmap[5]["skill"], "SQL")
        self.assertEqual(
            sum(item["skill"] == "Python" for item in roadmap), 25
        )
        self.assertIn("Python skill gap", roadmap[0]["instructions"])

    def test_task_completion_persists_and_is_scoped_to_career(self):
        analysis_id = self.db.save_profile_analysis(
            self.user_id, "Data Analyst", 50, ["Python"], ["SQL"]
        )
        roadmap = build_daily_roadmap(["SQL", "Python"], "Data Analyst")
        self.db.save_roadmap_tasks(
            self.user_id, "Data Analyst", roadmap, analysis_id=analysis_id
        )
        self.assertTrue(self.db.set_roadmap_task_completed(
            self.user_id, "Data Analyst", 1, True, analysis_id=analysis_id
        ))
        tasks = self.db.get_roadmap_tasks(
            self.user_id, "Data Analyst", analysis_id=analysis_id
        )
        self.assertTrue(tasks[0]["completed"])
        self.assertFalse(tasks[1]["completed"])
        self.assertEqual(tasks[0]["analysis_id"], analysis_id)
        self.assertEqual(tasks[0]["title"], roadmap[0]["title"])
        self.assertEqual(tasks[0]["instructions"], roadmap[0]["instructions"])
        self.assertEqual(tasks[0]["exercise"], roadmap[0]["exercise"])
        self.assertEqual(
            tasks[0]["learning_objective"], roadmap[0]["learning_objective"]
        )
        self.assertEqual(
            tasks[0]["expected_outcome"], roadmap[0]["expected_outcome"]
        )
        self.db.close_connection()
        self.db = Database(self.db_path)
        self.assertTrue(self.db.get_roadmap_tasks(
            self.user_id, "Data Analyst", analysis_id=analysis_id
        )[0]["completed"])
        self.assertFalse(self.db.get_roadmap_tasks(
            self.user_id, "Software Engineer"
        ))

    def test_roadmaps_are_separate_for_distinct_analyses(self):
        first_analysis = self.db.save_profile_analysis(
            self.user_id, "Data Analyst", 50, ["Python"], ["SQL"]
        )
        self.db.save_roadmap_tasks(
            self.user_id, "Data Analyst", build_daily_roadmap(["SQL"], "Data Analyst"),
            analysis_id=first_analysis,
        )
        self.db.set_roadmap_task_completed(
            self.user_id, "Data Analyst", 1, True, analysis_id=first_analysis
        )

        second_analysis = self.db.save_profile_analysis(
            self.user_id, "Data Analyst", 25, [], ["Python", "SQL"]
        )
        self.db.save_roadmap_tasks(
            self.user_id, "Data Analyst",
            build_daily_roadmap(["Python", "SQL"], "Data Analyst"),
            analysis_id=second_analysis,
        )
        self.db.save_roadmap_tasks(
            self.user_id, "Data Analyst",
            build_daily_roadmap(["SQL"], "Data Analyst"),
            analysis_id=first_analysis,
        )
        self.assertTrue(self.db.get_roadmap_tasks(
            self.user_id, "Data Analyst", analysis_id=first_analysis
        )[0]["completed"])
        self.assertEqual(len(self.db.get_roadmap_tasks(
            self.user_id, "Data Analyst", analysis_id=first_analysis
        )), 30)
        second_tasks = self.db.get_roadmap_tasks(
            self.user_id, "Data Analyst", analysis_id=second_analysis
        )
        self.assertFalse(second_tasks[0]["completed"])
        self.assertEqual(second_tasks[0]["skill"], "Python")
        self.assertEqual(len(second_tasks), 30)

    def test_roadmap_is_scoped_to_the_correct_profile(self):
        other_user_id = self.db.add_user("Second Roadmap Tester")
        first_analysis = self.db.save_profile_analysis(
            self.user_id, "Data Analyst", 50, ["Python"], ["SQL"]
        )
        second_analysis = self.db.save_profile_analysis(
            other_user_id, "Data Analyst", 25, [], ["Excel"]
        )
        self.db.save_roadmap_tasks(
            self.user_id, "Data Analyst",
            build_daily_roadmap(["SQL"], "Data Analyst"),
            analysis_id=first_analysis,
        )
        self.db.save_roadmap_tasks(
            other_user_id, "Data Analyst",
            build_daily_roadmap(["Excel"], "Data Analyst"),
            analysis_id=second_analysis,
        )
        self.assertEqual(len(self.db.get_roadmap_tasks(
            self.user_id, "Data Analyst", analysis_id=first_analysis
        )), 30)
        self.assertEqual(
            self.db.get_roadmap_tasks(
                other_user_id, "Data Analyst", analysis_id=second_analysis
            )[0]["skill"],
            "Excel",
        )

    def test_refreshing_roadmap_does_not_reset_completed_tasks(self):
        self.db.save_roadmap_tasks(
            self.user_id, "Data Analyst", build_daily_roadmap(["SQL"], "Data Analyst")
        )
        self.db.set_roadmap_task_completed(self.user_id, "Data Analyst", 7, True)
        self.db.save_roadmap_tasks(
            self.user_id, "Data Analyst",
            build_daily_roadmap(["SQL", "Python"], "Data Analyst")
        )
        tasks = self.db.get_roadmap_tasks(self.user_id, "Data Analyst")
        self.assertTrue(tasks[6]["completed"])
        self.assertEqual(len(tasks), 30)

    def test_analysis_page_shows_daily_content_and_saved_progress(self):
        import app as flask_app

        self.db.add_skill(self.user_id, "Python")
        self.db.close_connection()
        self.db = Database(self.db_path)
        flask_app.app.config["TESTING"] = True
        client = flask_app.app.test_client()

        with patch.object(
            flask_app, "Database", side_effect=lambda: Database(self.db_path)
        ):
            response = client.post(
                f"/profiles/{self.user_id}/analyze",
                data={"target_job": "Data Analyst"},
            )
            self.assertEqual(response.status_code, 302)
            report_url = response.headers["Location"]
            report = client.get(report_url)
            self.assertEqual(report.status_code, 200)
            self.assertIn(b"Spreadsheet workspace and data layout", report.data)
            self.assertIn(b"Practical activity", report.data)
            self.assertIn(b"Expected outcome", report.data)
            self.assertIn(b"Daily lesson and deliverable", report.data)
            self.assertIn(b"0 of 30 tasks completed", report.data)

            analysis_id = parse_qs(urlparse(report_url).query)["analysis_id"][0]
            updated = client.post(
                f"/profiles/{self.user_id}/roadmap/task/1",
                data={
                    "target_job": "Data Analyst",
                    "analysis_id": analysis_id,
                    "completed": "1",
                },
            )
            self.assertEqual(updated.status_code, 302)
            report = client.get(updated.headers["Location"])
            self.assertIn(b"1 of 30 tasks completed", report.data)
            self.assertIn(b">3%</span>", report.data)
            self.assertIn(b"Completed", report.data)

    def test_legacy_roadmap_schema_migrates_without_losing_progress(self):
        legacy_path = os.path.join(self.temp_dir.name, "legacy.db")
        connection = sqlite3.connect(legacy_path)
        connection.executescript("""
            CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);
            INSERT INTO users(name) VALUES ('Legacy user');
            CREATE TABLE profile_analyses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_job TEXT NOT NULL,
                match_percent REAL NOT NULL,
                matched_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            INSERT INTO profile_analyses(
                user_id, target_job, match_percent, matched_skills, missing_skills
            ) VALUES (1, 'Data Analyst', 50, 'Python', 'SQL');
            CREATE TABLE roadmap_tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_job TEXT NOT NULL,
                day INTEGER NOT NULL CHECK(day BETWEEN 1 AND 30),
                skill TEXT NOT NULL,
                task TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, target_job, day),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            INSERT INTO roadmap_tasks(user_id, target_job, day, skill, task, completed)
            VALUES (1, 'Data Analyst', 1, 'SQL', 'Legacy task', 1);
        """)
        connection.commit()
        connection.close()

        migrated = Database(legacy_path)
        tasks = migrated.get_roadmap_tasks(1, "Data Analyst", analysis_id=1)
        self.assertEqual(tasks[0]["task"], "Legacy task")
        self.assertTrue(tasks[0]["completed"])
        self.assertEqual(tasks[0]["instructions"], "Legacy task")
        self.assertEqual(tasks[0]["analysis_id"], 1)
        migrated.close_connection()


if __name__ == "__main__":
    unittest.main()
