"""Career-aware, progressive learning-roadmap generation."""

PHASES = (
    (1, 7, "Foundations and setup"),
    (8, 14, "Guided practice and core exercises"),
    (15, 21, "Applied tasks and mini-project development"),
    (22, 26, "Integrated project implementation"),
    (27, 29, "Testing, improvements, documentation and portfolio"),
    (30, 30, "Final assessment, project review and next steps"),
)

DEVOPS_TASKS = (
    ("Linux files and shell navigation", "Inspect the filesystem hierarchy and practice safe navigation, listing, and file inspection.", "Navigate to a chosen directory, inspect three files, and record the commands and results.", 35),
    ("Linux users, permissions, and processes", "Learn how ownership, permissions, users, and running processes affect a service.", "Create a permissions checklist for a sample app directory and inspect a running process.", 40),
    ("Shell pipes and basic automation", "Combine shell commands with pipes, redirection, and variables to automate a repeatable check.", "Write a short shell script that checks a local file and reports a clear success or failure.", 45),
    ("Git repository and commit fundamentals", "Practice the working tree, staging area, commits, and readable commit messages.", "Create a small repository, make two focused commits, and inspect its history.", 40),
    ("Branches and collaborative changes", "Create a feature branch, make a change, and understand how branches isolate work.", "Merge a feature branch into the main branch and document the merge result.", 45),
    ("Networking: IP, DNS, and ports", "Trace how an IP address, DNS lookup, and port identify a network service.", "Use local or public DNS lookup tools and explain the destination and port of one request.", 45),
    ("HTTP requests and network troubleshooting", "Read HTTP status codes and practice a systematic connection troubleshooting sequence.", "Inspect a harmless public endpoint or local service and record its status and response headers.", 45),
    ("Guided Git conflict resolution", "Follow a guided workflow for resolving a simple merge conflict without discarding either change.", "Create a conflict in a practice repository, resolve it, and verify the resulting file.", 45),
    ("Linux service logs and diagnostics", "Use service status and log inspection concepts to identify a failing service.", "Analyze a sample log or local service output and write a short root-cause note.", 45),
    ("Networking: firewall and connectivity checks", "Practice checking reachability and relating firewall rules to required service ports.", "Build a small port-and-purpose table for an example web deployment and verify one connection.", 45),
    ("Docker images and containers", "Build an understanding of images, containers, registries, and the container lifecycle.", "Run a small public or local container image and record its ports and lifecycle commands.", 50),
    ("Writing a minimal Dockerfile", "Follow a guided example to define a reproducible image for a small application.", "Containerize a tiny app and verify that it starts with the expected command.", 55),
    ("Docker storage and networking", "Explore how container ports, networks, and persistent volumes affect an application.", "Run a container with an explicit port mapping and a persistent data directory.", 55),
    ("CI/CD pipeline stages", "Trace a basic pipeline from source checkout through build, test, and delivery.", "Draw a pipeline for a sample application and identify its inputs, outputs, and failure points.", 45),
    ("Guided CI workflow", "Create a basic automated workflow that runs checks when repository changes are pushed.", "Configure a simple CI workflow to run a harmless build or test command and inspect its result.", 60),
    ("Deploying a containerized service", "Apply Linux, networking, Git, and container concepts to deploy a small service locally.", "Deploy the containerized sample app, verify its health endpoint, and capture the run steps.", 70),
    ("Infrastructure configuration and secrets", "Practice separating configuration from code and handling secrets safely.", "Move sample settings into environment variables and confirm no secret is committed to Git.", 50),
    ("Cloud compute and storage concepts", "Compare cloud compute, storage, and identity concepts before choosing a service for an app.", "Sketch a small cloud deployment and label its compute, storage, network, and access needs.", 50),
    ("Cloud deployment plan", "Translate a service's resource needs into a practical, cost-aware cloud deployment plan.", "Write a deployment checklist with resource choices, access boundaries, and a teardown step.", 55),
    ("CI/CD release and rollback", "Plan how a release is promoted and how to recover from an unsuccessful deployment.", "Add explicit verification and rollback steps to the sample pipeline plan.", 50),
    ("Observability: logs, metrics, and alerts", "Choose useful signals for detecting whether a deployed service is healthy.", "Define three service metrics and one alert condition for the sample application.", 50),
    ("Integrated project: define the service", "Select a small app and define its build, runtime, network, and deployment requirements.", "Create project acceptance criteria and an architecture sketch for a containerized service.", 60),
    ("Integrated project: container build", "Build and run the project's container using the requirements from the previous day.", "Build the image, start the service, and verify its expected response locally.", 70),
    ("Integrated project: automate delivery", "Connect the project repository to a CI workflow that builds and tests each change.", "Run the workflow on a change and record the successful check and one failure case.", 70),
    ("Integrated project: deploy and observe", "Deploy the project to a local or available cloud environment and add a basic health check.", "Verify deployment availability and inspect logs after restarting the service.", 75),
    ("Test the deployment and recovery path", "Test normal behavior, a failure case, and the documented recovery path.", "Run a deployment checklist and demonstrate recovery from a deliberately stopped service.", 60),
    ("Document setup and operations", "Write clear setup, configuration, deployment, and troubleshooting instructions.", "Ask someone unfamiliar with the project to follow the README setup steps.", 50),
    ("Prepare the project for a portfolio", "Polish the repository presentation with a diagram, example output, and a concise project summary.", "Add a project overview and deployment evidence to the repository README.", 45),
    ("Review the pipeline and security basics", "Review permissions, exposed ports, configuration, pipeline steps, and operational gaps.", "Complete a checklist and fix or document at least one improvement.", 45),
    ("Roadmap review and next steps", "Review what you built, identify remaining DevOps gaps, and plan the next learning cycle.", "Demonstrate the project end to end and write three specific next steps.", 40),
)

