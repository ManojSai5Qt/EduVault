import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="EduVault | Academic Intelligence & Database Operations",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- HIGH VISIBILITY DEVOPS THEME (ZERO GAPS, LARGE HEADERS, LUMINOUS CONTRAST) ----------
st.markdown("""
<style>
:root { color-scheme: dark; }

/* Global Obsidian Canvas */
.stApp {
  background-color: #080c16 !important;
  color: #e2e8f0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Allow smooth scrolling without cutting off */
html, body {
  overflow-x: auto !important;
  overflow-y: auto !important;
}

/* Hide Left Sidebar Completely */
[data-testid="stSidebar"] {
  display: none !important;
}
header[data-testid="stHeader"] {
  background: rgba(8, 12, 22, 0.95) !important;
}

/* Main Content Container */
.main .block-container {
  width: 100% !important;
  max-width: 1300px !important;
  margin: 0 auto !important;
  padding-top: 1rem !important;
  padding-bottom: 3.5rem !important;
  padding-left: 1.5rem !important;
  padding-right: 1.5rem !important;
  box-sizing: border-box !important;
}

/* Top Branding Bar */
.top-brand-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #0f172a;
  border: 1.5px solid #1e293b;
  border-radius: 16px;
  margin-bottom: 18px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.35);
}
.brand-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.brand-logo-sq {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  box-shadow: 0 0 18px rgba(16, 185, 129, 0.5);
}
.brand-title-text {
  font-size: 1.55rem;
  font-weight: 850;
  color: #ffffff;
  letter-spacing: -0.4px;
}
.brand-badge-pill {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 800;
  background: rgba(16, 185, 129, 0.18);
  color: #34d399;
  border: 1.5px solid #059669;
  display: flex;
  align-items: center;
  gap: 10px;
}
.dot-green {
  width: 9px;
  height: 9px;
  background-color: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 10px #10b981;
}

/* =========================================================================
   TOP NAVIGATION COMMAND DECK (ZERO GAPS, HIGH-VISIBILITY THEME)
   ========================================================================= */
.nav-card-container {
  background: #0d1527 !important;
  border: 1.5px solid #1e293b !important;
  border-radius: 16px !important;
  padding: 16px 20px !important;
  margin-bottom: 24px !important;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4) !important;
}

.nav-section-title {
  color: #94a3b8 !important;
  font-size: 0.78rem !important;
  font-weight: 800 !important;
  letter-spacing: 1.2px !important;
  text-transform: uppercase !important;
  margin-bottom: 8px !important;
}

.nav-inner-divider {
  height: 1px !important;
  background: linear-gradient(90deg, rgba(30, 41, 59, 0) 0%, rgba(51, 65, 85, 0.8) 50%, rgba(30, 41, 59, 0) 100%) !important;
  margin: 14px 0 16px 0 !important;
}

/* Universal Dot & Radio Circle Removal across ALL browsers */
div[data-testid="stRadio"] input[type="radio"],
div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child,
div[data-testid="stRadio"] [role="radiogroup"] label svg,
div[data-testid="stRadio"] [role="radiogroup"] label span:first-child:not(:last-child) {
  display: none !important;
  opacity: 0 !important;
  visibility: hidden !important;
  width: 0 !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* Flex distribution for Buttons, Pills & Radios */
div[data-testid="stButtonGroup"],
div[data-testid="stRadio"] > div {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: wrap !important;
  gap: 12px !important;
  width: 100% !important;
  align-items: center !important;
}

/* Base High-Contrast Navigation Pill / Tab */
div[data-testid="stButtonGroup"] button,
div[data-testid="stRadio"] label {
  background: #131f36 !important;
  border: 1.5px solid #2a3d60 !important;
  border-radius: 12px !important;
  padding: 12px 24px !important;
  color: #f1f5f9 !important;
  font-size: 1.15rem !important;
  font-weight: 750 !important;
  letter-spacing: -0.2px !important;
  cursor: pointer !important;
  transition: all 0.18s ease-in-out !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-height: 48px !important;
}

div[data-testid="stButtonGroup"] button p,
div[data-testid="stButtonGroup"] button span,
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span {
  font-size: 1.15rem !important;
  font-weight: 750 !important;
  color: #f1f5f9 !important;
  margin: 0 !important;
  line-height: 1.3 !important;
}

/* Hover State - Vibrant Sky Blue Glow */
div[data-testid="stButtonGroup"] button:hover,
div[data-testid="stRadio"] label:hover {
  background: #1c2b4a !important;
  border-color: #38bdf8 !important;
  color: #ffffff !important;
  box-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
  transform: translateY(-1px) !important;
}

/* Active State - Glowing Neon Emerald Pill (Matches Reference Image) */
div[data-testid="stButtonGroup"] button[aria-pressed="true"],
div[data-testid="stButtonGroup"] button[data-state="on"],
div[data-testid="stButtonGroup"] button[data-checked="true"],
div[data-testid="stRadio"] label:has(input:checked) {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.35) 0%, rgba(5, 150, 105, 0.25) 100%) !important;
  border: 2px solid #10b981 !important;
  box-shadow: 0 0 22px rgba(16, 185, 129, 0.45), inset 0 0 12px rgba(16, 185, 129, 0.2) !important;
  transform: translateY(-1px) !important;
}

div[data-testid="stButtonGroup"] button[aria-pressed="true"] p,
div[data-testid="stButtonGroup"] button[aria-pressed="true"] span,
div[data-testid="stRadio"] label:has(input:checked) p,
div[data-testid="stRadio"] label:has(input:checked) span {
  color: #34d399 !important;
  font-weight: 850 !important;
  text-shadow: 0 0 12px rgba(52, 211, 153, 0.6) !important;
}

/* High Visibility Headings */
h1, h2, h3, h4, h5 {
  color: #ffffff !important;
  font-weight: 800 !important;
  letter-spacing: -0.3px !important;
}
h2 { font-size: 1.45rem !important; margin: 1.2rem 0 0.6rem 0 !important; }
h3 { font-size: 1.25rem !important; margin: 1.1rem 0 0.5rem 0 !important; }
h5 { font-size: 1.1rem !important; color: #f1f5f9 !important; margin-bottom: 0.5rem !important; }

/* Node Health Cards (Matches Reference Photo 1:1) */
.node-card {
  border-radius: 14px;
  padding: 22px 26px;
  background: #0f1728;
  position: relative;
  margin-bottom: 20px;
  box-sizing: border-box;
}
.card-healthy {
  border: 1px solid #10b981;
  box-shadow: 0 0 18px rgba(16, 185, 129, 0.14);
}
.card-warning {
  border: 1px solid #f59e0b;
  box-shadow: 0 0 18px rgba(245, 158, 11, 0.14);
}
.card-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}
.node-name {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 750;
  margin: 0;
}
.node-client {
  color: #64748b;
  font-size: 0.82rem;
  margin-top: 3px;
}
.status-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.badge-healthy {
  background: rgba(16, 185, 129, 0.18);
  color: #34d399;
  border: 1px solid #059669;
}
.badge-warning {
  background: rgba(245, 158, 11, 0.18);
  color: #fbbf24;
  border: 1px solid #d97706;
}
.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 5px 0;
}
.stat-label { color: #94a3b8; font-size: 0.92rem; }
.stat-val-green { color: #34d399; font-weight: 750; font-size: 1.38rem; }
.stat-val-amber { color: #fbbf24; font-weight: 750; font-size: 1.38rem; }
.stat-val-white { color: #f1f5f9; font-weight: 600; font-size: 0.98rem; }

/* High-Impact Page Headings */
.view-title {
  color: #ffffff !important;
  font-size: 1.65rem !important;
  font-weight: 850 !important;
  margin: 6px 0 4px 0 !important;
  letter-spacing: -0.4px !important;
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
}
.view-subtitle {
  color: #94a3b8 !important;
  font-size: 0.98rem !important;
  font-weight: 500 !important;
  margin-bottom: 22px !important;
  line-height: 1.45 !important;
}

/* Metric Tiles with Elevated Contrast */
.top-brand-bar {
  background: radial-gradient(ellipse at 10% 0%, rgba(16,185,129,0.10), transparent 52%), #0f172a !important;
  border: 1px solid rgba(71, 85, 105, 0.58) !important;
}
.nav-card-container {
  background: linear-gradient(145deg, rgba(17,29,50,0.98), rgba(9,16,30,0.98)) !important;
}
.metric-tile {
  background: linear-gradient(145deg, #111d32, #0c1425) !important;
  border: 1px solid #2a3d60 !important;
  transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}
.metric-tile:hover {
  transform: translateY(-2px);
  border-color: rgba(45, 212, 191, 0.65) !important;
  box-shadow: 0 10px 28px rgba(0,0,0,0.24) !important;
}
.metric-tile {
  background: #0f182c !important;
  border: 1.5px solid #233554 !important;
  border-radius: 14px !important;
  padding: 18px 22px !important;
  margin-bottom: 18px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.28) !important;
}
.metric-tile-label {
  color: #94a3b8 !important;
  font-size: 0.82rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.6px !important;
  text-transform: uppercase !important;
}
.metric-tile-value {
  color: #ffffff !important;
  font-size: 1.85rem !important;
  font-weight: 850 !important;
  margin-top: 4px !important;
}
.metric-tile-sub {
  color: #34d399 !important;
  font-size: 0.85rem !important;
  font-weight: 650 !important;
  margin-top: 2px !important;
}

div[data-testid="stDataFrame"] {
  border: 1px solid #1e293b;
  border-radius: 10px;
  width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
# ---------- LIVE CONNECTION GATE & DATA LOAD ----------
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from database.telemetry import get_database_health

demo_mode = os.getenv("EDUVAULT_DEMO_MODE", "false").lower() == "true"
db_health = get_database_health()

st.markdown("## Runtime connection status")
h1, h2, h3 = st.columns([1, 1, 1.2])
for col, name in [(h1, "PostgreSQL"), (h2, "MongoDB")]:
    item = db_health.get(name, {"connected": False, "error": "Health check unavailable"})
    with col:
        if item.get("connected"):
            col.success(f"● {name} connected")
            if name == "PostgreSQL":
                col.caption(f"Database: {item.get('database')} · Role: {'replica' if item.get('is_replica') else 'primary/standalone'}")
            else:
                col.caption(f"Database: {item.get('database')} · Ping: {item.get('latency_ms')} ms")
        else:
            col.error(f"● {name} disconnected")
            col.caption(str(item.get("error", "Connection unavailable"))[:180])
with h3:
    if all(db_health.get(n, {}).get("connected") for n in ("PostgreSQL", "MongoDB")):
        st.success("LIVE DATA MODE")
        st.caption("Metrics below are read from configured database servers.")
    elif demo_mode:
        st.warning("DEMO MODE ENABLED")
        st.caption("Synthetic fallback records may be displayed. Not production telemetry.")
    else:
        st.error("LIVE MODE BLOCKED")
        st.caption("Configure both database connections. No sample data is silently substituted.")

if not all(db_health.get(n, {}).get("connected") for n in ("PostgreSQL", "MongoDB")) and not demo_mode:
    st.info("Set PostgreSQL and MongoDB connection values in .env, then restart Streamlit. Set EDUVAULT_DEMO_MODE=true only when you intentionally want sample data.")
    st.stop()

from analytics.student_analysis import get_student_performance, get_student_summary
from analytics.course_analysis import get_course_outcomes
from analytics.activity_analysis import get_activity_data

try:
    summary_df = get_student_summary()
    perf_df = get_student_performance()
    courses_df = get_course_outcomes()
    activities_df = get_activity_data()
except Exception as data_error:
    st.error(f"Live analytics could not be loaded: {data_error}")
    st.stop()

for col in ["marks", "grade_point"]:
    if col in perf_df.columns:
        perf_df[col] = pd.to_numeric(perf_df[col], errors="coerce")
for col in ["average_marks", "students_enrolled", "highest_marks", "lowest_marks"]:
    if col in courses_df.columns:
        courses_df[col] = pd.to_numeric(courses_df[col], errors="coerce")

# ---------- TOP BRANDING BAR ----------
active_students = int(summary_df["student_id"].nunique()) if "student_id" in summary_df.columns else len(summary_df)
all_live = all(db_health.get(n, {}).get("connected") for n in ("PostgreSQL", "MongoDB"))
status_text = "LIVE DATABASES" if all_live else ("DEMO DATA" if demo_mode else "OFFLINE")
status_color = "#10b981" if all_live else ("#f59e0b" if demo_mode else "#ef4444")
st.markdown(f"""
<div class="top-brand-bar">
  <div class="brand-left">
    <div class="brand-logo-sq">🎓</div>
    <div>
      <div class="brand-title-text">EduVault <span style="color:#34d399;">/</span> DataVault</div>
      <div style="color:#94a3b8; font-size:0.86rem;">Academic Intelligence · Query Observatory · Database Reliability</div>
    </div>
  </div>
  <div class="brand-badge-pill" style="border-color:{status_color}; color:{status_color}; background:{status_color}20;">
    <span style="width:9px;height:9px;border-radius:50%;background:{status_color};box-shadow:0 0 12px {status_color};display:inline-block;"></span>
    <span>{status_text} &nbsp;·&nbsp; <b>{active_students:,} students loaded</b></span>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- TOP NAVIGATION COMMAND DECK (ZERO GAPS, HIGH-VISIBILITY THEME) ----------
st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)

