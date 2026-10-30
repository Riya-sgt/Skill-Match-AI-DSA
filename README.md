# 🚀 SKILL MATCH AI

### Intelligent Career Recommendation & Skill Gap Analysis System

**A Python-based Data Structures and Algorithms (DSA) project with a Flask web dashboard and SQLite database.**

Skill Match AI is a career recommendation system designed to help students and job seekers discover suitable career opportunities based on their skills, explore job roles, identify skill gaps, and follow personalized learning roadmaps.

The system uses data structures, algorithms, skill normalization, and weighted matching techniques to generate transparent career recommendations. It combines a Python console application with a responsive web dashboard.

<p align="center">
  <a href="https://skill-match-ai-dsa.onrender.com/"><strong>🌐 Live Demo</strong></a> •
  <a href="https://github.com/Riya-sgt/Skill-Match-AI-DSA"><strong>💻 GitHub Repository</strong></a>
</p>

---

## 📌 Project Information

| Detail | Description |
|---|---|
| Project Name | SKILL MATCH AI |
| Project Type | Academic Project |
| Domain | Computer Science – AI & ML |
| Programming Language | Python |
| Backend | Flask |
| Database | SQLite |
| Interface | Python Console + Web Dashboard |
| Recommendation Approach | Rule-based weighted skill matching |
| Deployment | Render |

---

## 📑 Table of Contents

1. Project Overview
2. Problem Statement
3. Project Objectives
4. Key Features
5. How It Works
6. Technology Stack
7. DSA Concepts Implemented
8. Career Matching Logic
9. Personalized 30-Day Learning Roadmap
10. Database Management
11. Project Structure
12. Installation and Setup
13. Running the Application
14. Live Deployment
15. Running Tests
16. Security and Limitations
17. Future Enhancements
18. Author

---

## 🎯 1. Project Overview

Choosing the right career can be challenging, especially for students and fresh graduates who are unsure which job roles match their existing skills.

**SKILL MATCH AI** addresses this challenge by analyzing a user's profile and comparing their skills with predefined job requirements.

The system provides:

- Ranked career recommendations.
- Career match percentages.
- Matched and missing skill details.
- Course-title suggestions.
- Personalized 30-day learning roadmaps.
- Daily learning progress tracking.
- Career analysis reports and history.
- Job application management.

The project demonstrates how fundamental Data Structures and Algorithms can be applied to solve a practical career guidance problem.

## ❗ 2. Problem Statement

Students and job seekers often struggle to identify suitable career opportunities because they may not know:

- Which job roles match their existing skills.
- What skills are required for a particular career.
- Which important skills they are missing.
- What they should learn to become job-ready.
- How to organize their learning into achievable daily goals.

Skill Match AI provides a structured approach to address these challenges through skill comparison, career ranking, skill-gap analysis, and personalized learning plans.

## 🎯 3. Project Objectives

1. Develop a system that recommends suitable careers based on user skills.
2. Apply DSA concepts to manage and process career-related information.
3. Calculate career-fit scores using transparent matching logic.
4. Identify skill gaps between user profiles and job requirements.
5. Suggest relevant learning areas and courses.
6. Generate personalized 30-day learning roadmaps.
7. Store user profiles, analyses, and progress using SQLite.
8. Provide an accessible web dashboard alongside the original console application.

## ✨ 4. Key Features

### 1. User Profile Management
- Create and manage user profiles.
- Add, view, edit, and remove skills.
- Store education, interests, target careers, and profile information.
- Load previously saved profiles.
- Perform case-insensitive, alias-aware checks for duplicate skills.

### 2. Career Recommendation Engine
- Includes 20 predefined job roles.
- Compares user skills against job requirements.
- Uses normalized skill names and weighted matching.
- Ranks career recommendations by match percentage.
- Displays the top five recommendations.

### 3. Skill Gap Analysis
- Identifies matched skills.
- Highlights missing or underdeveloped skills.
- Calculates career-fit percentages.
- Helps users identify the skills they need to improve.

### 4. Course Suggestions
- Provides offline course-title suggestions based on skill gaps.
- Identifies learning areas relevant to the selected career.

### 5. Personalized 30-Day Learning Roadmap
- Generates exactly 30 progressive daily learning tasks.
- Adapts roadmap content to the selected career and identified skill gaps.
- Provides learning objectives, explanations, practical activities, expected outcomes, and estimated durations.
- Includes a final assessment on Day 30.
- Supports marking tasks as complete or incomplete.
- Displays overall learning progress.