DATA_SCIENTIST_TASKS = (
    ("Statistics: populations and samples", "Review populations, samples, variables, and sources of sampling bias.", "Choose a small public dataset and identify its population, sample, and possible bias.", 35),
    ("Descriptive statistics", "Calculate and interpret mean, median, spread, and outliers for a numeric variable.", "Summarize one dataset column and explain when its median is more useful than its mean.", 40),
    ("Probability and distributions", "Explore probability, common distributions, and what distribution shape says about observations.", "Plot a numeric variable's distribution and describe its shape and unusual values.", 45),
    ("SQL: filtering and sorting", "Practice selecting, filtering, and sorting records in a relational dataset.", "Write queries that answer five concrete questions using WHERE and ORDER BY.", 40),
    ("SQL: grouping and aggregation", "Use GROUP BY and aggregate functions to summarize data at a useful level.", "Produce a grouped summary and explain the meaning of each measure.", 45),
    ("Python data-analysis workflow", "Load a dataset in Python and inspect its shape, columns, types, and missing values.", "Create a short notebook that profiles a dataset and records three quality observations.", 45),
    ("Data cleaning and missing values", "Choose defensible cleaning and missing-value handling strategies for the dataset.", "Clean one messy column and compare its summary before and after the change.", 45),
    ("Guided SQL joins", "Follow a guided example joining related tables while preserving the intended row grain.", "Join two sample tables and verify row counts and unmatched records.", 45),
    ("Python transformations", "Use dataframe filtering, grouping, and derived columns to answer a concrete question.", "Create two derived features and validate their values on selected rows.", 45),
    ("Exploratory analysis and outliers", "Investigate distributions and relationships without treating correlation as causation.", "Explore two variables and write one cautious observation supported by a chart or summary.", 50),
    ("Visualization: choosing chart types", "Match chart types to comparison, distribution, and relationship questions.", "Create three charts from the dataset and write the question each chart answers.", 50),
    ("Visualization: communicate a finding", "Improve labels, scales, and annotation so a chart communicates one clear conclusion.", "Revise one chart and explain how its design avoids a misleading interpretation.", 50),
    ("Machine learning: problem framing", "Translate a question into a prediction target, unit of analysis, and baseline.", "Define a supervised-learning problem and identify target leakage risks.", 50),
    ("Train and validation data", "Split data appropriately and explain why evaluation data must stay separate.", "Create a reproducible train/test split and confirm target proportions where relevant.", 55),
    ("Baseline model and feature preparation", "Build a simple baseline and prepare features using a pipeline that avoids leakage.", "Train a baseline model and record its score and the chosen evaluation metric.", 60),
    ("Applied SQL-to-Python analysis", "Combine SQL extraction with Python cleaning to build a traceable analysis dataset.", "Recreate a grouped business metric in SQL and Python, then reconcile the outputs.", 60),
    ("Feature engineering exercise", "Create and validate features that express useful domain information without using future data.", "Add two candidate features and compare their distributions across the target classes.", 60),
    ("Model evaluation and metrics", "Compare suitable evaluation metrics and examine errors beyond a single aggregate score.", "Calculate at least two metrics and inspect a small set of incorrect predictions.", 60),
    ("Model comparison and cross-validation", "Compare a baseline with a second model using a consistent validation strategy.", "Run cross-validation and summarize variation in model performance.", 65),
    ("Explainability and limitations", "Explain the model's strongest signals and consider uncertainty, bias, and data limitations.", "Write a short model-card draft with intended use and three limitations.", 55),
    ("Small project: define an analysis question", "Choose a focused question that can be answered with data and define a measurable outcome.", "Write a project brief, success criteria, and a list of required data fields.", 50),
    ("Small project: acquire and validate data", "Load project data and verify types, missing values, duplicates, and row grain.", "Add reproducible validation checks and summarize any data-quality decisions.", 65),
    ("Small project: explore and visualize", "Perform focused exploratory analysis and create visuals that address the project question.", "Produce two labeled charts and write evidence-based observations beneath them.", 70),
    ("Small project: build an evaluated model", "Train a baseline and candidate model with a defensible validation approach.", "Compare both models using appropriate metrics and save the evaluation results.", 75),
    ("Small project: communicate recommendations", "Connect analysis findings to a cautious, actionable recommendation.", "Prepare a one-page results summary with evidence, caveats, and a next experiment.", 65),
    ("Test the analysis workflow", "Check data assumptions, edge cases, reproducibility, and model evaluation code.", "Run the workflow from a clean session and test at least three edge cases.", 55),
    ("Document methods and reproduce results", "Document data sources, methods, assumptions, setup, and how to reproduce the analysis.", "Ask another person to reproduce one result using only your project instructions.", 50),
    ("Prepare the portfolio case study", "Present the question, process, results, limitations, and artifacts as a concise case study.", "Add a project summary and a selected visualization or result to your portfolio draft.", 45),
    ("Review model quality and next experiments", "Review model errors, metric tradeoffs, and possible improvements without overclaiming.", "List three ranked follow-up experiments and the evidence each would test.", 45),
    ("Roadmap review and next steps", "Review the analysis project and identify the next statistics, SQL, Python, or modeling gap.", "Present the project in five minutes and write three specific learning next steps.", 40),
)

