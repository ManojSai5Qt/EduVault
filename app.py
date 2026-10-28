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
if "applied_indexes" not in st.session_state:
    st.session_state.applied_indexes = set()
if "query_optimized" not in st.session_state:
    st.session_state.query_optimized = False
if "shards_balanced" not in st.session_state:
    st.session_state.shards_balanced = False

# Load 250+ Students & Academic Records
from analytics.student_analysis import get_student_performance, get_student_summary
from analytics.course_analysis import get_course_outcomes
from analytics.activity_analysis import get_activity_data

summary_df = get_student_summary()
perf_df = get_student_performance()
courses_df = get_course_outcomes()
activities_df = get_activity_data()

for col in ["marks", "grade_point"]:
    if col in perf_df.columns:
        perf_df[col] = pd.to_numeric(perf_df[col], errors="coerce")
for col in ["average_marks", "students_enrolled", "highest_marks", "lowest_marks"]:
    if col in courses_df.columns:
        courses_df[col] = pd.to_numeric(courses_df[col], errors="coerce")

# ---------- TOP BRANDING BAR ----------
st.markdown("""
<div class="top-brand-bar">
  <div class="brand-left">
    <div class="brand-logo-sq">🎓</div>
    <div>
      <div class="brand-title-text">EduVault & DataVault Platform</div>
      <div style="color:#64748b; font-size:0.82rem;">Academic Intelligence • Query Optimization • High Availability Replication • Sharding</div>
    </div>
  </div>
  <div class="brand-badge-pill">
    <div class="dot-green"></div>
    <span>Active Cohort: <b>250 Students</b> • Cluster: <b>Healthy</b></span>
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
    <div class="view-title">Slow Query Analyzer & Optimization Engine</div>
    <div class="view-subtitle">Profile expensive queries, inspect EXPLAIN ANALYZE execution plans, and eliminate sequential table scans.</div>
    """, unsafe_allow_html=True)

    sq1, sq2, sq3 = st.columns(3)
    with sq1:
        st.markdown("""
        <div class="metric-tile">
          <div class="metric-tile-label">QUERIES PROFILED</div>
          <div class="metric-tile-value">1,842</div>
          <div class="metric-tile-sub">Active database sessions</div>
        </div>
        """, unsafe_allow_html=True)
    with sq2:
        st.markdown("""
        <div class="metric-tile">
          <div class="metric-tile-label">SLOW QUERIES (>100ms)</div>
          <div class="metric-tile-value" style="color:#fbbf24;">14 Queries</div>
          <div class="metric-tile-sub" style="color:#fbbf24;">Requires index optimization</div>
        </div>
        """, unsafe_allow_html=True)
    with sq3:
        st.markdown("""
        <div class="metric-tile">
          <div class="metric-tile-label">OPTIMIZATION POTENTIAL</div>
          <div class="metric-tile-value" style="color:#34d399;">99.7% Latency Drop</div>
          <div class="metric-tile-sub">From 342ms down to 0.82ms</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("##### Detected Query Bottlenecks (`pg_stat_statements`)")
    slow_queries_data = [
        {"Query ID": "Q-8821", "Table": "activity_logs", "SQL Query": "SELECT * FROM activity_logs WHERE student_id = 42 AND activity_type = 'Video Watched';", "Calls": 1840, "Latency": "342.5 ms", "Scan Plan": "Seq Scan (100k rows filtered)", "Severity": "⚠️ Critical"},
        {"Query ID": "Q-4912", "Table": "grades JOIN students", "SQL Query": "SELECT s.name, g.marks FROM students s JOIN grades g ON s.id = g.student_id WHERE g.marks > 90;", "Calls": 320, "Latency": "185.0 ms", "Scan Plan": "Hash Join + Seq Scan", "Severity": "⚠️ High"},
        {"Query ID": "Q-1049", "Table": "courses", "SQL Query": "SELECT course_code, AVG(marks) FROM grades GROUP BY course_code;", "Calls": 120, "Latency": "132.0 ms", "Scan Plan": "HashAggregate", "Severity": "ℹ️ Medium"}
    ]
    st.dataframe(pd.DataFrame(slow_queries_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("##### 🔬 Interactive Query Optimization Lab (EXPLAIN ANALYZE)")
    oc1, oc2 = st.columns([3.2, 1.3])
    with oc1:
        st.selectbox("Target SQL Query", ["Q-8821: SELECT * FROM activity_logs WHERE student_id = 42 AND activity_type = 'Video Watched'"])
    with oc2:
        st.write("")
        st.write("")
        if st.button("🚀 Optimize with Composite Index", type="primary", use_container_width=True):
            st.session_state.query_optimized = True

    if st.session_state.query_optimized:
        col_b, col_a = st.columns(2)
        with col_b:
            st.markdown("""
            <div class="node-card card-warning">
              <div class="card-header-flex">
                <div class="node-name">Before Optimization</div>
                <div class="status-badge badge-warning">SEQ SCAN</div>
              </div>
              <div class="stat-row"><span class="stat-label">Execution Time</span><span class="stat-val-amber">342.50 ms</span></div>
              <div class="stat-row"><span class="stat-label">Total Cost</span><span class="stat-val-white">2,845.00</span></div>
              <div class="stat-row"><span class="stat-label">Disk IO</span><span class="stat-val-white">read=1,890 blocks</span></div>
              <div class="stat-row"><span class="stat-label">Rows Scanned</span><span class="stat-val-white">100,000 rows</span></div>
            </div>
            """, unsafe_allow_html=True)
        with col_a:
            st.markdown("""
            <div class="node-card card-healthy">
              <div class="card-header-flex">
                <div class="node-name">After Index Optimization</div>
                <div class="status-badge badge-healthy">INDEX SCAN</div>
              </div>
              <div class="stat-row"><span class="stat-label">Execution Time</span><span class="stat-val-green">0.82 ms (99.7% Faster)</span></div>
              <div class="stat-row"><span class="stat-label">Total Cost</span><span class="stat-val-white">8.42</span></div>
              <div class="stat-row"><span class="stat-label">Disk IO</span><span class="stat-val-white">read=0 (Zero Disk Read)</span></div>
              <div class="stat-row"><span class="stat-label">Rows Scanned</span><span class="stat-val-white">12 matching rows</span></div>
            </div>
            """, unsafe_allow_html=True)


# --- 7. REPLICATION HEALTH (MATCHES PHOTO 100%) ---
elif nav_topic == "⏱ Replication Health":
    col_card1, col_card2 = st.columns(2)
    with col_card1:
        st.markdown("""
        <div class="node-card card-healthy">
          <div class="card-header-flex">
            <div>
              <div class="node-name">pg-replica1</div>
              <div class="node-client">Local client</div>
            </div>
            <div class="status-badge badge-healthy">HEALTHY</div>
          </div>
          <div class="stat-row"><span class="stat-label">Replication Lag</span><span class="stat-val-green">0.16s</span></div>
          <div class="stat-row"><span class="stat-label">Write Lag</span><span class="stat-val-white">0.13s</span></div>
          <div class="stat-row"><span class="stat-label">Standby State</span><span class="stat-val-white">Streaming</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col_card2:
        st.markdown("""
        <div class="node-card card-warning">
          <div class="card-header-flex">
            <div>
              <div class="node-name">pg-replica2</div>
              <div class="node-client">Local client</div>
            </div>
            <div class="status-badge badge-warning">WARNING</div>
          </div>
          <div class="stat-row"><span class="stat-label">Replication Lag</span><span class="stat-val-amber">11.13s</span></div>
          <div class="stat-row"><span class="stat-label">Write Lag</span><span class="stat-val-white">1.11s</span></div>
          <div class="stat-row"><span class="stat-label">Standby State</span><span class="stat-val-white">Streaming</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="view-title">Streaming Replication Lag Over Time</div>
    <div class="view-subtitle">Historical trends of standby node lag read from SQLite snapshots.</div>
    """, unsafe_allow_html=True)

    time_seq = list(range(1, 26))
    lag_rep1 = [round(0.16 + 0.06 * np.sin(i), 2) for i in time_seq]
    lag_rep2 = [11.5, 9.8, 4.2, 7.5, 3.8, 6.9, 3.2, 7.8, 2.5, 6.2, 8.0, 3.5, 8.5, 4.1, 7.6, 3.2, 4.8, 21.0, 19.5, 16.0, 17.8, 20.5, 14.2, 18.0, 21.2]

    chart_data = pd.DataFrame({
        "Sample": time_seq * 2,
        "Lag Seconds": lag_rep1 + lag_rep2,
        "Replica": ["pg-replica1"] * 25 + ["pg-replica2"] * 25
    })

    alt_chart = alt.Chart(chart_data).mark_line(interpolate="monotone", strokeWidth=2.4, point=alt.OverlayMarkDef(filled=True, size=28)).encode(
        x=alt.X("Sample:Q", title=None, axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
        y=alt.Y("Lag Seconds:Q", title="Lag Seconds", axis=alt.Axis(gridColor="#162035", labelColor="#94a3b8")),
        color=alt.Color("Replica:N", scale=alt.Scale(domain=["pg-replica1", "pg-replica2"], range=["#2dd4bf", "#10b981"]), legend=alt.Legend(orient="top-right", labelColor="#e2e8f0", title=None))
    ).properties(height=300, background="transparent").configure_view(strokeWidth=0)
    st.altair_chart(alt_chart, use_container_width=True)

    st.markdown("##### Standby Slot & WAL Synchronization Telemetry")
    pg_stat_data = [
        {"pid": 14201, "application_name": "pg-replica1", "client_addr": "10.0.1.25", "state": "streaming", "sync_state": "sync", "sent_lsn": "0/16B38D0", "write_lsn": "0/16B38D0", "flush_lsn": "0/16B38D0", "replay_lag": "00:00:00.160"},
        {"pid": 14208, "application_name": "pg-replica2", "client_addr": "10.0.2.80", "state": "streaming", "sync_state": "async", "sent_lsn": "0/16B38D0", "write_lsn": "0/16B3898", "flush_lsn": "0/16B3898", "replay_lag": "00:00:11.130"}
    ]
    st.dataframe(pd.DataFrame(pg_stat_data), use_container_width=True, hide_index=True)


# --- 8. SHARD BALANCE ---
elif nav_topic == "📦 Shard Balance":
    st.markdown("""
    <div class="view-title">Shard Distribution & Cluster Partitioning</div>
    <div class="view-subtitle">Horizontal distribution of data chunks across database storage nodes.</div>
    """, unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    balanced = st.session_state.shards_balanced
    with s1:
        st.markdown(f"""
        <div class="node-card card-healthy">
          <div class="card-header-flex"><div class="node-name">mongo-shard-1</div><div class="status-badge badge-healthy">BALANCED</div></div>
          <div class="stat-row"><span class="stat-label">Chunks</span><span class="stat-val-green">{"3,340" if balanced else "4,120"} ({"33.4%" if balanced else "41.2%"})</span></div>
          <div class="stat-row"><span class="stat-label">Storage Size</span><span class="stat-val-white">12.4 GB</span></div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="node-card card-healthy">
          <div class="card-header-flex"><div class="node-name">mongo-shard-2</div><div class="status-badge badge-healthy">BALANCED</div></div>
          <div class="stat-row"><span class="stat-label">Chunks</span><span class="stat-val-green">{"3,330" if balanced else "3,580"} ({"33.3%" if balanced else "35.8%"})</span></div>
          <div class="stat-row"><span class="stat-label">Storage Size</span><span class="stat-val-white">11.8 GB</span></div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="node-card {'card-healthy' if balanced else 'card-warning'}">
          <div class="card-header-flex"><div class="node-name">mongo-shard-3</div><div class="status-badge {'badge-healthy' if balanced else 'badge-warning'}">{"BALANCED" if balanced else "DRAINED"}</div></div>
          <div class="stat-row"><span class="stat-label">Chunks</span><span class="{'stat-val-green' if balanced else 'stat-val-amber'}">{"3,330" if balanced else "2,300"} ({"33.3%" if balanced else "23.0%"})</span></div>
          <div class="stat-row"><span class="stat-label">Storage Size</span><span class="stat-val-white">{"11.9 GB" if balanced else "7.6 GB"}</span></div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("⚖️ Trigger Cluster Auto-Rebalance", type="primary"):
        st.session_state.shards_balanced = True
        st.rerun()

    st.write("")
    st.markdown("##### Shard Query Router (Point Query vs Scatter-Gather)")
    q_mode = st.radio("Query Pattern", ["Point Query (Direct O(1) Route using Shard Key)", "Scatter-Gather Broadcast (Queries All Shards in Parallel)"], horizontal=True)
    if "Point" in q_mode:
        st.json({"SQL Query": "SELECT * FROM activity_logs WHERE student_id = 105;", "Execution Strategy": "Single-Shard Direct Route (O(1))", "Target Node Contacted": "mongo-shard-2 (hash(105) % 3 = 1)", "Network Round-Trips": 1, "Latency Overhead": "0.12 ms"})
    else:
        st.json({"SQL Query": "SELECT * FROM activity_logs WHERE duration_minutes > 45;", "Execution Strategy": "Scatter-Gather Parallel Broadcast", "Target Nodes Contacted": ["mongo-shard-1", "mongo-shard-2", "mongo-shard-3"], "Network Round-Trips": "3 parallel RPCs + Coordinator Merge", "Latency Overhead": "14.20 ms"})


# --- 9. INDEX ADVISOR ---
elif nav_topic == "💡 Index Advisor":
    st.markdown("""
    <div class="view-title">Automated Database Index Advisor</div>
    <div class="view-subtitle">Rule-based optimizer detecting high-cost sequential scans and generating optimal DDL indexes.</div>
    """, unsafe_allow_html=True)

    ia1, ia2, ia3 = st.columns(3)
    with ia1:
        st.markdown("""<div class="metric-tile"><div class="metric-tile-label">MISSING INDEXES DETECTED</div><div class="metric-tile-value" style="color:#fbbf24;">3 Indexes</div><div class="metric-tile-sub">High scan cost identified</div></div>""", unsafe_allow_html=True)
    with ia2:
        st.markdown("""<div class="metric-tile"><div class="metric-tile-label">POTENTIAL IO REDUCTION</div><div class="metric-tile-value" style="color:#34d399;">88.4%</div><div class="metric-tile-sub">Index Scan efficiency</div></div>""", unsafe_allow_html=True)
    with ia3:
        st.markdown("""<div class="metric-tile"><div class="metric-tile-label">BUFFER CACHE HIT RATIO</div><div class="metric-tile-value">96.2%</div><div class="metric-tile-sub">Memory hit efficiency</div></div>""", unsafe_allow_html=True)

    st.markdown("##### Index Recommendations & Creation")
    idx_list = [
        {"Table": "activity_logs", "Name": "idx_activity_student_type", "Columns": "student_id, activity_type", "Type": "B-Tree (Composite)", "Saving": "98.5%", "Reason": "Accelerates Q-8821 student activity filtering"},
        {"Table": "grades", "Name": "idx_grades_marks", "Columns": "marks", "Type": "B-Tree", "Saving": "74.0%", "Reason": "Optimizes high-achiever scholarship filtering"},
        {"Table": "courses", "Name": "idx_courses_name", "Columns": "course_name", "Type": "GIN (trgm)", "Saving": "85.2%", "Reason": "Speeds up course keyword searching"}
    ]

    for item in idx_list:
        is_created = item["Name"] in st.session_state.applied_indexes
        col_card, col_btn = st.columns([3.8, 1.2])
        with col_card:
            st.markdown(f"""
            <div style="background:#0f1728; border:1px solid {'#10b981' if is_created else '#1e293b'}; border-radius:10px; padding:15px 18px; margin-bottom:12px;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <b>Table: <code>{item['Table']}</code></b> &nbsp;|&nbsp; Index: <code>{item['Name']}</code> ({item['Type']})<br>
                  <span style="color:#94a3b8; font-size:0.87rem;">Columns: <code>{item['Columns']}</code> • Estimated Cost Savings: <b style="color:#34d399;">{item['Saving']}</b></span><br>
                  <span style="color:#64748b; font-size:0.82rem;">{item['Reason']}</span>
                </div>
                <div><span class="status-badge {'badge-healthy' if is_created else 'badge-warning'}">{'ACTIVE' if is_created else 'RECOMMENDED'}</span></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            st.write("")
            if is_created:
                st.button("✅ Created", key=f"created_{item['Name']}", disabled=True, use_container_width=True)
            else:
                if st.button("⚡ Create Index", key=f"create_{item['Name']}", type="primary", use_container_width=True):
                    st.session_state.applied_indexes.add(item["Name"])
                    st.rerun()