# 1. SECTION SWITCHER
st.markdown('<div class="nav-section-title">PLATFORM ENGINE</div>', unsafe_allow_html=True)
section_choices = ["🎓 Academic Intelligence", "🗄️ Database Operations"]
if "selected_platform_section" not in st.session_state:
    st.session_state.selected_platform_section = section_choices[0]

picked_section = st.pills(
    "Platform Section",
    options=section_choices,
    default=st.session_state.selected_platform_section,
    selection_mode="single",
    label_visibility="collapsed",
    key="pill_platform_section"
)
if picked_section:
    st.session_state.selected_platform_section = picked_section
selected_category = st.session_state.selected_platform_section

st.markdown('<div class="nav-inner-divider"></div>', unsafe_allow_html=True)

# 2. TOPIC SWITCHER (SEAMLESSLY FILLS FULL WIDTH, ZERO VOID)
st.markdown('<div class="nav-section-title">ACTIVE WORKSPACE & TOPICS</div>', unsafe_allow_html=True)
if selected_category == "🎓 Academic Intelligence":
    academic_topics = [
        "📊 Overview",
        "📈 Student Performance",
        "📚 Course Outcomes",
        "⏱️ Learning Activity",
        "🔍 Student Explorer"
    ]
    if "selected_academic_topic" not in st.session_state or st.session_state.selected_academic_topic not in academic_topics:
        st.session_state.selected_academic_topic = academic_topics[0]

    picked_topic = st.pills(
        "Academic Topics",
        options=academic_topics,
        default=st.session_state.selected_academic_topic,
        selection_mode="single",
        label_visibility="collapsed",
        key="pill_academic_topics"
    )
    if picked_topic:
        st.session_state.selected_academic_topic = picked_topic
    nav_topic = st.session_state.selected_academic_topic