DATA_ANALYST_TASKS = (
    ("Spreadsheet workspace and data layout", "Set up a workbook with a raw-data tab, analysis tab, and clearly named fields; learn how rows and columns represent records and attributes.", "Import a small sales or service CSV, freeze headers, format the range as a table, and document its row grain.", 35),
    ("Spreadsheet formulas and references", "Use relative and absolute references to calculate consistent measures without silently changing formula inputs.", "Add revenue and average-value formulas to a sample sheet, fill them down, and verify three rows by hand.", 40),
    ("Spreadsheet cleaning and validation", "Use sorting, filters, duplicate checks, and validation rules to find common spreadsheet data-quality issues.", "Find and correct inconsistent category labels and duplicate IDs; record the before/after row counts.", 45),
    ("SQL tables and query structure", "Relate spreadsheet row-grain concepts to tables, columns, data types, and a basic SELECT query.", "Inspect a sample customers or orders table and write a query returning only the fields needed for one question.", 40),
    ("SQL filtering for business questions", "Translate a business question into WHERE conditions, null handling, and stable sorting.", "Write three queries for a date range, a category, and a combined condition; check the returned rows.", 45),
    ("SQL aggregations and grouped metrics", "Choose a meaningful grouping level and use COUNT, SUM, and AVG without confusing row counts with entity counts.", "Calculate monthly sales and order counts by category, then reconcile one result manually.", 45),
    ("Statistics for interpreting metrics", "Use center, spread, percent change, and sample size to distinguish a meaningful change from a misleading average.", "Compare mean and median order values across two groups and write a cautious interpretation.", 45),
    ("SQL joins and row-grain checks", "Join related tables using keys while checking whether one-to-many relationships multiply rows.", "Join orders to customers, compare row counts before and after, and explain any unmatched records.", 50),
    ("SQL subqueries and window functions", "Use a subquery or window function to rank, compare, or select records within a group.", "Find each category's top product and verify the ranking against a small hand-checked subset.", 50),
    ("Python notebook and data inspection", "Load a dataset in Python and inspect shape, types, missing values, and representative records before analysis.", "Create a notebook that profiles a CSV and saves a concise data dictionary.", 45),
    ("Python data cleaning", "Clean types, duplicates, missing values, and inconsistent labels using reproducible transformations.", "Create a cleaned dataframe and report row counts plus the treatment used for each issue.", 50),
    ("Python grouping and derived measures", "Use dataframe filtering, grouping, and derived columns to calculate a business metric reproducibly.", "Calculate monthly revenue and a second derived KPI, then compare the results with SQL.", 50),
    ("Data visualization fundamentals", "Choose chart forms based on whether the question concerns comparison, trend, distribution, or relationship.", "Create a trend chart and category comparison from the cleaned dataset; label axes and units.", 50),
    ("Dashboard structure and audience", "Organize a dashboard around an audience's decisions, with clear KPI definitions and useful filters.", "Sketch a dashboard wireframe with three KPIs, two charts, one filter, and a stated audience question.", 50),
    ("Mini-project: define the analysis question", "Scope a practical Data Analyst question, its audience, unit of analysis, and measurable success criteria.", "Write a project brief and list the fields and source tables needed to answer the question.", 45),
    ("Mini-project: extract with SQL", "Build a documented SQL extract for the project, retaining the correct grain and only necessary columns.", "Save the query, run row-count and key checks, and record the extract's date coverage.", 55),
    ("Mini-project: clean in Python", "Turn the extracted data into a repeatable cleaning workflow with explicit quality checks.", "Implement cleaning steps and produce a small validation report for missing, duplicate, and invalid values.", 60),
    ("Mini-project: calculate and interpret KPIs", "Calculate project KPIs and use statistical summaries to identify patterns without overstating causation.", "Create a metric table with definitions, values, denominators, and one caveat for each KPI.", 60),
    ("Mini-project: visualize the findings", "Use complementary visuals to answer the project question and show the evidence behind the result.", "Build two charts with descriptive titles and write one evidence-based finding for each.", 60),
    ("Mini-project: assemble a dashboard", "Combine project KPIs, charts, and an appropriate filter into a coherent analytical dashboard.", "Build a first dashboard draft and verify that changing its filter updates every relevant view.", 65),
    ("Mini-project: write the recommendation", "Turn analytical findings into a specific recommendation that names evidence, impact, and uncertainty.", "Write a short stakeholder summary separating observed facts from proposed actions.", 55),
    ("Integrated project: organize the analysis workflow", "Connect the project question, SQL extraction, cleaning, KPI calculations, and dashboard into a reproducible workflow.", "Create a workflow diagram and arrange project files so another analyst can identify each stage.", 50),
    ("Integrated project: implement data extraction", "Finalize the SQL extract and add checks that detect unexpected row-grain or coverage changes.", "Run the extract from a clean session and compare its row count and date range with the project brief.", 60),
    ("Integrated project: automate cleaning and metrics", "Run cleaning and KPI transformations in a repeatable order with clear field definitions.", "Execute the pipeline end to end and compare one KPI against an independent SQL calculation.", 65),
    ("Integrated project: complete dashboard interactions", "Connect validated metrics and visuals to the dashboard and ensure filters preserve accurate denominators.", "Test each filter choice and reconcile the displayed KPI values with the underlying data.", 65),
    ("Integrated project: refine the stakeholder story", "Polish the dashboard narrative so a stakeholder can move from question to evidence to recommendation.", "Ask a reviewer to find the main result and document one revision based on their feedback.", 55),
    ("Test data quality and metric edge cases", "Test empty results, missing fields, duplicate records, date boundaries, and zero denominators.", "Run a test checklist against the analysis workflow and fix or clearly report each failure.", 50),
    ("Improve usability and document the workflow", "Improve labels and accessibility, then document data sources, metric definitions, setup, and limitations.", "Follow your own instructions from a clean environment and correct any missing step.", 50),
    ("Prepare the Data Analyst portfolio case study", "Package the question, analysis workflow, dashboard, key finding, recommendation, and caveats for a portfolio audience.", "Create a concise case-study page and include a dashboard image or reproducible artifact.", 45),
    ("Final assessment and next steps", "Demonstrate the project end to end, defend its metric choices, review limitations, and choose the next skill gap to address.", "Present the project in five minutes, answer three review questions, and write three measurable follow-up goals.", 45),
)

