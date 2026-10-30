from linkedlist import JobLinkedList


class Job:
    def __init__(self, db=None):
        self.job_list = JobLinkedList()
        self.db = db
        self.load_jobs()

    def load_jobs(self):
        # Keep the original DSA linked-list implementation and seed its original roles.
        defaults = [
            ("Data Analyst", ["Python", "SQL", "Excel"]),
            ("ML Engineer", ["Python", "Machine Learning"]),
            ("Data Scientist", ["Python", "SQL", "Machine Learning"]),
            ("Web Developer", ["HTML", "CSS", "JavaScript"]),
            ("Software Engineer", ["Python", "Java", "C++"]),
            ("DevOps Engineer", ["Linux", "Docker", "AWS"]),
            ("Network Engineer", ["Networking", "Security", "Cybersecurity"]),
            ("QA Engineer", ["Testing", "Debugging", "Manual Testing"]),
            ("UI/UX Designer", ["Design", "User Experience", "User Interface"]),
            ("Product Manager", ["Product Management", "Project Management", "Stakeholders"]),
            ("Business Analyst", ["Business Analysis", "Financial Analysis", "Market Research"]),
            ("Financial Analyst", ["Financial Analysis", "Risk Management", "Valuation"]),
            ("Operations Manager", ["Operations Management", "Supply Chain", "Project Management"]),
            ("Project Manager", ["Project Management", "Team Leadership", "Risk Management"]),
            ("Sales Manager", ["Sales Management", "Marketing", "Relationship Building"]),
            ("Customer Service Representative", ["Customer Service", "Problem-Solving", "Negotiation"]),
            ("Social Media Manager", ["Social Media Management", "Content Creation", "SEO"]),
            ("Digital Marketing Specialist", ["Digital Marketing", "Content Creation", "SEO"]),
            ("Financial Planner", ["Financial Planning", "Risk Management", "Budgeting"]),
            ("Human Resources Manager", ["Human Resources", "Recruitment", "Training"]),
        ]
        for title, skills in defaults:
            if self.db:
                self.db.save_job(title, skills)

        # Load ALL database jobs, including demo roles, into the linked list.
        if self.db:
            for row in self.db.get_jobs():
                self.job_list.add_job(row["title"], row["skills"])
        else:
            for title, skills in defaults:
                self.job_list.add_job(title, skills)

    def view_jobs(self):
        print("\\n===== AVAILABLE JOBS =====")
        self.job_list.display_jobs()

    def get_jobs(self):
        return self.job_list.get_all_jobs()

    def search_job(self, title=None):
        if title is None:
            title = input("Enter Job Title: ")
        target = (title or "").strip().casefold()
        for item in self.get_jobs():
            if item["title"].casefold() == target:
                print("\\n===== JOB FOUND =====")
                print("Title :", item["title"])
                print("Skills:", ", ".join(item["skills"]))
                return item
        matches = [item for item in self.get_jobs() if target and target in item["title"].casefold()]
        if len(matches) == 1:
            return matches[0]
        print("\\nJob Not Found" if not matches else "\\nMultiple jobs matched. Please enter a more specific title.")
        return None
