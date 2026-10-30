from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database
from job import Job
from skill_utils import normalize_skill, unique_skills
from course_recommender import CourseRecommender
from matching_engine import WeightedMatchingEngine
from roadmap import build_daily_roadmap

app = Flask(__name__)
app.secret_key = "skill-match-ai-local-demo-change-this"


def load_data():
    db = Database()
    jobs = Job(db).get_jobs()  # seeds original roles and reuses the DSA linked-list job layer
    profiles = []
    for uid, name in db.get_users():
        profile = db.get_user_profile(uid)
        if profile:
            profiles.append(profile)
    return db, jobs, profiles


def weighted_analysis(profile, job):
    """Compatibility wrapper used by existing Flask routes and templates."""
    return WeightedMatchingEngine().analyze(profile, job)


def close(db):
    db.close_connection()


@app.route("/")
def dashboard():
    db, jobs, profiles = load_data()
    analyses = db.cursor.execute("""
        SELECT pa.id, u.name, pa.target_job, pa.match_percent, pa.created_at
        FROM profile_analyses pa JOIN users u ON u.id=pa.user_id
        ORDER BY pa.id DESC LIMIT 6
    """).fetchall()
    stats = {
        "profiles": db.get_profile_count(),
        "jobs": len(jobs),
        "analyses": db.get_analysis_count(),
        "applications": len(db.get_applications())
    }
    close(db)
    return render_template("dashboard.html", profiles=profiles, jobs=jobs, stats=stats, analyses=analyses)


@app.route("/profiles/new", methods=["GET", "POST"])
def create_profile():
    db, jobs, profiles = load_data()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        education = request.form.get("education", "").strip()
        interests = request.form.get("interests", "").strip()
        target_job = request.form.get("target_job", "").strip()
        skills = unique_skills(request.form.get("skills", "").split(","))
        if not name:
            flash("Please enter a name.", "error")
        elif not skills:
            flash("Please enter at least one skill.", "error")
        else:
            existing = db.get_user_by_name(name)
            if existing:
                uid = existing[0]
                db.update_profile(uid, name, education, interests, target_job)
                for skill in skills:
                    db.add_skill(uid, skill)
                flash(f"Existing profile #{uid} updated; new skills were added without duplicates.", "success")
                close(db)
                return redirect(url_for("profile_detail", user_id=uid))
            uid = db.add_user(name, education, interests, target_job)
            for skill in skills:
                db.add_skill(uid, skill)
            flash(f"Profile saved successfully. Profile ID: {uid}", "success")
            close(db)
            return redirect(url_for("profile_detail", user_id=uid))
    close(db)
    return render_template("profile_form.html", jobs=jobs, profile=None)


@app.route("/profiles/<int:user_id>")
def profile_detail(user_id):
    db, jobs, profiles = load_data()
    profile = db.get_user_profile(user_id)
    if not profile:
        close(db)
        flash("Profile not found.", "error")
        return redirect(url_for("dashboard"))
    analyses = db.get_profile_analyses(user_id)
    close(db)
    return render_template("profile.html", profile=profile, jobs=jobs, analyses=analyses)


@app.route("/profiles/<int:user_id>/edit", methods=["GET", "POST"])
def edit_profile(user_id):
    db, jobs, profiles = load_data()
    profile = db.get_user_profile(user_id)
    if not profile:
        close(db)
        flash("Profile not found.", "error")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Name cannot be empty.", "error")
        else:
            db.update_profile(user_id, name, request.form.get("education", ""),
                              request.form.get("interests", ""), request.form.get("target_job", ""))
            for skill in unique_skills(request.form.get("skills", "").split(",")):
                db.add_skill(user_id, skill)
            flash("Profile updated. Any new skills were added.", "success")
            close(db)
            return redirect(url_for("profile_detail", user_id=user_id))
    close(db)
    return render_template("profile_form.html", jobs=jobs, profile=profile)


@app.post("/profiles/<int:user_id>/skills")
def add_skill(user_id):
    skill = request.form.get("skill", "").strip()
    db, jobs, profiles = load_data()
    profile = db.get_user_profile(user_id)
    if not profile:
        close(db)
        flash("Profile not found.", "error")
        return redirect(url_for("dashboard"))
    if not skill:
        flash("Enter a skill first.", "error")
    elif db.add_skill(user_id, skill):
        flash(f"{skill} added to profile.", "success")
    else:
        flash("That skill is already in the profile.", "error")
    close(db)
    return redirect(url_for("profile_detail", user_id=user_id))


@app.post("/profiles/<int:user_id>/skills/delete")
def remove_skill(user_id):
    db, jobs, profiles = load_data()
    skill = request.form.get("skill", "")
    if db.delete_skill(user_id, skill):
        flash(f"{skill} removed.", "success")
    else:
        flash("Skill could not be removed.", "error")
    close(db)
    return redirect(url_for("profile_detail", user_id=user_id))


@app.post("/profiles/<int:user_id>/delete")
def delete_profile(user_id):
    db, jobs, profiles = load_data()
    deleted = db.delete_profile(user_id)
    close(db)
    flash("Profile and its analysis history deleted." if deleted else "Profile not found.",
          "success" if deleted else "error")
    return redirect(url_for("dashboard"))