GENERIC_TASKS = (
    ("Establish {focus_skill} foundations for {target_job}", "Define the purpose, key concepts, and professional use of {focus_skill} in a {target_job} workflow.", "Create a labeled concept map using one realistic {target_job} scenario and explain each connection.", 35),
    ("Set up a {focus_skill} practice environment", "Identify the tools, inputs, and prerequisites needed to use {focus_skill} reliably in {target_job} work.", "Prepare a small practice workspace and record the setup steps and a successful verification.", 35),
    ("Trace a {focus_skill} workflow", "Trace how {focus_skill} moves from input through decisions to a useful output in {target_job}.", "Diagram the workflow for a realistic case and label its inputs, checks, and deliverable.", 40),
    ("Apply {focus_skill} quality standards", "Identify professional quality criteria and common failure modes for {focus_skill} in this career.", "Inspect a sample result against a quality checklist and correct three specific defects.", 40),
    ("Explain {focus_skill} to a stakeholder", "Practice describing {focus_skill} without jargon while retaining the details a {target_job} stakeholder needs.", "Write a short stakeholder explanation and add one example, assumption, and limitation.", 35),
    ("Follow a guided {focus_skill} case", "Follow a worked {focus_skill} example using realistic inputs and explain why each step is needed.", "Reproduce the example from a clean starting point and compare it with the expected result.", 45),
    ("Practice {focus_skill} with increasing difficulty", "Move from a basic {focus_skill} task to a slightly more complex case while checking each result.", "Complete three progressively harder exercises and note the rule used in each.", 45),
    ("Interpret a {focus_skill} result", "Evaluate what a {focus_skill} result supports, what it does not prove, and what decision it can inform.", "Write a concise interpretation for a {target_job} audience, including supporting evidence and one caveat.", 40),
    ("Compare {focus_skill} approaches", "Compare two ways to apply {focus_skill} and choose based on accuracy, effort, and the career requirement.", "Solve one case both ways, compare the outputs, and justify the approach you would use at work.", 50),
    ("Troubleshoot a {focus_skill} failure", "Use observable symptoms and a repeatable diagnostic sequence to locate a {focus_skill} failure.", "Diagnose a prepared scenario and record the symptom, likely cause, test, and verified correction.", 45),
    ("Complete a career-specific {focus_skill} challenge", "Combine core {focus_skill} concepts to solve an unfamiliar but bounded {target_job} challenge.", "Complete the challenge against explicit acceptance criteria and capture evidence of the result.", 50),
    ("Review and correct {focus_skill} misconceptions", "Use feedback and recent practice to identify and correct gaps in your understanding of {focus_skill}.", "Redo two missed exercises without notes and explain the corrected reasoning in your own words.", 40),
    ("Apply {focus_skill} to a realistic work request", "Translate a realistic {target_job} request into a clear task and use {focus_skill} to deliver it.", "Produce the requested work artifact and annotate the decisions you made along the way.", 55),
    ("Handle {focus_skill} edge cases", "Extend your {focus_skill} approach to unusual inputs, constraints, or failure conditions common in the role.", "Test three boundary cases and document expected versus observed behavior.", 50),
    ("Connect {focus_skill} with a related career skill", "Combine {focus_skill} with another relevant capability in a complete {target_job} workflow.", "Build a small handoff between the two capabilities and verify both its input and output.", 60),
    ("Scope a {target_job} mini-project", "Define a bounded mini-project where {focus_skill} addresses a clear need in the selected career.", "Write the user need, scope, acceptance criteria, prerequisites, and a completion checklist.", 45),
    ("Build the core {focus_skill} component", "Implement the first working project component using {focus_skill} and the agreed acceptance criteria.", "Demonstrate the component with a realistic input and save the resulting artifact.", 60),
    ("Add a second project capability", "Extend the mini-project with a complementary capability while preserving the original working behavior.", "Implement the next feature and demonstrate how it connects to the day 17 component.", 60),
    ("Improve mini-project reliability", "Improve error handling, validation, or consistency so the project behaves predictably in realistic use.", "Run normal, invalid, and boundary cases; fix one defect and capture the retest result.", 55),
    ("Review the mini-project against requirements", "Assess the mini-project against its original requirements and remove unnecessary complexity.", "Complete the acceptance checklist, close one gap, and record any remaining limitation.", 50),
    ("Plan the integrated {target_job} project", "Plan an end-to-end project that combines {focus_skill} with the workflow and outcome expected in this career.", "Create an architecture or process diagram, ordered implementation steps, and a definition of done.", 50),
    ("Implement the integrated project core", "Build the central workflow using the project plan and keep assumptions, inputs, and outputs explicit.", "Run the core workflow end to end and capture a verifiable output for review.", 65),
    ("Connect and verify project components", "Connect the project's components and validate that each handoff preserves the required information.", "Exercise every transition, document one issue, and verify its correction.", 65),
    ("Add a useful project feature", "Add a practical feature based on the needs of the intended user or stakeholder.", "Demonstrate the feature against one acceptance criterion and record reviewer feedback.", 60),
    ("Finalize the integrated project", "Complete the planned workflow, resolve open issues, and ensure the project has a coherent usable finish.", "Run the full workflow from a clean starting state and verify every definition-of-done item.", 60),
    ("Test project quality and edge cases", "Test expected results, failure conditions, boundary cases, and the most important career-specific quality risks.", "Execute a test checklist, record outcomes, and fix or explicitly document each discovered issue.", 50),
    ("Improve and document the project", "Improve one usability or maintainability issue and document purpose, setup, operation, and limitations.", "Apply the improvement and verify that a new user can follow the written steps without help.", 50),
    ("Prepare portfolio evidence for {target_job}", "Package the project evidence so a reviewer can quickly understand the career problem and your contribution.", "Create a concise portfolio summary with a demonstration, outcome, and relevant artifact.", 45),
    ("Review remaining {focus_skill} gaps", "Review the project against {target_job} expectations and prioritize remaining {focus_skill} learning needs.", "Complete a self-review, rank three improvements by impact, and choose one for the next cycle.", 45),
    ("Final assessment and next steps for {target_job}", "Demonstrate the complete project, explain key decisions and limitations, then choose a measurable next career goal.", "Give a five-minute project walkthrough, answer three review questions, and write three follow-up goals.", 45),
)