### 6. Dashboard and Career Library
- Responsive dark-navy web interface.
- Career exploration and profile management.
- Career matching and analysis details.
- Learning roadmap and progress tracking.

### 7. Reports and Analytics
- Generate text-based reports.
- Optional PDF report export.
- Optional chart generation and statistics dashboard.
- View saved career analysis history.

### 8. Job Application Management
- Maintain job application history.
- Display saved applications in FIFO submission order using a queue.
- View database records.

### 9. Data Persistence
- Store profiles, skills, jobs, applications, and analysis history in SQLite.
- Load saved profiles after restarting the application when the database file is retained.
- Persist roadmap tasks and completion progress.

## ⚙️ 5. How It Works

The application follows this workflow:

1. **Create Profile:** Enter personal, educational, and career-related information.
2. **Add Skills:** Add current technical and complementary skills.
3. **Explore Careers:** Browse available job roles or select a target career.
4. **Analyze Skills:** The system normalizes skills and compares them with job requirements.
5. **Calculate Match:** The matching engine calculates career-fit scores.
6. **Identify Skill Gaps:** View matched and missing skills.
7. **Get Recommendations:** Explore ranked career recommendations.
8. **Generate Roadmap:** Receive a personalized 30-day learning plan.
9. **Track Progress:** Mark daily tasks complete and monitor progress.
10. **Save Results:** Store profiles, analyses, and roadmap progress in SQLite.

## 🛠️ 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language and application logic |
| Flask | Web application framework |
| SQLite | Database and storage |
| HTML | Webpage structure |
| CSS | Styling and responsive interface |
| JavaScript | Frontend interactions |
| Matplotlib | Optional charts and visualizations |
| ReportLab | Optional PDF report generation |
| Git & GitHub | Version control and project hosting |
| unittest | Automated testing |

## 🧠 7. Data Structures & Algorithms Implemented

This project demonstrates practical applications of fundamental DSA concepts.

| Concept | Application |
|---|---|
| Singly Linked List | Stores predefined job records |
| Stack | Tracks the current profile's skill history during a session |
| Queue (FIFO) | Displays saved job applications in submission order |
| Lists | Stores skills, jobs, and recommendation results |
| Dictionaries | Represents structured profile and job information |
| Sets | Removes duplicate skills and compares skill collections |
| Searching | Searches for job titles |
| Sorting | Ranks recommendations by match percentage and title |
| File Handling | Supports report generation and project data operations |

These concepts demonstrate how DSA can be applied to organize, search, compare, and process career-related information.

## 📊 8. Career Matching Logic

The system uses a shared weighted matching engine to calculate career-fit scores.

The matching engine:

- Normalizes skill names before comparison.
- Recognizes common aliases such as `ML` and `Machine Learning`.
- Recognizes variations such as `PowerBI` and `Power BI`.
- Assigns default weights to technical and complementary skills.
- Allows individual job roles to override default skill weights.
- Calculates matched and missing skills.
- Produces ranked career recommendations.

### Weighted Matching Formula

**Match Percentage:**

`(Earned Skill Points / Total Required Skill Points) × 100`

Default weights:

- Technical/core skills: 2 points.
- Selected complementary skills: 1 point.
- Individual job definitions may override these weights.

**Important:** The current recommendation engine uses transparent, rule-based calculations. It does not train a machine-learning model or claim to provide trained AI predictions.

## 📅 9. Personalized 30-Day Learning Roadmap

The roadmap generator creates a structured learning plan based on the selected career and the missing skills identified through career analysis.

Each daily task includes:

- Unique task title.
- Learning objective.
- Detailed explanation.
- Practical activity.
- Expected outcome.
- Estimated duration.
- Learning phase.
- Completion status.

### Roadmap Capabilities

- Exactly 30 progressive daily tasks.
- Dedicated curricula for Data Analyst, Data Scientist, and DevOps Engineer roles.
- Career-relevant exercises for other supported roles.
- Skill-gap-based learning activities.
- Separate final assessment on Day 30.
- Expandable daily lesson details.
- Persistent task completion tracking.
- Overall progress displayed as completed tasks out of 30 and percentage.

Roadmap content can be regenerated without resetting existing completion progress for the same profile and career.

## 🗄️ 10. Database Management

The application uses **SQLite** for data storage.

The database supports:

- User profiles and profile metadata.
- User skills.
- Job records.
- Saved career analyses.
- Job application history.
- Personalized roadmap tasks.
- Daily task completion progress.

Database migrations are included for supported schema upgrades while retaining existing records.