else:
    db_topics = [
        "⚡ Slow Queries",
        "⏱ Replication Health",
        "📦 Shard Balance",
        "💡 Index Advisor"
    ]
    if "selected_db_topic" not in st.session_state or st.session_state.selected_db_topic not in db_topics:
        st.session_state.selected_db_topic = db_topics[0]

    picked_topic = st.pills(
        "Database Topics",
        options=db_topics,
        default=st.session_state.selected_db_topic,
        selection_mode="single",
        label_visibility="collapsed",
        key="pill_db_topics"
    )
    if picked_topic:
        st.session_state.selected_db_topic = picked_topic
    nav_topic = st.session_state.selected_db_topic

st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# SECTION 1: ACADEMIC INTELLIGENCE (250+ STUDENTS DATA & VISUALIZATIONS)
# ==============================================================================

# --- 1. OVERVIEW ---
if nav_topic == "📊 Overview":
    st.markdown("""
    <div class="view-title">Academic Records & Cohort Overview</div>
    <div class="view-subtitle">Consolidated view of student cohort performance, course enrollments, and digital learning activity.</div>
    """, unsafe_allow_html=True)

    total_students = int(summary_df["student_id"].nunique()) if "student_id" in summary_df else len(summary_df)
    total_courses = int(courses_df["course_id"].nunique()) if "course_id" in courses_df else len(courses_df)
    total_records = len(perf_df)
    mean_marks = float(perf_df["marks"].mean()) if not perf_df.empty and "marks" in perf_df else 0.0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="metric-tile">
          <div class="metric-tile-label">TOTAL STUDENTS</div>
          <div class="metric-tile-value">{total_students:,}</div>
          <div class="metric-tile-sub">Enrolled active cohort</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-tile">
          <div class="metric-tile-label">OFFERED COURSES</div>
          <div class="metric-tile-value">{total_courses:,}</div>
          <div class="metric-tile-sub">Curriculum subjects</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="metric-tile">
          <div class="metric-tile-label">COURSE-GRADE RECORDS</div>
          <div class="metric-tile-value">{total_records:,}</div>
          <div class="metric-tile-sub">Graded enrollments</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="metric-tile">
          <div class="metric-tile-label">AVERAGE COHORT MARKS</div>
          <div class="metric-tile-value" style="color:#34d399;">{mean_marks:.1f}/100</div>
          <div class="metric-tile-sub">Overall grade point</div>
        </div>
        """, unsafe_allow_html=True)

    col_chart_l, col_chart_r = st.columns(2)
    with col_chart_l:
        st.markdown("##### Top 15 High-Achieving Students")
        if not summary_df.empty and "average_marks" in summary_df.columns:
            top_15 = summary_df.dropna(subset=["average_marks"]).nlargest(15, "average_marks")
            chart_top = alt.Chart(top_15).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#2dd4bf").encode(
                x=alt.X("student_name:N", title="Student Name", sort="-y", axis=alt.Axis(labelAngle=-45, labelColor="#94a3b8")),
                y=alt.Y("average_marks:Q", title="Average Marks", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
                tooltip=["roll_number", "student_name", "average_marks", "department_name"]
            ).properties(height=280, background="transparent")
            st.altair_chart(chart_top, use_container_width=True)

    with col_chart_r:
        st.markdown("##### Course Average Marks")
        if not courses_df.empty and "average_marks" in courses_df.columns:
            chart_c = alt.Chart(courses_df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, color="#818cf8").encode(
                y=alt.Y("course_name:N", title="Course", sort="-x", axis=alt.Axis(labelColor="#94a3b8")),
                x=alt.X("average_marks:Q", title="Average Marks", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
                tooltip=["course_code", "course_name", "students_enrolled", "average_marks"]
            ).properties(height=280, background="transparent")
            st.altair_chart(chart_c, use_container_width=True)

    st.markdown("##### Master Enrollment & Academic Grades (250 Students)")
    st.dataframe(perf_df, use_container_width=True, hide_index=True)


# --- 2. STUDENT PERFORMANCE ---
elif nav_topic == "📈 Student Performance":
    st.markdown("""
    <div class="view-title">Student Performance Analytics</div>
    <div class="view-subtitle">Inspect student grade distributions, average marks, and filter by academic department.</div>
    """, unsafe_allow_html=True)

    depts = ["All Departments"] + sorted(summary_df["department_name"].dropna().astype(str).unique().tolist())
    sel_dept = st.selectbox("Select Academic Department", depts)

    f_summary = summary_df.copy()
    f_perf = perf_df.copy()
    if sel_dept != "All Departments":
        f_summary = f_summary[f_summary["department_name"] == sel_dept]
        f_perf = f_perf[f_perf["department_name"] == sel_dept]

    p1, p2, p3 = st.columns(3)
    p1.metric("Students in Department", f"{f_summary['student_id'].nunique():,}")
    p2.metric("Graded Records", f"{len(f_perf):,}")
    p3.metric("Department Mean Marks", f"{f_perf['marks'].mean():.1f}/100" if not f_perf.empty else "N/A")

    if not f_summary.empty and "average_marks" in f_summary.columns:
        st.markdown("##### Grade Distribution Histogram")
        hist = alt.Chart(f_summary).mark_bar(color="#818cf8", opacity=0.85).encode(
            x=alt.X("average_marks:Q", bin=alt.Bin(maxbins=15), title="Average Marks Range", axis=alt.Axis(labelColor="#94a3b8")),
            y=alt.Y("count()", title="Student Count", axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
            tooltip=["count()"]
        ).properties(height=250, background="transparent")
        st.altair_chart(hist, use_container_width=True)

    st.dataframe(f_summary, use_container_width=True, hide_index=True)
    st.download_button(
        "📥 Download Student Performance CSV",
        f_summary.to_csv(index=False).encode("utf-8"),
        "eduvault_student_performance.csv",
        "text/csv"
    )


# --- 3. COURSE OUTCOMES ---
elif nav_topic == "📚 Course Outcomes":
    st.markdown("""
    <div class="view-title">Course Outcomes & Curriculum Evaluation</div>
    <div class="view-subtitle">Enrollment volume, average marks, highest, and lowest grade outcomes across courses.</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Active Courses", f"{len(courses_df):,}")
    c2.metric("Total Enrollments", f"{int(courses_df['students_enrolled'].fillna(0).sum()):,}")
    c3.metric("Mean Course Grade", f"{courses_df['average_marks'].mean():.1f}/100" if "average_marks" in courses_df else "N/A")

    if not courses_df.empty:
        st.markdown("##### Course Enrollment Volume vs Mean Marks")
        c_chart = alt.Chart(courses_df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
            x=alt.X("course_code:N", title="Course Code", axis=alt.Axis(labelColor="#94a3b8")),
            y=alt.Y("average_marks:Q", title="Average Marks", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
            color=alt.Color("students_enrolled:Q", scale=alt.Scale(range=["#38bdf8", "#818cf8", "#c084fc"]), title="Enrollments"),
            tooltip=["course_code", "course_name", "students_enrolled", "average_marks", "highest_marks", "lowest_marks"]
        ).properties(height=280, background="transparent")
        st.altair_chart(c_chart, use_container_width=True)

    st.dataframe(courses_df, use_container_width=True, hide_index=True)


# --- 4. LEARNING ACTIVITY ---
elif nav_topic == "⏱️ Learning Activity":
    st.markdown("""
    <div class="view-title">Student Digital Learning Activity (MongoDB)</div>
    <div class="view-subtitle">Behavioral event telemetry, video watch duration, quiz attempts, and course completion rates.</div>
    """, unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    a1.metric("Total Activity Events", f"{len(activities_df):,}")
    a2.metric("Total Learning Duration", f"{int(activities_df['duration_minutes'].fillna(0).sum()):,} min" if "duration_minutes" in activities_df else "0 min")
    a3.metric("Mean Completion Rate", f"{activities_df['completion_percentage'].mean():.1f}%" if "completion_percentage" in activities_df else "N/A")

    if not activities_df.empty and "activity_type" in activities_df.columns:
        counts = activities_df["activity_type"].value_counts().reset_index()
        counts.columns = ["activity_type", "events"]

        act_chart = alt.Chart(counts).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, color="#2dd4bf").encode(
            y=alt.Y("activity_type:N", title="Activity Type", sort="-x", axis=alt.Axis(labelColor="#94a3b8")),
            x=alt.X("events:Q", title="Event Count", axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
            tooltip=["activity_type", "events"]
        ).properties(height=230, background="transparent")
        st.altair_chart(act_chart, use_container_width=True)

    st.dataframe(activities_df, use_container_width=True, hide_index=True)


# --- 5. STUDENT EXPLORER ---
elif nav_topic == "🔍 Student Explorer":
    st.markdown("""
    <div class="view-title">Individual Student Record Explorer</div>
    <div class="view-subtitle">Search and inspect an individual student's complete academic transcript, course marks, and digital engagement.</div>
    """, unsafe_allow_html=True)

    if summary_df.empty:
        st.info("No student records were returned by the live database.")
        st.stop()

    options = summary_df[["student_id", "roll_number", "student_name", "department_name"]].copy()
    options["display"] = options["student_name"] + " (" + options["roll_number"] + ") — " + options["department_name"]
    sel_display = st.selectbox("Select or Search Student", options["display"].tolist())
    
    chosen = options[options["display"] == sel_display].iloc[0]
    sid = chosen["student_id"]
    student_row = summary_df[summary_df["student_id"] == sid].iloc[0]
    st_courses = perf_df[perf_df["student_id"] == sid]
    st_acts = activities_df[activities_df["student_id"] == sid]

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Roll Number", str(student_row["roll_number"]))
    e2.metric("Department", str(student_row["department_name"]))
    e3.metric("Average Marks", f"{st_courses['marks'].mean():.1f}/100" if not st_courses.empty else "N/A")
    e4.metric("Activity Logs", f"{len(st_acts):,} events")

    if not st_courses.empty:
        st.markdown(f"##### Course Marks for {chosen['student_name']}")
        bar_st = alt.Chart(st_courses).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#818cf8").encode(
            x=alt.X("course_code:N", title="Course Code", axis=alt.Axis(labelColor="#94a3b8")),
            y=alt.Y("marks:Q", title="Marks Obtained", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
            tooltip=["course_code", "course_name", "marks", "grade"]
        ).properties(height=240, background="transparent")
        st.altair_chart(bar_st, use_container_width=True)

        st.markdown("##### Academic Transcript")
        st.dataframe(st_courses, use_container_width=True, hide_index=True)


# ==============================================================================
# SECTION 2: DATABASE OPERATIONS (4 TOPICS FROM REFERENCE PHOTO)
# ==============================================================================

# --- 6. SLOW QUERIES ---
elif nav_topic == "⚡ Slow Queries":
    st.markdown("""
    <div class="view-title">Live Query Performance Center</div>
    <div class="view-subtitle">Measured application query latency, PostgreSQL workload statistics, and real query plans. No estimated benchmark values are shown.</div>
    """, unsafe_allow_html=True)

    from database.postgres_db import get_query_metrics, get_slow_queries, explain_query
    from database.mongo_db import get_mongo_metrics

    if st.button("↻ Refresh live telemetry"):
        st.rerun()

    local_metrics = get_query_metrics()
    mongo_metrics = pd.DataFrame(get_mongo_metrics())
    total_calls = len(local_metrics)
    slow_count = int((local_metrics["elapsed_ms"] >= 100).sum()) if total_calls else 0
    avg_ms = float(local_metrics["elapsed_ms"].mean()) if total_calls else 0.0
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Measured app queries", f"{total_calls:,}")
    q2.metric("Queries ≥ 100 ms", f"{slow_count:,}")
    q3.metric("Mean client latency", f"{avg_ms:.2f} ms" if total_calls else "No samples yet")
    q4.metric("Mongo operations measured", f"{len(mongo_metrics):,}")

    st.markdown("### Application query samples")
    if local_metrics.empty:
        st.info("No query samples have been collected in this Streamlit process yet.")
    else:
        st.dataframe(local_metrics.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)

    st.markdown("### PostgreSQL server workload (pg_stat_statements)")
    try:
        server_slow = get_slow_queries(50)
        if server_slow.empty:
            st.info("pg_stat_statements returned no statements.")
        else:
            st.dataframe(server_slow, use_container_width=True, hide_index=True)
    except Exception as exc:
        st.warning(f"Server-level query history is unavailable: {exc}")
        st.caption("A database administrator must enable pg_stat_statements in shared_preload_libraries, restart PostgreSQL, and run CREATE EXTENSION pg_stat_statements in this database.")

    st.markdown("### Explain a real query")
    sql_text = st.text_area(
        "SELECT query (read-only only)",
        value="SELECT s.student_id, s.student_name, g.marks FROM students s JOIN enrollments e ON e.student_id = s.student_id JOIN grades g ON g.enrollment_id = e.enrollment_id WHERE s.student_id = 16;",
        height=130,
        help="Only SELECT/WITH statements are accepted. Use parameters in application code for user-supplied values."
    )
    analyze = st.checkbox("Run EXPLAIN ANALYZE (executes this SELECT; use only safe, bounded queries)", value=False)
    if st.button("Inspect actual query plan", type="primary"):
        try:
            plan = explain_query(sql_text, analyze=analyze)
            st.success("Query plan retrieved from the connected PostgreSQL server.")
            st.json(plan)
        except Exception as exc:
            st.error(f"Could not explain query: {exc}")

    st.markdown("### MongoDB operation timings")
    if mongo_metrics.empty:
        st.info("No MongoDB operations have been measured in this process yet.")
    else:
        st.dataframe(mongo_metrics, use_container_width=True, hide_index=True)

    with st.expander("Inspect a MongoDB query with executionStats"):
        import json
        collection_name = st.selectbox("Collection", ["activity_logs", "learning_content"])
        filter_text = st.text_area("MongoDB filter (JSON)", value='{"student_id": 16}', height=90)
        if st.button("Explain MongoDB find"):
            try:
                filter_doc = json.loads(filter_text)
                if not isinstance(filter_doc, dict):
                    raise ValueError("Filter must be a JSON object.")
                from database.mongo_db import explain_find
                explain_result = explain_find(collection_name, filter_doc, limit=500)
                st.success("MongoDB execution statistics received from the live server.")
                st.json(explain_result)
            except Exception as exc:
                st.error(f"MongoDB explain failed: {exc}")


# --- 7. REPLICATION HEALTH ---
elif nav_topic == "⏱ Replication Health":
    st.markdown("""
    <div class="view-title">Live Replication Monitor</div>
    <div class="view-subtitle">Reads PostgreSQL replication views from the connected server. Empty results are reported as no connected standby, never as a healthy replica.</div>
    """, unsafe_allow_html=True)

    from database.postgres_db import postgres_health, get_replication_status, get_wal_receiver_status
    if st.button("↻ Refresh replication status"):
        st.rerun()

    try:
        health = postgres_health()
        if health.get("is_replica"):
            st.info("This PostgreSQL server reports that it is operating as a standby.")
            receiver = get_wal_receiver_status()
            if receiver.empty:
                st.warning("No active WAL receiver row was returned.")
            else:
                st.success("WAL receiver is reporting live streaming state.")
                st.dataframe(receiver, use_container_width=True, hide_index=True)
        else:
            st.info(f"Connected to database: {health.get('database')} · This server is not in recovery.")
            replicas = get_replication_status()
            if replicas.empty:
                st.warning("No standby connections are currently reported by pg_stat_replication.")
                st.caption("Configure physical or logical replication before expecting replica telemetry.")
            else:
                st.success(f"{len(replicas)} standby connection(s) currently reported.")
                st.dataframe(replicas, use_container_width=True, hide_index=True)
    except Exception as exc:
        st.error(f"Could not read live replication status: {exc}")

    st.markdown("### What this screen measures")
    st.write("Primary-side streaming state, client address, synchronous state, WAL positions, and reported write/flush/replay lag. These values exist only when the database is configured for replication.")


# --- 8. SHARD BALANCE ---
elif nav_topic == "📦 Shard Balance":
    st.markdown("""
    <div class="view-title">Live Partition & Shard Topology</div>
    <div class="view-subtitle">Inspects PostgreSQL declarative partitions and the connected MongoDB topology. No placeholder shard counts or simulated rebalancing actions.</div>
    """, unsafe_allow_html=True)

    from database.postgres_db import get_partition_status
    from database.mongo_db import mongo_cluster_status

    st.markdown("### PostgreSQL table partitioning")
    try:
        partitions = get_partition_status()
        if partitions.empty:
            st.info("No declaratively partitioned PostgreSQL tables were found in the visible schemas.")
        else:
            st.dataframe(partitions, use_container_width=True, hide_index=True)
    except Exception as exc:
        st.warning(f"Partition metadata unavailable: {exc}")

    st.markdown("### MongoDB topology")
    try:
        topology = mongo_cluster_status()
        st.json(topology)
        if topology.get("topology") == "mongos":
            st.success(f"MongoDB mongos reports {len(topology.get('shards', []))} shard(s).")
        elif topology.get("topology") == "replica set":
            st.info("MongoDB replica set detected. Replica sets provide replication, not automatic proof of sharding.")
        else:
            st.warning("Standalone MongoDB detected; sharding is not configured on this connection.")
    except Exception as exc:
        st.error(f"Could not inspect MongoDB topology: {exc}")

    st.caption("EduVault reports topology only. It does not trigger production shard migration or rebalancing from the dashboard.");


# --- 9. INDEX ADVISOR ---
elif nav_topic == "💡 Index Advisor":
    st.markdown("""
    <div class="view-title">Live Index Advisor</div>
    <div class="view-subtitle">Uses actual PostgreSQL sequential-scan counters, catalog indexes, and schema metadata. Index creation requires explicit review and confirmation.</div>
    """, unsafe_allow_html=True)

    from database.postgres_db import get_table_index_stats, list_indexes, get_table_columns, create_index_concurrently

    if st.button("↻ Refresh index statistics"):
        st.rerun()

    try:
        stats = get_table_index_stats(100)
        indexes = list_indexes()
        st.markdown("### Table scan statistics")
        if stats.empty:
            st.info("No user-table statistics are currently available.")
        else:
            st.dataframe(stats, use_container_width=True, hide_index=True)
        st.markdown("### Existing indexes")
        if indexes.empty:
            st.info("No visible indexes were returned.")
        else:
            st.dataframe(indexes, use_container_width=True, hide_index=True)

        if not stats.empty:
            st.markdown("### Create a reviewed B-tree index")
            table_choices = sorted(stats["table_name"].dropna().astype(str).unique().tolist())
            table_name = st.selectbox("Table", table_choices)
            available_columns = get_table_columns(table_name)
            selected_columns = st.multiselect("Index columns (order matters)", available_columns)
            default_idx = "idx_" + table_name[:35] + "_" + "_".join(selected_columns[:2])[:35] if selected_columns else ""
            index_name = st.text_input("Index name", value=default_idx)
            confirm = st.checkbox("I reviewed the table size and write overhead; create this index concurrently.")
            if st.button("Create index concurrently", type="primary", disabled=not (selected_columns and index_name and confirm)):
                try:
                    create_index_concurrently(index_name, table_name, selected_columns)
                    st.success(f"Index {index_name} was created or already existed.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Index creation failed: {exc}")
    except Exception as exc:
        st.error(f"Index catalog inspection failed: {exc}")

    st.markdown("### MongoDB activity collection indexes")
    try:
        from database.mongo_db import get_mongo_database, explain_find, timed_create_index
        activity_collection = get_mongo_database()["activity_logs"]
        st.json(activity_collection.index_information())
        filter_doc = {"student_id": 16, "activity_type": "Video Watched"}
        if st.button("Inspect MongoDB activity query plan"):
            st.json(explain_find("activity_logs", filter_doc, limit=100))
        mongo_confirm = st.checkbox("I reviewed the MongoDB workload and want to create the student/activity compound index.")
        if st.button("Create MongoDB compound index", disabled=not mongo_confirm):
            index_name = timed_create_index(
                "activity_logs", [("student_id", 1), ("activity_type", 1)],
                name="idx_activity_student_type",
            )
            st.success(f"MongoDB index available: {index_name}")
    except Exception as exc:
        st.warning(f"MongoDB index inspection is unavailable: {exc}")