def build_daily_roadmap(missing_skills, target_job="", skill_weights=None):
    """Build 30 distinct daily tasks, prioritizing the weighted skill gaps."""
    skills = list(dict.fromkeys(
        skill.strip() for skill in (missing_skills or [])
        if isinstance(skill, str) and skill.strip()
    ))
    weights = skill_weights or {}
    skill_order = {skill: index for index, skill in enumerate(skills)}
    skills.sort(key=lambda skill: (-weights.get(skill, 0), skill_order[skill]))
    if not skills:
        skills = ["Portfolio project"]
    skill_weights = {
        skill: max(1, weights.get(skill, 1)) for skill in skills
    }
    total_weight = sum(skill_weights.values())

    career = (target_job or "").casefold()
    if "devops" in career:
        curriculum = DEVOPS_TASKS
    elif "data scientist" in career:
        curriculum = DATA_SCIENTIST_TASKS
    elif "data analyst" in career:
        curriculum = DATA_ANALYST_TASKS
    else:
        curriculum = GENERIC_TASKS

    roadmap = []
    for day, (title, instructions, exercise, duration) in enumerate(curriculum, start=1):
        priority_offset = (day - 1) % total_weight
        skill = skills[0]
        for candidate in skills:
            if priority_offset < skill_weights[candidate]:
                skill = candidate
                break
            priority_offset -= skill_weights[candidate]
        target = target_job or "your target career"
        replacements = {"focus_skill": skill, "target_job": target}
        rendered_title = title.format(**replacements)
        if curriculum is GENERIC_TASKS and target.casefold() not in rendered_title.casefold():
            rendered_title = f"{rendered_title} for {target}"
        task_instructions = instructions.format(**replacements)
        practical_exercise = exercise.format(**replacements)
        task_instructions += (
            f" Apply this in a {target} workflow and connect it to your "
            f"{skill} skill gap."
        )
        practical_exercise += (
            f" Record how your result demonstrates progress on {skill} for {target}."
        )
        learning_objective = (
            f"By the end of day {day}, you can explain and demonstrate "
            f"'{rendered_title}' in a {target} workflow."
        )
        expected_outcome = (
            f"A verified work artifact demonstrating '{rendered_title}', plus a "
            f"short note showing how it addresses the {skill} gap for {target}."
        )
        phase = next(label for first, last, label in PHASES if first <= day <= last)
        roadmap.append({
            "day": day,
            "phase": phase,
            "skill": skill,
            "title": rendered_title,
            "learning_objective": learning_objective,
            "explanation": task_instructions,
            "practical_activity": practical_exercise,
            "expected_outcome": expected_outcome,
            "instructions": task_instructions,
            "exercise": practical_exercise,
            "duration": duration,
            "completed": False,
        })
    return roadmap
