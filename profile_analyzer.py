from matching_engine import WeightedMatchingEngine


class ProfileAnalyzer:
    """DSA/CLI profile analyzer using the same weighted engine as the Flask site."""

    def analyze(self, user, jobs, db, target_title=None):
        if not user.user_id:
            print("\nPlease create or load a profile first.")
            return None
        if not jobs:
            print("\nNo jobs are available to analyze.")
            return None

        if not target_title:
            if user.target_job:
                target_title = user.target_job
                print(f"Using target career from profile: {target_title}")
            else:
                print("\nAvailable target careers:")
                for index, job in enumerate(jobs, start=1):
                    print(f"{index}. {job['title']}")
                target_title = input("Enter target career title: ").strip()

        target = (target_title or "").strip().casefold()
        job = next((j for j in jobs if j["title"].strip().casefold() == target), None)
        if job is None:
            print(f"\nCareer '{target_title}' was not found. Use a title shown in the jobs list.")
            return None

        profile = {"id": user.user_id, "name": user.name, "skills": user.skills}
        result = WeightedMatchingEngine().analyze(profile, job)
        db.save_profile_analysis(user.user_id, job["title"], result["score"],
                                 result["matched"], result["missing"])

        print("\n========== PERSONALIZED PROFILE ANALYSIS ==========")
        print(f"Profile ID : {user.user_id}")
        print(f"Student    : {user.name}")
        print(f"Target job : {job['title']}")
        print(f"Weighted match: {result['score']}%")
        print(f"Matched ({len(result['matched'])}): {', '.join(result['matched']) if result['matched'] else 'None yet'}")
        print(f"Missing ({len(result['missing'])}): {', '.join(result['missing']) if result['missing'] else 'None'}")
        print("\nSkill details:")
        for item in result["details"]:
            status = "MATCHED" if item["matched"] else "MISSING"
            print(f"- {item['skill']} (weight {item['weight']}): {status}")
        print("\nNext steps:")
        if result["missing"]:
            for skill in result["missing"]:
                print(f"- Learn/practice {skill}")
        else:
            print("- You have all listed required skills. Build projects and prepare for interviews.")
        print("\nAnalysis saved to the database.")
        return {
            "target_job": job["title"], "match_percent": result["score"],
            "matched_skills": result["matched"], "missing_skills": result["missing"],
            "details": result["details"],
        }

    def show_history(self, user, db):
        if not user.user_id:
            print("\nPlease create or load a profile first.")
            return
        rows = db.get_profile_analyses(user.user_id)
        print("\n========== SAVED PROFILE ANALYSIS HISTORY ==========")
        if not rows:
            print("No saved analyses yet. Choose option 19 to analyze your profile.")
            return
        for row in rows:
            analysis_id, title, percent, matched, missing, created_at = row
            print(f"#{analysis_id} | {title} | {percent}% | {created_at}")
            print(f"  Matched: {matched or 'None'}")
            print(f"  Missing: {missing or 'None'}")
