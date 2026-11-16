import os
from database.sample_data import get_fallback_performance, get_fallback_summary

def _fallback_or_raise(factory, error):
    if os.getenv("EDUVAULT_DEMO_MODE", "false").lower() == "true":
        return factory()
    raise RuntimeError("PostgreSQL query failed. Check the live database connection; enable EDUVAULT_DEMO_MODE=true only for intentional demo data.") from error

def get_student_performance():
    from database.postgres_db import fetch_dataframe
    query = """
    SELECT s.student_id, s.roll_number, s.student_name, d.department_name,
           c.course_code, c.course_name, e.semester, g.marks, g.grade, g.grade_point
    FROM students s
    JOIN departments d ON s.department_id = d.department_id
    JOIN enrollments e ON s.student_id = e.student_id
    JOIN courses c ON e.course_id = c.course_id
    JOIN grades g ON e.enrollment_id = g.enrollment_id
    ORDER BY s.student_id, c.course_id;
    """
    try:
        return fetch_dataframe(query)
    except Exception as exc:
        return _fallback_or_raise(get_fallback_performance, exc)

def get_student_summary():
    from database.postgres_db import fetch_dataframe
    query = """
    SELECT s.student_id, s.roll_number, s.student_name, d.department_name,
           COUNT(e.enrollment_id) AS courses_taken, ROUND(AVG(g.marks), 2) AS average_marks
    FROM students s
    JOIN departments d ON s.department_id = d.department_id
    LEFT JOIN enrollments e ON s.student_id = e.student_id
    LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
    GROUP BY s.student_id, s.roll_number, s.student_name, d.department_name
    ORDER BY s.student_id;
    """
    try:
        return fetch_dataframe(query)
    except Exception as exc:
        return _fallback_or_raise(get_fallback_summary, exc)
