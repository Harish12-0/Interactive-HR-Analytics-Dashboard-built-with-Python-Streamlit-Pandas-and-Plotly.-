from pathlib import Path
import re
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="PeoplePulse | HR Analytics", page_icon="👥", layout="wide")

ROOT = Path(__file__).parent
DEMO_PATH = ROOT / "data" / "hr_employee_demo.csv"
NAVY = "#17365D"
BLUE = "#3D8FE8"
SKY = "#A9D2F5"
GOLD = "#C79A6B"
PALE = "#E5F0FA"

st.markdown("""
<style>
.stApp { background: #F5F9FD; }
.block-container { padding-top: 1.6rem; }
[data-testid="stMetric"] {
  background: #FFFFFF; padding: 14px 16px; border-radius: 12px;
  border: 1px solid #DCE8F4; box-shadow: 0 2px 8px rgba(23,54,93,.05);
}
[data-testid="stMetricLabel"] { color: #35516F; }
[data-testid="stMetricValue"] { color: #17365D; }
h1,h2,h3 { color: #17365D; }
</style>
""", unsafe_allow_html=True)

REQUIRED = [
    "EmployeeID", "FullName", "Gender", "Age", "Department", "JobTitle",
    "City", "EducationLevel", "HireDate", "TerminationDate", "AnnualSalary",
    "PerformanceRating", "Manager", "RecruitmentSource", "LastPromotionYear",
    "OvertimeHours", "TrainingHoursLastYear", "JobSatisfaction", "WorkMode", "ExitReason"
]

def parse_salary(series):
    cleaned = series.astype("string").str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(cleaned, errors="coerce")

@st.cache_data(show_spinner=False)
def load_data(file_bytes=None):
    if file_bytes is None:
        df = pd.read_csv(DEMO_PATH)
    else:
        from io import BytesIO
        df = pd.read_csv(BytesIO(file_bytes))
    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    df["HireDate"] = pd.to_datetime(df["HireDate"], errors="coerce", dayfirst=True)
    df["TerminationDate"] = pd.to_datetime(df["TerminationDate"], errors="coerce", dayfirst=True)
    for col in ["Age", "PerformanceRating", "LastPromotionYear", "OvertimeHours",
                "TrainingHoursLastYear", "JobSatisfaction"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["AnnualSalary"] = parse_salary(df["AnnualSalary"])

    for col in ["Gender", "Department", "JobTitle", "City", "EducationLevel",
                "Manager", "RecruitmentSource", "WorkMode", "ExitReason"]:
        df[col] = df[col].astype("string").str.strip()

    df["Gender"] = df["Gender"].str.lower().replace({
        "m": "Male", "male": "Male", "f": "Female", "female": "Female",
        "non-binary": "Other", "prefer not to say": "Not specified"
    }).fillna("Not specified")
    df["Department"] = df["Department"].str.replace(r"\s+", " ", regex=True).str.title()
    df["City"] = df["City"].str.title()
    df["WorkMode"] = df["WorkMode"].str.title()
    df["IsActive"] = df["TerminationDate"].isna()
    df["HireYear"] = df["HireDate"].dt.year
    df["HireMonth"] = df["HireDate"].dt.to_period("M").dt.to_timestamp()
    df["AgeBand"] = pd.cut(
        df["Age"], bins=[0, 25, 35, 45, 55, 100],
        labels=["18–25", "26–35", "36–45", "46–55", "56+"], include_lowest=True
    )
    return df

st.title("👥 PeoplePulse | HR Analytics Dashboard")
st.caption("Workforce overview · Hiring · Retention · Compensation · Employee experience")

with st.sidebar:
    st.header("Dashboard filters")
    uploaded = st.file_uploader("Upload HR CSV", type=["csv"])
    try:
        data = load_data(uploaded.getvalue() if uploaded else None)
    except Exception as exc:
        st.error(f"Unable to load the dataset: {exc}")
        st.stop()

    valid_years = data["HireYear"].dropna().astype(int)
    if valid_years.empty:
        st.error("No valid HireDate values were found.")
        st.stop()
    min_year, max_year = int(valid_years.min()), int(valid_years.max())
    year_range = st.slider("Hire year range", min_year, max_year, (min_year, max_year))
    dept_options = sorted(data["Department"].dropna().unique().tolist())
    dept_selected = st.multiselect("Department", dept_options, default=dept_options)
    city_options = sorted(data["City"].dropna().unique().tolist())
    city_selected = st.multiselect("City", city_options, default=city_options)
    mode_options = sorted(data["WorkMode"].dropna().unique().tolist())
    mode_selected = st.multiselect("Work mode", mode_options, default=mode_options)

filtered = data[
    data["HireYear"].between(year_range[0], year_range[1])
    & data["Department"].isin(dept_selected)
    & data["City"].isin(city_selected)
    & data["WorkMode"].isin(mode_selected)
].copy()

if filtered.empty:
    st.warning("No employees match these filters. Adjust the filters in the sidebar.")
    st.stop()

total = len(filtered)
active = int(filtered["IsActive"].sum())
exited = total - active
exit_rate = exited / total * 100 if total else 0
avg_salary = filtered.loc[filtered["IsActive"], "AnnualSalary"].mean()
avg_satisfaction = filtered["JobSatisfaction"].mean()
avg_rating = filtered["PerformanceRating"].mean()

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Employees in View", f"{total:,}")
m2.metric("Active Employees", f"{active:,}")
m3.metric("Exit Rate", f"{exit_rate:.1f}%")
m4.metric("Avg. Active Salary", f"₹{avg_salary:,.0f}" if pd.notna(avg_salary) else "N/A")
m5.metric("Avg. Satisfaction", f"{avg_satisfaction:.2f}/5" if pd.notna(avg_satisfaction) else "N/A")

st.divider()
left, middle, right = st.columns([1, 1.4, 1], gap="medium")

with left:
    st.subheader("Employees by Department")
    dept_counts = filtered.groupby("Department", as_index=False).size().rename(columns={"size":"Employees"})
    fig = px.bar(dept_counts.sort_values("Employees"), x="Employees", y="Department",
                 orientation="h", color="Employees", color_continuous_scale=[PALE, BLUE, NAVY])
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=4,r=4,t=8,b=8),
                      plot_bgcolor="white", paper_bgcolor="white", xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with middle:
    st.subheader("Hiring Trend by Year")
    hires = filtered.dropna(subset=["HireYear"]).groupby("HireYear").size().reset_index(name="Hires")
    hires["HireYear"] = hires["HireYear"].astype(int)
    fig = px.line(hires, x="HireYear", y="Hires", markers=True)
    fig.update_traces(line_color=NAVY, line_width=3, marker_color=BLUE)
    fig.update_layout(margin=dict(l=4,r=4,t=8,b=8), plot_bgcolor="white",
                      paper_bgcolor="white", xaxis_title="Hire year", yaxis_title="Employees hired")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Work Mode Mix")
    mode_counts = filtered.groupby("WorkMode", as_index=False).size().rename(columns={"size":"Employees"})
    fig = px.pie(mode_counts, names="WorkMode", values="Employees", hole=.58,
                 color_discrete_sequence=[NAVY, BLUE, GOLD, SKY])
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(l=4,r=4,t=8,b=8), paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