The database file `skillmatch.db` is created automatically in the working directory when the application initializes the database.

**Important:** Keep a backup of the database file if you want to preserve saved profiles and learning progress.

## 📁 11. Project Structure

The project contains Python application modules, Flask routes, templates, static assets, tests, and database functionality.

Important components include:

| Component | Responsibility |
|---|---|
| `main.py` | Original Python console application |
| `app.py` | Flask web application |
| `database.py` | SQLite database operations |
| `matching_engine.py` | Shared weighted career matching |
| `matcher.py` | Skill matching functionality |
| `profile_analyzer.py` | Profile and career analysis |
| `recommendation.py` | Career recommendation logic |
| `skill_gap.py` | Skill gap identification |
| `roadmap.py` | 30-day roadmap generation |
| `report_generator.py` | Report generation |
| `job.py` | Job-related functionality |
| `user.py` | User-related functionality |
| `templates/` | HTML templates |
| `static/` | CSS, JavaScript, and static assets |
| `tests/` | Automated test cases |
| `requirements.txt` | Python dependencies |

*Refer to the repository for the complete current folder structure.*

## 💻 12. Installation and Setup

### Prerequisites

- Python 3.10 or newer recommended.
- Visual Studio Code or another Python editor.
- Git installed on your computer.
- A web browser.

### Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/Riya-sgt/Skill-Match-AI-DSA.git
```

### Step 2: Open the Project Folder

```bash
cd Skill-Match-AI-DSA
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## ▶️ 13. Running the Application

### Option 1: Run the Flask Web Dashboard

From the project directory:

```bash
python app.py
```

Open your browser and visit:

**http://127.0.0.1:5000**

Keep the terminal running while using the dashboard.

### Option 2: Run the Original Python Console Application

```bash
python main.py
```

The original console application remains available alongside the Flask dashboard.

## 🌐 14. Live Deployment

The Flask web application is deployed using **Render**.

<details>
<summary><strong>Deployment information</strong></summary>

| Setting | Value |
|---|---|
| Hosting Platform | Render |
| Service Type | Web Service |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Branch | `main` |
| Root Directory | Repository root |

</details>

### Open the Live Application

**Live Website:** https://skill-match-ai-dsa.onrender.com/

**GitHub Repository:** https://github.com/Riya-sgt/Skill-Match-AI-DSA

### Deployment Notes

- The first request may take longer if the free Render service has been inactive.
- The deployed application uses the server environment rather than your personal computer.
- SQLite data stored on Render's default filesystem may not survive service restarts, redeployments, or instance replacement.
- For reliable long-term data storage, configure persistent storage or migrate to a managed database.
- Do not use the public demonstration application to store sensitive personal information.

## 🧪 15. Running Tests

The project includes automated unit tests for core functionality, database operations, skill normalization, and weighted career matching.

Run the complete test suite from the project directory:

```bash
python -m unittest discover -s tests -v
```

The test suite uses temporary databases for its tests and is designed not to modify your personal `skillmatch.db` file.

## 🔐 16. Security and Limitations

- The recommendation engine is rule-based, not a trained machine-learning model.
- Course suggestions are offline title-based suggestions, not live course searches.
- The application is currently designed as a student project demonstration.
- The Flask secret key requires secure production configuration.
- Authentication and authorization are not implemented.
- CSRF protection and additional production security hardening should be implemented before handling real user data.
- SQLite data on Render's default filesystem may be temporary.
- Database backups are recommended before moving or replacing project databases.

## 🚀 17. Future Enhancements

Potential improvements include:

- Secure user registration and authentication.
- Role-based access control.
- Integration with live job listing APIs.
- Real learning-resource and course links.
- Advanced career analytics and visualizations.
- Resume analysis and skill extraction.
- Exportable career development reports.
- More career-specific learning roadmaps.
- Cloud database integration.
- Improved deployment and production security.

## 👩‍💻 18. Author

**Project:** SKILL MATCH AI – Career Recommendation System  
**Author:** Riya Malik  
**Domain:** Computer Science Engineering – Artificial Intelligence & Machine Learning  
**University:** SGT University  
**Core Technologies:** Python, DSA, Flask, SQLite

Developed as an academic project to demonstrate the practical application of Data Structures and Algorithms in career recommendation, skill analysis, and personalized learning.

---

<p align="center">
  ⭐ If you find this project interesting, consider giving the repository a star!
</p>

<p align="center">
  <strong>Built with Python, problem-solving, and a passion for technology. 🚀</strong>
</p>
