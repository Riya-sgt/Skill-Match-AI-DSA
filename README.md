# 🚀 SKILL MATCH AI
### Intelligent Career Recommendation & Skill Gap Analysis System

**A Python-based Data Structures and Algorithms (DSA) project with a Flask web dashboard and SQLite database.**

Skill Match AI is a rule-based career recommendation system that helps students and job seekers identify career opportunities based on their skills, explore matching job roles, understand skill gaps, and follow a personalized learning roadmap.

The system uses data structures, algorithms, skill normalization, and weighted matching techniques to generate transparent career recommendations. It combines a Python console application with a responsive Flask dashboard.

> **Project Type:** Python | DSA | Flask | SQLite  
> **Recommendation Approach:** Rule-based and weighted skill matching  
> **Interface:** Python Console + Web Dashboard

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Project Objectives](#-project-objectives)
4. [Key Features](#-key-features)
5. [How It Works](#-how-it-works)
6. [Technology Stack](#-technology-stack)
7. [DSA Concepts Implemented](#-data-structures--algorithms-implemented)
8. [Career Matching Logic](#-career-matching-logic)
9. [Personalized 30-Day Roadmap](#-personalized-30-day-learning-roadmap)
10. [Database Management](#-database-management)
11. [Project Structure](#-project-structure)
12. [Installation and Setup](#-installation-and-setup)
13. [Running the Application](#-running-the-application)
14. [Running Tests](#-running-tests)
15. [Security and Limitations](#-security-and-limitations)
16. [Future Enhancements](#-future-enhancements)
17. [Author](#-author)

---

## 🎯 Project Overview

Choosing the right career can be challenging, especially for students and fresh graduates who are unsure which job roles match their current skills.

**SKILL MATCH AI** addresses this challenge by analyzing a user's profile and comparing their skills with predefined job requirements.

The system provides:

- Ranked career recommendations.
- Skill match percentages.
- Matched and missing skill details.
- Offline course-title suggestions.
- Personalized 30-day learning roadmaps.
- Daily learning progress tracking.
- Reports and career analysis history.

The project demonstrates how fundamental DSA concepts can be applied to solve a practical career guidance problem.

---

## ❗ Problem Statement

Students and job seekers often struggle to identify suitable career opportunities because they may not know:

- Which job roles match their existing skills.
- What skills are required for a particular career.
- Which important skills they are missing.
- What they should learn to become job-ready.
- How to organize their learning into achievable daily goals.

Skill Match AI provides a structured, data-driven approach to address these challenges through skill comparison, career ranking, and personalized learning plans.

---

## 🎯 Project Objectives

1. Develop a system that recommends suitable careers based on user skills.
2. Apply DSA concepts to manage and process career-related information.
3. Calculate career-fit scores using transparent matching logic.
4. Identify skill gaps between user profiles and job requirements.
5. Suggest relevant learning resources and courses.
6. Generate personalized 30-day learning roadmaps.
7. Store user profiles, analyses, and progress using SQLite.
8. Provide an accessible web dashboard alongside the original console application.

---

## ✨ Key Features

### 1. User Profile Management
- Create and manage user profiles.
- Add, view, edit, and remove skills.
- Store education, interests, target careers, and profile information.
- Load previously saved profiles.
- Prevent duplicate profiles by name and duplicate skills using case-insensitive, alias-aware checks.

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
- Helps users understand what they need to learn next.

### 4. Course Suggestions
- Provides offline course-title suggestions based on skill gaps.
- Helps users identify learning areas relevant to their selected career.

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
- Load saved profiles after restarting the application.
- Persist roadmap tasks and completion progress.

---

## ⚙️ How It Works

The application follows this general workflow:

1. **Create Profile:** The user enters personal, educational, and career-related information.
2. **Add Skills:** The user adds their current technical and complementary skills.
3. **Select Career:** The user explores job roles or selects a target career.
4. **Analyze Skills:** The system normalizes skills and compares them with job requirements.
5. **Calculate Match:** The weighted matching engine calculates career-fit scores.
6. **Identify Skill Gaps:** The system displays matched and missing skills.
7. **Generate Recommendations:** Suitable careers are ranked and displayed.
8. **Create Roadmap:** A personalized 30-day learning plan is generated.
9. **Track Progress:** The user marks daily tasks complete and monitors progress.
10. **Save Results:** Profile information, analyses, and roadmap progress are stored in SQLite.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language and application logic |
| Flask | Web application framework |
| SQLite | Database and persistent storage |
| HTML | Webpage structure |
| CSS | Styling and responsive interface |
| JavaScript | Frontend interactions |
| Matplotlib | Optional charts and visualizations |
| ReportLab | Optional PDF report generation |
| Git & GitHub | Version control and project hosting |
| unittest | Automated testing |

---

## 🧠 Data Structures & Algorithms Implemented

This project demonstrates practical applications of fundamental data structures and algorithms.

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

---

## 📊 Career Matching Logic

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

By default:
- Technical/core skills have a weight of 2.
- Selected complementary skills have a weight of 1.
- Individual job definitions may override these weights.

The system uses transparent, rule-based calculations. It does **not** train a machine-learning model or claim to provide trained AI predictions.

---

## 📅 Personalized 30-Day Learning Roadmap

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

---

## 🗄️ Database Management

The application uses **SQLite** for persistent storage.

The database supports:

- User profiles and profile metadata.
- User skills.
- Job records.
- Saved career analysis.
- Job application history.
- Personalized roadmap tasks.
- Daily task completion progress.

Database migrations are included for supported schema upgrades while retaining existing records.

**Important:** The database file `skillmatch.db` is created automatically in the working directory when the application initializes the database.

Keep a backup of this file if you want to preserve your saved profiles and progress.

---

## 📁 Project Structure

The project contains Python application modules, Flask routes, templates, static assets, tests, and database functionality.

Main components include:

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

*Note: This is a component overview. Refer to the repository for the complete current folder structure.*

---

## 💻 Installation and Setup

### Prerequisites

- Python 3.10 or newer recommended.
- Visual Studio Code or another Python editor.
- Git (for cloning and version control).
- A web browser.

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/SKILL-MATCH-AI.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Open the Project Folder

```bash
cd skill_match_audit
```

Use the actual repository folder name if it differs.

### Step 3: Create a Virtual Environment (Recommended)

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

---

## ▶️ Running the Application

### Option 1: Run the Flask Web Dashboard

From the `skill_match_audit` project directory:

```bash
python app.py
```

Open the following address in your browser:

**http://127.0.0.1:5000**

Keep the terminal running while using the dashboard.

### Option 2: Run the Original Python Console Application

```bash
python main.py
```

The console application remains available alongside the Flask dashboard.

---

## 🧪 Running Tests

The project includes automated unit tests for core functionality, database operations, skill normalization, and weighted career matching.

Run the complete test suite from the `skill_match_audit` directory:

```bash
python -m unittest discover -s tests -v
```

The test suite uses temporary databases for its tests and is designed not to modify your personal `skillmatch.db` file.

---

## 🔐 Security and Limitations

- The recommendation engine is rule-based, not a trained machine-learning model.
- Course suggestions are offline title-based suggestions, not live course searches.
- The application is currently designed as a student project demonstration.
- The Flask secret key is a development placeholder.
- Authentication and authorization are not implemented.
- The application should not be exposed publicly with real personal data until authentication, CSRF protection, secure configuration, and deployment hardening are implemented.
- SQLite data must be backed up before moving or replacing project databases.

---

## 🚀 Future Enhancements

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

---

## 👩‍💻 Author

**Project:** SKILL MATCH AI – Career Recommendation System  
**Domain:** Computer Science Engineering – Artificial Intelligence & Machine Learning  
**Core Technologies:** Python, DSA, Flask, SQLite

Developed as an academic project to demonstrate the practical application of Data Structures and Algorithms in career recommendation, skill analysis, and personalized learning.

---

⭐ **If you find this project interesting, consider giving the repository a star!**

*Built with Python, problem-solving, and a passion for technology.*