left2, right2 = st.columns([1.2, 1], gap="medium")
with left2:
    st.subheader("Average Salary by Department (Active Employees)")
    salary_data = filtered[filtered["IsActive"] & filtered["AnnualSalary"].notna()]
    if salary_data.empty:
        st.info("No active employee salary values are available for this filter.")
    else:
        salary_dept = salary_data.groupby("Department", as_index=False)["AnnualSalary"].mean().sort_values("AnnualSalary")
        fig = px.bar(salary_dept, x="AnnualSalary", y="Department", orientation="h",
                     color="AnnualSalary", color_continuous_scale=[PALE, BLUE, NAVY],
                     labels={"AnnualSalary":"Average annual salary (₹)", "Department":""})
        fig.update_layout(coloraxis_showscale=False, margin=dict(l=4,r=4,t=8,b=8),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

with right2:
    st.subheader("Exit Reasons")
    exits = filtered[~filtered["IsActive"]]
    reason_data = exits["ExitReason"].fillna("Not recorded").value_counts().rename_axis("Exit Reason").reset_index(name="Exits")
    if exits.empty:
        st.info("No exited employees in the selected view.")
    else:
        fig = px.bar(reason_data.head(8), x="Exits", y="Exit Reason", orientation="h",
                     color="Exits", color_continuous_scale=[PALE, GOLD, NAVY])
        fig.update_layout(coloraxis_showscale=False, margin=dict(l=4,r=4,t=8,b=8),
                          plot_bgcolor="white", paper_bgcolor="white", xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Workforce Snapshot")
a, b, c = st.columns(3)
with a:
    st.markdown("**Age distribution**")
    age_data = filtered.dropna(subset=["AgeBand"]).groupby("AgeBand", observed=False).size().reset_index(name="Employees")
    fig = px.bar(age_data, x="AgeBand", y="Employees", color_discrete_sequence=[BLUE])
    fig.update_layout(margin=dict(l=4,r=4,t=8,b=8), plot_bgcolor="white", paper_bgcolor="white",
                      xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with b:
    st.markdown("**Performance rating distribution**")
    rating_data = filtered["PerformanceRating"].dropna().astype(int).value_counts().sort_index().rename_axis("Rating").reset_index(name="Employees")
    if rating_data.empty:
        st.info("No performance rating values.")
    else:
        fig = px.bar(rating_data, x="Rating", y="Employees", color_discrete_sequence=[GOLD])
        fig.update_layout(margin=dict(l=4,r=4,t=8,b=8), plot_bgcolor="white", paper_bgcolor="white",
                          xaxis_title="Rating (1–5)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
with c:
    st.markdown("**Job satisfaction distribution**")
    satisfaction_data = filtered["JobSatisfaction"].dropna().astype(int).value_counts().sort_index().rename_axis("Satisfaction").reset_index(name="Employees")
    if satisfaction_data.empty:
        st.info("No satisfaction values.")
    else:
        fig = px.bar(satisfaction_data, x="Satisfaction", y="Employees", color_discrete_sequence=[NAVY])
        fig.update_layout(margin=dict(l=4,r=4,t=8,b=8), plot_bgcolor="white", paper_bgcolor="white",
                          xaxis_title="Score (1–5)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

with st.expander("Data quality summary"):
    quality = pd.DataFrame({
        "Column": filtered.columns,
        "Missing values": [int(filtered[col].isna().sum()) for col in filtered.columns],
        "Missing %": [round(float(filtered[col].isna().mean() * 100), 1) for col in filtered.columns],
    })
    st.dataframe(quality, use_container_width=True, hide_index=True)

st.caption(
    "Privacy note: employee-level HR information is sensitive. This dashboard does not display names or employee IDs, "
    "but uploaded files are processed in the app session. Do not publish identifiable HR records or deploy with sensitive "
    "data unless your organization has approved the access and hosting arrangements."
)
