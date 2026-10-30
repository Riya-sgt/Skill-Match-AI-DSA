from database import Database
from user import User
from job import Job
from matcher import SkillMatcher
from recommendation import RecommendationEngine
from skill_gap import SkillGapAnalyzer
from course_recommender import CourseRecommender
from report_generator import ReportGenerator
from chart_generator import ChartGenerator
from queue_ds import JobQueue
from profile_analyzer import ProfileAnalyzer


def build_results(user, jobs, matcher):
    return [
        {
            "title": job_data["title"],
            "score": matcher.calculate_match(
                user.skills, job_data["skills"]
            )
        }
        for job_data in jobs
    ]


def require_profile(user):
    if not user.user_id:
        print("\nPlease create a profile first.")
        return False
    return True


def main():
    db = Database()
    user = User(db)
    job = Job(db)
    matcher = SkillMatcher()
    recommender = RecommendationEngine()
    skill_gap = SkillGapAnalyzer()
    course = CourseRecommender()
    report = ReportGenerator()
    chart = ChartGenerator()
    job_queue = JobQueue()
    profile_analyzer = ProfileAnalyzer()

    while True:
        print("\n" + "=" * 50)
        print("              SKILL MATCH AI")
        print("=" * 50)
        print("1.  Create Profile")
        print("2.  View Profile")
        print("3.  Add Skill")
        print("4.  View Jobs")
        print("5.  Match Skills")
        print("6.  Recommend Jobs")
        print("7.  Skill Gap Analysis")
        print("8.  Recommend Course")
        print("9.  Generate Report")
        print("10. View Chart")
        print("11. Apply For Job")
        print("12. View Application Queue")
        print("13. Exit")
        print("14. View Skill History (Stack)")
        print("15. View Database Records")
        print("16. Export PDF Report")
        print("17. View Statistics Dashboard")
        print("18. Load Existing Profile")
        print("19. Analyze My Profile (save skill-gap report)")
        print("20. View Saved Analysis History")

        choice = input("\nEnter Choice: ").strip()

        if choice == "1":
            user.create_profile()

        elif choice == "2":
            user.view_profile()

        elif choice == "3":
            user.add_skill()

        elif choice == "4":
            job.view_jobs()

        elif choice == "5":
            if not require_profile(user):
                continue
            print("\n===== SKILL MATCHING =====")
            results = build_results(user, job.get_jobs(), matcher)
            for item in results:
                print(f"{item['title']} -> {item['score']}%")

        elif choice == "6":
            if not require_profile(user):
                continue
            results = build_results(user, job.get_jobs(), matcher)
            recommendations = recommender.recommend(results)
            print("\n===== TOP RECOMMENDATIONS =====")
            if not recommendations:
                print("No matching jobs found.")
            for item in recommendations:
                print(f"{item['title']} -> {item['score']}%")

        elif choice == "7":
            if not require_profile(user):
                continue
            target_job = input("Enter Job Title: ")
            skill_gap.find_gap(target_job, user.skills, job.get_jobs())

        elif choice == "8":
            skill = input("Enter Missing Skill: ")
            print("Recommended Course:",
                  course.recommend_course(skill))

        elif choice == "9":
            if not require_profile(user):
                continue
            results = build_results(user, job.get_jobs(), matcher)
            recommendations = recommender.recommend(results)
            report.generate_report(user, recommendations)

        elif choice == "10":
            if not require_profile(user):
                continue
            results = build_results(user, job.get_jobs(), matcher)
            recommendations = recommender.recommend(results)
            chart.generate_chart(recommendations)

        elif choice == "11":
            if not require_profile(user):
                continue
            job_name = input("Enter Job Name: ").strip()
            selected = job.search_job(job_name)
            if selected:
                job_queue.enqueue(selected["title"])
                db.add_application(user.user_id, selected["title"])
                print("\nApplication Added To Queue")

        elif choice == "12":
            if not require_profile(user):
                continue
            # Applications are persisted in SQLite; rebuild the FIFO queue from saved records.
            saved_applications = db.get_applications(user.user_id)
            job_queue = JobQueue()
            for application in saved_applications:
                job_queue.enqueue(application[2])
            job_queue.display()

        elif choice == "19":
            if not require_profile(user):
                continue
            profile_analyzer.analyze(user, job.get_jobs(), db)

        elif choice == "20":
            if not require_profile(user):
                continue
            profile_analyzer.show_history(user, db)

        elif choice == "13":
            print("\nThank You For Using Skill Match AI")
            db.close_connection()
            break

        elif choice == "14":
            user.view_skill_history()

        elif choice == "15":
            print("\n===== DATABASE RECORDS =====")
            print("\nUsers:")
            for record in db.get_users():
                print(record)

            print("\nJobs:")
            for record in db.get_jobs():
                print(record)

            print("\nApplications:")
            for record in db.get_applications(user.user_id if user.user_id else None):
                print(record)

        elif choice == "16":
            if not require_profile(user):
                continue
            results = build_results(user, job.get_jobs(), matcher)
            recommendations = recommender.recommend(results)
            report.export_pdf(user, recommendations)

        elif choice == "17":
            if not require_profile(user):
                continue
            results = build_results(user, job.get_jobs(), matcher)
            chart.show_dashboard(results)

        elif choice == "18":
            saved_users = db.get_users()
            if not saved_users:
                print("\nNo saved profiles found. Create a profile first.")
                continue
            print("\n===== SAVED PROFILES =====")
            for saved_id, saved_name in saved_users:
                print(f"{saved_id}. {saved_name}")
            raw_id = input("Enter profile ID to load: ").strip()
            try:
                user.load_profile(int(raw_id))
            except ValueError:
                print("Please enter a valid numeric profile ID.")

        else:
            print("\nInvalid Choice. Please enter 1-20.")


if __name__ == "__main__":
    main()
