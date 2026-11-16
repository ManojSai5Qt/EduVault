import os
from database.sample_data import get_fallback_courses

def get_course_outcomes():
    from database.postgres_db import fetch_dataframe
    query = """
    SELECT c.course_id, c.course_code, c.course_name,
           COUNT(e.enrollment_id) AS students_enrolled,
           ROUND(AVG(g.marks), 2) AS average_marks,
           MAX(g.marks) AS highest_marks, MIN(g.marks) AS lowest_marks
    FROM courses c
    LEFT JOIN enrollments e ON c.course_id = e.course_id
    LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
    GROUP BY c.course_id, c.course_code, c.course_name
    ORDER BY c.course_id;
    """
    try:
        return fetch_dataframe(query)
    except Exception as exc:
        if os.getenv("EDUVAULT_DEMO_MODE", "false").lower() == "true":
            return get_fallback_courses()
        raise RuntimeError("Course analytics query failed; live PostgreSQL is required unless demo mode is enabled.") from exc
