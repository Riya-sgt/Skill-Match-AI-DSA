from stack import SkillStack
from skill_utils import normalize_skill, unique_skills


class User:
    def __init__(self, db):
        self.name = ""
        self.skills = []
        self.user_id = None
        self.education = ""
        self.interests = ""
        self.target_job = ""
        self.db = db
        self.skill_stack = SkillStack()

    def load_profile(self, user_id):
        profile = self.db.get_user_profile(user_id)
        if profile is None:
            print("\nProfile not found.")
            return False
        self.user_id = profile["id"]
        self.name = profile["name"]
        self.skills = profile["skills"]
        self.education = profile["education"]
        self.interests = profile["interests"]
        self.target_job = profile["target_job"]
        self.skill_stack = SkillStack()
        for skill in self.skills:
            self.skill_stack.push(skill)
        print(f"\nWelcome back, {self.name}. Profile loaded successfully.")
        return True

    def create_profile(self):
        name = input("Enter Name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return False

        education = input("Enter Education (e.g. B.Tech CSE AI-ML): ").strip()
        interests = input("Enter Career Interests (comma separated): ").strip()
        target_job = input("Enter Target Career (e.g. Data Analyst): ").strip()
        skill_input = input("Enter Skills (comma separated): ").strip()
        incoming = unique_skills(skill_input.split(","))
        if not incoming:
            print("Please enter at least one skill.")
            return False

        existing = self.db.get_user_by_name(name)
        if existing:
            self.load_profile(existing[0])
            self.db.update_user_profile(self.user_id, name, education, interests, target_job)
            self.education, self.interests, self.target_job = education, interests, target_job
            added = 0
            for skill in incoming:
                if self.db.add_skill(self.user_id, skill):
                    self.skills.append(skill)
                    self.skill_stack.push(skill)
                    added += 1
            print(f"\nExisting profile loaded and updated. Added {added} new skill(s).")
            return True

        self.user_id = self.db.add_user(name, education, interests, target_job)
        self.name = name
        self.education, self.interests, self.target_job = education, interests, target_job
        self.skills = []
        self.skill_stack = SkillStack()
        for skill in incoming:
            if self.db.add_skill(self.user_id, skill):
                self.skills.append(skill)
                self.skill_stack.push(skill)
        print(f"\nProfile Created Successfully. Your Profile ID is {self.user_id}.")
        print("Your profile and skills are saved in the SQLite database.")
        return True

    def view_profile(self):
        print("\n===== SAVED PROFILE =====")
        print("Profile ID :", self.user_id if self.user_id else "Not loaded")
        print("Name       :", self.name if self.name else "Not Created")
        print("Education  :", self.education or "Not provided")
        print("Interests  :", self.interests or "Not provided")
        print("Target Job :", self.target_job or "Not provided")
        print("Skills:")
        if not self.skills:
            print("No skills added.")
        else:
            for skill in self.skills:
                print("-", skill)

    def add_skill(self):
        if not self.user_id:
            print("\nPlease create or load your profile first.")
            return False
        skill = input("Enter New Skill: ").strip()
        key = normalize_skill(skill)
        if not key:
            print("Skill cannot be empty.")
            return False
        if key in {normalize_skill(s) for s in self.skills}:
            print("Skill already exists.")
            return False
        if self.db.add_skill(self.user_id, skill):
            self.skills.append(skill)
            self.skill_stack.push(skill)
            print("\nSkill Added Successfully and saved to database.")
            return True
        print("Skill already exists.")
        return False

    def view_skill_history(self):
        self.skill_stack.display()