@app.route("/profiles/<int:user_id>/analyze", methods=["GET", "POST"])
def analyze_profile(user_id):
    db, jobs, profiles = load_data()
    profile = db.get_user_profile(user_id)
    if not profile:
        close(db)
        flash("Profile not found.", "error")
        return redirect(url_for("dashboard"))
    target_title = request.values.get("target_job", "").strip() or profile["target_job"]
    selected_job = next((j for j in jobs if j["title"].casefold() == target_title.casefold()), None)
    result = weighted_analysis(profile, selected_job) if selected_job else None
    if request.method == "POST":
        if not selected_job:
            flash("Choose a valid target career.", "error")
        else:
            analysis_id = db.save_profile_analysis(
                user_id, selected_job["title"], result["score"],
                result["matched"], result["missing"]
            )
            flash("Analysis calculated and saved to your database.", "success")
            close(db)
            return redirect(url_for("analysis_result", user_id=user_id,
                                    target_job=selected_job["title"],
                                    analysis_id=analysis_id))
    close(db)
    return render_template("analyze.html", profile=profile, jobs=jobs,
                           selected_title=target_title, result=result)


@app.route("/profiles/<int:user_id>/analysis")
def analysis_result(user_id):
    target_title = request.args.get("target_job", "")
    requested_analysis_id = request.args.get("analysis_id", type=int)
    db, jobs, profiles = load_data()
    profile = db.get_user_profile(user_id)
    selected_job = next((j for j in jobs if j["title"].casefold() == target_title.casefold()), None)
    if not profile or not selected_job:
        close(db)
        flash("Profile or job was not found.", "error")
        return redirect(url_for("dashboard"))
    result = weighted_analysis(profile, selected_job)
    analysis = db.get_profile_analysis(user_id, selected_job["title"], requested_analysis_id)
    if analysis is None:
        analysis = db.get_profile_analysis(user_id, selected_job["title"])
    if analysis is None:
        analysis_id = db.save_profile_analysis(
            user_id, selected_job["title"], result["score"],
            result["matched"], result["missing"]
        )
        analysis = db.get_profile_analysis(user_id, selected_job["title"], analysis_id)
    result = WeightedMatchingEngine().analyze(
        {"skills": analysis["matched_skills"]}, selected_job
    )
    courses = CourseRecommender()
    recommendations = [{"skill": skill, "course": courses.recommend_course(skill)}
                       for skill in result["missing"]]
    missing_skills = analysis["missing_skills"]
    skill_weights = {
        skill: WeightedMatchingEngine().skill_weight(skill, selected_job)
        for skill in missing_skills
    }
    roadmap = build_daily_roadmap(
        missing_skills, selected_job["title"], skill_weights
    )
    db.save_roadmap_tasks(
        user_id, selected_job["title"], roadmap, analysis_id=analysis["id"]
    )
    saved_tasks = db.get_roadmap_tasks(
        user_id, selected_job["title"], analysis_id=analysis["id"]
    )
    completed_count = sum(1 for item in saved_tasks if item["completed"])
    roadmap_progress = round(completed_count / 30 * 100)
    history = db.get_profile_analyses(user_id)
    close(db)
    return render_template("analysis_result.html", profile=profile, job=selected_job,
                           result=result, courses=recommendations, roadmap=saved_tasks,
                           roadmap_completed=completed_count, roadmap_progress=roadmap_progress,
                           history=history, analysis_id=analysis["id"])


@app.route("/jobs")
def jobs_page():
    db, jobs, profiles = load_data()
    close(db)
    return render_template("jobs.html", jobs=jobs)


@app.post("/profiles/<int:user_id>/roadmap/task/<int:day>")
def update_roadmap_task(user_id, day):
    target_job = request.form.get("target_job", "").strip()
    analysis_id = request.form.get("analysis_id", type=int)
    completed = request.form.get("completed", "0") == "1"
    db, jobs, profiles = load_data()
    profile = db.get_user_profile(user_id)
    valid_job = next((j for j in jobs if j["title"].casefold() == target_job.casefold()), None)
    if not profile or not valid_job or not 1 <= day <= 30:
        close(db)
        flash("Profile, career, or roadmap day was not valid.", "error")
        return redirect(url_for("dashboard"))
    # Ensure tasks exist if a user submits from an older/open report tab.
    result = weighted_analysis(profile, valid_job)
    analysis = db.get_profile_analysis(user_id, valid_job["title"], analysis_id)
    if analysis is None:
        analysis = db.get_profile_analysis(user_id, valid_job["title"])
    if analysis is None:
        saved_id = db.save_profile_analysis(
            user_id, valid_job["title"], result["score"],
            result["matched"], result["missing"]
        )
        analysis = db.get_profile_analysis(user_id, valid_job["title"], saved_id)
    missing_skills = analysis["missing_skills"]
    skill_weights = {
        skill: WeightedMatchingEngine().skill_weight(skill, valid_job)
        for skill in missing_skills
    }
    db.save_roadmap_tasks(
        user_id, valid_job["title"],
        build_daily_roadmap(missing_skills, valid_job["title"], skill_weights),
        analysis_id=analysis["id"],
    )
    updated = db.set_roadmap_task_completed(
        user_id, valid_job["title"], day, completed, analysis_id=analysis["id"]
    )
    close(db)
    if updated:
        flash(f"Day {day:02d} marked {'complete' if completed else 'not complete'}.", "success")
    else:
        flash("That roadmap task could not be found.", "error")
    return redirect(url_for(
        "analysis_result", user_id=user_id, target_job=valid_job["title"],
        analysis_id=analysis["id"]
    ))


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Local development only. For deployment, use a production WSGI server.
    app.run(debug=True, host="127.0.0.1", port=5000)
