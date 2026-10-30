import sqlite3
from pathlib import Path
from skill_utils import normalize_skill


class Database:
    def __init__(self, db_name="skillmatch.db"):
        self.db_path = Path(db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                skills TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                job_title TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        # Safe migrations for databases created by earlier versions.
        user_columns = {row[1] for row in self.cursor.execute("PRAGMA table_info(users)")}
        for column in ("education", "interests", "target_job"):
            if column not in user_columns:
                self.cursor.execute(f"ALTER TABLE users ADD COLUMN {column} TEXT NOT NULL DEFAULT ''")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile_analyses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_job TEXT NOT NULL,
                match_percent REAL NOT NULL,
                matched_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        # Existing databases receive an additive migration before their task scope is upgraded.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roadmap_tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_job TEXT NOT NULL,
                analysis_id INTEGER REFERENCES profile_analyses(id) ON DELETE CASCADE,
                day INTEGER NOT NULL CHECK(day BETWEEN 1 AND 30),
                skill TEXT NOT NULL,
                task TEXT NOT NULL,
                title TEXT NOT NULL DEFAULT '',
                instructions TEXT NOT NULL DEFAULT '',
                exercise TEXT NOT NULL DEFAULT '',
                learning_objective TEXT NOT NULL DEFAULT '',
                explanation TEXT NOT NULL DEFAULT '',
                practical_activity TEXT NOT NULL DEFAULT '',
                expected_outcome TEXT NOT NULL DEFAULT '',
                duration INTEGER NOT NULL DEFAULT 45,
                phase TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, target_job, analysis_id, day),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        roadmap_columns = {
            row[1] for row in self.cursor.execute("PRAGMA table_info(roadmap_tasks)")
        }
        roadmap_migrations = {
            "analysis_id": "INTEGER REFERENCES profile_analyses(id) ON DELETE SET NULL",
            "title": "TEXT NOT NULL DEFAULT ''",
            "instructions": "TEXT NOT NULL DEFAULT ''",
            "exercise": "TEXT NOT NULL DEFAULT ''",
            "learning_objective": "TEXT NOT NULL DEFAULT ''",
            "explanation": "TEXT NOT NULL DEFAULT ''",
            "practical_activity": "TEXT NOT NULL DEFAULT ''",
            "expected_outcome": "TEXT NOT NULL DEFAULT ''",
            "duration": "INTEGER NOT NULL DEFAULT 45",
            "phase": "TEXT NOT NULL DEFAULT ''",
        }
        for column, definition in roadmap_migrations.items():
            if column not in roadmap_columns:
                self.cursor.execute(
                    f"ALTER TABLE roadmap_tasks ADD COLUMN {column} {definition}"
                )
        has_analysis_unique = False
        for index in self.cursor.execute("PRAGMA index_list(roadmap_tasks)").fetchall():
            if index[2]:
                indexed_columns = [
                    row[2] for row in self.cursor.execute(
                        f"PRAGMA index_info('{index[1]}')"
                    ).fetchall()
                ]
                if indexed_columns == ["user_id", "target_job", "analysis_id", "day"]:
                    has_analysis_unique = True
                    break
        if not has_analysis_unique:
            self.cursor.execute("""
                CREATE TABLE roadmap_tasks_new(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    target_job TEXT NOT NULL,
                    analysis_id INTEGER REFERENCES profile_analyses(id) ON DELETE CASCADE,
                    day INTEGER NOT NULL CHECK(day BETWEEN 1 AND 30),
                    skill TEXT NOT NULL,
                    task TEXT NOT NULL,
                    title TEXT NOT NULL DEFAULT '',
                    instructions TEXT NOT NULL DEFAULT '',
                    exercise TEXT NOT NULL DEFAULT '',
                    learning_objective TEXT NOT NULL DEFAULT '',
                    explanation TEXT NOT NULL DEFAULT '',
                    practical_activity TEXT NOT NULL DEFAULT '',
                    expected_outcome TEXT NOT NULL DEFAULT '',
                    duration INTEGER NOT NULL DEFAULT 45,
                    phase TEXT NOT NULL DEFAULT '',
                    completed INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, target_job, analysis_id, day),
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            self.cursor.execute("""
                INSERT INTO roadmap_tasks_new(
                    id, user_id, target_job, analysis_id, day, skill, task,
                    title, instructions, exercise, learning_objective, explanation,
                    practical_activity, expected_outcome, duration, phase, completed, updated_at
                )
                SELECT r.id, r.user_id, r.target_job,
                       COALESCE(r.analysis_id, (
                           SELECT pa.id FROM profile_analyses pa
                           WHERE pa.user_id=r.user_id
                             AND pa.target_job=r.target_job COLLATE NOCASE
                           ORDER BY pa.id DESC LIMIT 1
                       )),
                       r.day, r.skill, r.task, r.title, r.instructions, r.exercise,
                       r.learning_objective, r.explanation, r.practical_activity,
                       r.expected_outcome, r.duration, r.phase, r.completed, r.updated_at
                FROM roadmap_tasks r
            """)
            self.cursor.execute("DROP TABLE roadmap_tasks")
            self.cursor.execute("ALTER TABLE roadmap_tasks_new RENAME TO roadmap_tasks")
        self.cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS roadmap_tasks_legacy_scope
            ON roadmap_tasks(user_id, target_job, day)
            WHERE analysis_id IS NULL
        """)
        self.conn.commit()

    def add_user(self, name, education="", interests="", target_job=""):
        self.cursor.execute(
            "INSERT INTO users(name, education, interests, target_job) VALUES(?, ?, ?, ?)",
            (name.strip(), education.strip(), interests.strip(), target_job.strip())
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_user_profile(self, user_id, name, education="", interests="", target_job=""):
        self.cursor.execute(
            "UPDATE users SET name=?, education=?, interests=?, target_job=? WHERE id=?",
            (name.strip(), education.strip(), interests.strip(), target_job.strip(), user_id)
        )
        self.conn.commit()

    def add_skill(self, user_id, skill):
        skill = (skill or "").strip()
        if not skill:
            return False
        existing = self.get_skills(user_id)
        if normalize_skill(skill) in {normalize_skill(item) for item in existing}:
            return False
        self.cursor.execute(
            "INSERT INTO skills(user_id, skill) VALUES(?, ?)", (user_id, skill)
        )
        self.conn.commit()
        return True

    def get_user_by_name(self, name):
        self.cursor.execute(
            "SELECT id, name FROM users WHERE name = ? COLLATE NOCASE ORDER BY id LIMIT 1",
            (name.strip(),)
        )
        return self.cursor.fetchone()

    def get_users(self):
        self.cursor.execute("SELECT id, name FROM users ORDER BY id")
        return self.cursor.fetchall()

    def get_user_profile(self, user_id):
        self.cursor.execute(
            "SELECT id, name, education, interests, target_job FROM users WHERE id = ?",
            (user_id,)
        )
        user = self.cursor.fetchone()
        if user is None:
            return None
        return {
            "id": user[0], "name": user[1], "education": user[2] or "",
            "interests": user[3] or "", "target_job": user[4] or "",
            "skills": self.get_skills(user_id)
        }

    def save_job(self, title, skills):
        self.cursor.execute(
            "INSERT OR IGNORE INTO jobs(title, skills) VALUES(?, ?)",
            (title, ", ".join(skills))
        )
        self.conn.commit()

    def get_jobs(self):
        self.cursor.execute("SELECT id, title, skills FROM jobs ORDER BY id")
        return [
            {"id": row[0], "title": row[1],
             "skills": [skill.strip() for skill in (row[2] or "").split(",") if skill.strip()]}
            for row in self.cursor.fetchall()
        ]

    def save_profile_analysis(self, user_id, target_job, match_percent, matched_skills, missing_skills):
        self.cursor.execute("""
            INSERT INTO profile_analyses
            (user_id, target_job, match_percent, matched_skills, missing_skills)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, target_job, match_percent, ", ".join(matched_skills), ", ".join(missing_skills)))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_profile_analyses(self, user_id):
        self.cursor.execute("""
            SELECT id, target_job, match_percent, matched_skills, missing_skills, created_at
            FROM profile_analyses WHERE user_id=? ORDER BY id DESC
        """, (user_id,))
        return self.cursor.fetchall()

    def get_profile_analysis(self, user_id, target_job, analysis_id=None):
        if analysis_id is None:
            self.cursor.execute("""
                SELECT id, target_job, match_percent, matched_skills, missing_skills, created_at
                FROM profile_analyses
                WHERE user_id=? AND target_job=? COLLATE NOCASE
                ORDER BY id DESC LIMIT 1
            """, (user_id, target_job))
        else:
            self.cursor.execute("""
                SELECT id, target_job, match_percent, matched_skills, missing_skills, created_at
                FROM profile_analyses WHERE user_id=? AND target_job=? COLLATE NOCASE AND id=?
            """, (user_id, target_job, analysis_id))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row[0], "target_job": row[1], "match_percent": row[2],
            "matched_skills": [skill.strip() for skill in (row[3] or "").split(",") if skill.strip()],
            "missing_skills": [skill.strip() for skill in (row[4] or "").split(",") if skill.strip()],
            "created_at": row[5],
        }

    def save_roadmap_tasks(self, user_id, target_job, roadmap, analysis_id=None):
        """Create/update the 30 task descriptions without resetting completion state."""
        for item in roadmap:
            self.cursor.execute("""
                INSERT INTO roadmap_tasks(
                    user_id, target_job, analysis_id, day, skill, task,
                    title, instructions, exercise, learning_objective, explanation,
                    practical_activity, expected_outcome, duration, phase
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT DO UPDATE SET
                    analysis_id=excluded.analysis_id,
                    skill=excluded.skill, task=excluded.task,
                    title=excluded.title, instructions=excluded.instructions,
                    exercise=excluded.exercise, duration=excluded.duration,
                    learning_objective=excluded.learning_objective,
                    explanation=excluded.explanation,
                    practical_activity=excluded.practical_activity,
                    expected_outcome=excluded.expected_outcome,
                    phase=excluded.phase,
                    updated_at=CURRENT_TIMESTAMP
            """, (
                user_id, target_job, analysis_id, item["day"], item["skill"],
                item.get("instructions", item.get("task", "")),
                item.get("title", ""), item.get("instructions", item.get("task", "")),
                item.get("exercise", ""),
                item.get("learning_objective", ""),
                item.get("explanation", item.get("instructions", item.get("task", ""))),
                item.get("practical_activity", item.get("exercise", "")),
                item.get("expected_outcome", ""),
                item.get("duration", 45), item.get("phase", ""),
            ))
        self.conn.commit()

    def get_roadmap_tasks(self, user_id, target_job, analysis_id=None):
        if analysis_id is None:
            self.cursor.execute("""
                SELECT day, skill, task, completed, title, instructions, exercise,
                       learning_objective, explanation, practical_activity,
                       expected_outcome, duration, phase, analysis_id
                FROM roadmap_tasks
                WHERE user_id=? AND target_job=? AND analysis_id IS NULL
                ORDER BY day
            """, (user_id, target_job))
        else:
            self.cursor.execute("""
                SELECT day, skill, task, completed, title, instructions, exercise,
                       learning_objective, explanation, practical_activity,
                       expected_outcome, duration, phase, analysis_id
                FROM roadmap_tasks
                WHERE user_id=? AND target_job=? AND analysis_id=?
                ORDER BY day
            """, (user_id, target_job, analysis_id))
        return [
            {
                "day": row[0], "skill": row[1], "task": row[2],
                "completed": bool(row[3]), "title": row[4] or f"Day {row[0]} learning task",
                "instructions": row[5] or row[2],
                "exercise": row[6] or "Complete a practical exercise and record your result.",
                "learning_objective": row[7] or row[4] or f"Complete day {row[0]}",
                "explanation": row[8] or row[5] or row[2],
                "practical_activity": row[9] or row[6] or "Complete the task and record your result.",
                "expected_outcome": row[10] or "A completed task artifact ready for review.",
                "duration": row[11], "phase": row[12] or "",
                "analysis_id": row[13],
            }
            for row in self.cursor.fetchall()
        ]

    def set_roadmap_task_completed(self, user_id, target_job, day, completed, analysis_id=None):
        self.cursor.execute("""
            UPDATE roadmap_tasks
            SET completed=?, updated_at=CURRENT_TIMESTAMP
            WHERE user_id=? AND target_job=? AND day=? AND analysis_id IS ?
        """, (1 if completed else 0, user_id, target_job, day, analysis_id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_profile(self, user_id):
        self.cursor.execute("SELECT id, name FROM users ORDER BY id")
        return self.cursor.fetchall()

    def get_skills(self, user_id):
        self.cursor.execute(
            "SELECT skill FROM skills WHERE user_id=? ORDER BY id", (user_id,)
        )
        return [row[0] for row in self.cursor.fetchall()]

    def add_application(self, user_id, job_title):
        self.cursor.execute(
            "INSERT INTO applications(user_id, job_title) VALUES(?, ?)",
            (user_id, job_title)
        )
        self.conn.commit()

    def get_applications(self, user_id=None):
        if user_id is None:
            self.cursor.execute("SELECT id, user_id, job_title FROM applications ORDER BY id")
        else:
            self.cursor.execute(
                "SELECT id, user_id, job_title FROM applications WHERE user_id=? ORDER BY id",
                (user_id,)
            )
        return self.cursor.fetchall()


    def update_profile(self, user_id, name, education="", interests="", target_job=""):
        self.cursor.execute(
            "UPDATE users SET name=?, education=?, interests=?, target_job=? WHERE id=?",
            (name.strip(), education.strip(), interests.strip(), target_job.strip(), user_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_profile(self, user_id):
        # Delete dependent rows explicitly so this also works with older schemas.
        self.cursor.execute("DELETE FROM profile_analyses WHERE user_id=?", (user_id,))
        self.cursor.execute("DELETE FROM roadmap_tasks WHERE user_id=?", (user_id,))
        self.cursor.execute("DELETE FROM applications WHERE user_id=?", (user_id,))
        self.cursor.execute("DELETE FROM skills WHERE user_id=?", (user_id,))
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_skill(self, user_id, skill):
        self.cursor.execute(
            "DELETE FROM skills WHERE user_id=? AND skill=? COLLATE NOCASE",
            (user_id, skill)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_profile_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM users")
        return self.cursor.fetchone()[0]

    def get_analysis_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM profile_analyses")
        return self.cursor.fetchone()[0]

    def close_connection(self):
        self.conn.close()
