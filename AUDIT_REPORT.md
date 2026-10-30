# Skill Match AI — Code Audit and Upgrade Notes

## Scope inspected

The supplied ZIP contains 15 original files: 13 Python modules, `README.md`, and `requirements.txt`. All original Python modules compiled successfully before changes.

## Changes made

- Added `skill_utils.py` for consistent skill normalization, common aliases, and duplicate removal.
- Updated `matcher.py` so aliases are matched consistently and empty/invalid skills are ignored safely.
- Updated `skill_gap.py` to use the same normalization as the matcher.
- Updated `database.py` to enable SQLite foreign-key enforcement, prevent duplicate skills, and load users/profiles.
- Updated `user.py` to restore saved profiles, reuse a profile when the name already exists, and prevent duplicate skills.
- Added menu option 18 to load an existing profile.
- Updated application queue display to reconstruct FIFO order from persisted SQLite application records.
- Updated `course_recommender.py` to accept aliases and added a Power BI course suggestion.
- Escaped user-provided strings in PDF paragraphs to avoid malformed ReportLab markup.
- Added `.gitignore` to exclude virtual environments, caches, generated reports/charts, and local databases.
- Expanded `README.md` and added an automated test suite.

## Test results

Run with `python -m unittest discover -s tests -v`. Tests cover skill normalization, duplicate handling, scoring, alias matching, recommendation ordering/limits, skill gaps, course aliases, profile persistence/loading, job seeding, and application history persistence.

## Known limitations / next steps

- The archive is a command-line Python app, not a web application. Flask/React files are not included.
- The job catalog is hard-coded in `job.py`; move it to a versioned JSON dataset if non-code editing is needed.
- Course recommendations are offline titles, not verified live course URLs.
- Skill-history stack is session-only; profile skills themselves persist in SQLite.
- Matching uses exact normalized skill categories, not semantic similarity or a trained model.
- PDF and chart output should be tested on the target machine with optional dependencies installed.
- The tests validate core modules but are not a substitute for a manual end-to-end run of all 18 menu options.
