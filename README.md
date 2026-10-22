# PeoplePulse | HR Analytics Dashboard

An interactive **HR / People Analytics dashboard** built with Python, Streamlit, Pandas, NumPy, and Plotly. It helps explore workforce composition, hiring trends, compensation, work modes, employee satisfaction, performance ratings, and recorded exits.

> **Privacy and data note:** This repository includes a fully synthetic demo dataset. It does not contain the employee rows from the uploaded raw file. HR data can contain personal and sensitive information: do not commit real employee names, IDs, manager names, salaries, or other identifiable records to a public GitHub repository. Use synthetic, aggregated, or properly approved de-identified data for portfolio demonstrations.

## Dashboard Features

- **KPI cards:** Employees in view, active employees, exit rate, average active-employee salary, and average job satisfaction.
- **Department headcount:** Compare workforce size by department.
- **Hiring trend:** View the number of hires by year.
- **Work-mode mix:** Compare remote, hybrid, and office work arrangements.
- **Salary analysis:** Compare average salary by department for active employees.
- **Exit reasons:** Review recorded exit reasons for employees with a termination date.
- **Workforce snapshot:** Explore age bands, performance ratings, and job satisfaction.
- **Interactive filters:** Filter by hire-year range, department, city, and work mode.
- **CSV upload:** Load another CSV with the expected schema.
- **Data quality summary:** Inspect missing values and missing-value percentages.

## Tech Stack

| Technology | Use |
|---|---|
| Python | Application logic |
| Streamlit | Interactive dashboard interface |
| Pandas | Data cleaning, transformation, and aggregation |
| NumPy | Synthetic sample data generation |
| Plotly | Interactive charts |
| CSV | Input dataset |

## Repository Structure

```text
hr-people-analytics-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
└── data/
    └── hr_employee_demo.csv
```

## Run Locally

### 1. Clone your GitHub repository

After creating a repository named `hr-people-analytics-dashboard`, run:

```bash
git clone https://github.com/YOUR-USERNAME/hr-people-analytics-dashboard.git
cd hr-people-analytics-dashboard
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

Open the local URL shown in the terminal (normally `http://localhost:8501`).

## Dataset Schema

The dashboard expects the following columns:

| Column | Description |
|---|---|
| `EmployeeID` | Employee identifier; do not publish real IDs |
| `FullName` | Employee name; not displayed by the dashboard |
| `Gender` | Gender category |
| `Age` | Employee age |
| `Department` | Department name |
| `JobTitle` | Job title |
| `City` | Work city |
| `EducationLevel` | Education category |
| `HireDate` | Hire date |
| `TerminationDate` | Termination date; blank for active employees |
| `AnnualSalary` | Annual salary; numeric or currency-formatted text |
| `PerformanceRating` | Performance rating, typically 1–5 |
| `Manager` | Manager name or label |
| `RecruitmentSource` | Hiring source |
| `LastPromotionYear` | Year of most recent promotion |
| `OvertimeHours` | Overtime hours |
| `TrainingHoursLastYear` | Training hours completed last year |
| `JobSatisfaction` | Satisfaction score, typically 1–5 |
| `WorkMode` | Remote, hybrid, office, or equivalent |
| `ExitReason` | Recorded reason for leaving |

Column names must match the schema. Dates are parsed with Pandas; use unambiguous ISO dates such as `YYYY-MM-DD` when preparing your data.

### Uploading a dataset

1. Open the app.
2. Choose **Upload HR CSV** in the sidebar.
3. Upload a CSV with the required columns.
4. Apply the available filters.

The dashboard normalizes some common gender and text-category variations and parses salary values that include currency symbols. Check the data quality summary and validate the source data before using results.

## KPI Definitions

- **Employees in View:** Number of rows after the active filters are applied.
- **Active Employees:** Records with no valid termination date.
- **Exit Rate:** Number of records with a termination date divided by all filtered records, multiplied by 100. This is a dataset-level share, not a formal period-based HR attrition rate.
- **Average Active Salary:** Mean annual salary among active records with a valid salary.
- **Average Satisfaction:** Mean of available job-satisfaction scores.

All KPIs and charts update when filters change. For real HR reporting, agree on the definitions and reporting period with HR stakeholders before publishing results.

## Example Business Questions

1. Which departments have the largest workforce?
2. How has hiring volume changed over time?
3. What share of employees work remotely, in hybrid mode, or in the office?
4. How does average active salary differ by department?
5. Which exit reasons are most frequently recorded?
6. How are age bands, performance ratings, and satisfaction scores distributed?
7. Are there departments where missing data needs to be addressed?

## Publish to GitHub

Create a new repository on GitHub called `hr-people-analytics-dashboard`. Then, from the project folder, run:

```bash
git init
git add .
git commit -m "Build interactive HR analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/hr-people-analytics-dashboard.git
git push -u origin main
```

If Git asks you to authenticate, use GitHub's supported sign-in or credential workflow. Never store passwords, access tokens, private company files, or raw HR records in the repository.

### Suggested repository description

> Interactive HR analytics dashboard built with Python, Streamlit, Pandas, and Plotly. Explore workforce composition, hiring trends, compensation, work modes, satisfaction, performance ratings, exits, and data quality.

### Suggested GitHub topics

`hr-analytics` · `people-analytics` · `python` · `streamlit` · `pandas` · `plotly` · `data-analytics` · `data-visualization`

## Optional Deployment

You can deploy the dashboard using Streamlit Community Cloud:

1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create an app using the repository, `main` branch, and `app.py`.
4. Deploy and test the public app.

Review current deployment settings and access controls before deployment. Do not deploy a dashboard connected to real employee data unless your organization has approved the hosting, access, and privacy arrangements.

## Limitations and Responsible Use

- The bundled data is synthetic and intended only for testing and portfolio demonstration.
- The dashboard reports patterns and associations; it does not establish causation.
- The exit-rate metric is a simple share of records with termination dates and is not a substitute for a time-based attrition calculation.
- HR decisions can affect people. Do not use these aggregate visualizations alone to make decisions about hiring, promotion, compensation, or termination.
- Validate data quality, business definitions, permissions, and privacy requirements before using real data.

## Future Enhancements

- Add a time-based attrition rate with a defined denominator and reporting period.
- Add promotion velocity and tenure analysis.
- Add year-over-year hiring and exit trends.
- Add automated data validation and unit tests.
- Add role-based access controls for approved internal deployments.
- Connect to a secure database or approved HRIS source.

## Author

**Your Name**  
Aspiring Data Analyst / HR Analytics

- GitHub: `https://github.com/YOUR-USERNAME`
- LinkedIn: `https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE/`

Replace these placeholders with your real profile links before publishing.

## License

This project includes an MIT License template. Review the `LICENSE` file and replace `Your Name` before publishing if you choose to distribute the project under that license.
