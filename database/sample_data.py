import pandas as pd
import numpy as np
from datetime import datetime, timedelta

FIRST_NAMES = [
    "Aarav", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Rahul", "Priya", "Sneha", "Vikram",
    "Aditya", "Meera", "Rohan", "Saanvi", "Varun", "Nisha", "Kiran", "Pooja", "Sai", "Keerthi",
    "Abhishek", "Bhavya", "Chetan", "Deepika", "Esha", "Farhan", "Gautam", "Harini", "Imran", "Jyothi",
    "Karthik", "Lavanya", "Manish", "Neha", "Omkar", "Pranav", "Rithika", "Sanjay", "Tanvi", "Uday",
    "Vaishnavi", "Yash", "Zoya", "Akhil", "Divya", "Harsh", "Madhavi", "Naveen", "Pallavi", "Suraj"
]

LAST_NAMES = [
    "Sharma", "Reddy", "Kumar", "Patel", "Verma", "Rao", "Singh", "Gupta", "Naidu", "Das",
    "Choudhury", "Joshi", "Mishra", "Bhat", "Mehta", "Iyer", "Nair", "Saxena", "Kapoor", "Pillai"
]

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Electronics & Comm",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Data Science & AI"
]

COURSES_LIST = [
    ("CS101", "Introduction to Database Systems", 4),
    ("CS102", "Data Structures and Algorithms", 4),
    ("IT201", "Distributed Systems & Cloud", 3),
    ("CS205", "Advanced PostgreSQL & MVCC", 3),
    ("DS301", "Big Data Analytics & MongoDB", 4),
    ("EC104", "Computer Architecture & Networks", 3)
]

def get_fallback_summary():
    # Deterministic generation of 250 students
    np.random.seed(2026)
    students = []
    for i in range(1, 251):
        first = FIRST_NAMES[(i - 1) % len(FIRST_NAMES)]
        last = LAST_NAMES[((i - 1) // len(FIRST_NAMES) + i) % len(LAST_NAMES)]
        name = f"{first} {last}"
        dept = DEPARTMENTS[i % len(DEPARTMENTS)]
        avg_m = round(float(np.random.normal(loc=81.5, scale=8.5)), 2)
        avg_m = min(98.5, max(54.0, avg_m))
        students.append({
            "student_id": i,
            "roll_number": f"EV26{i:04d}",
            "student_name": name,
            "department_name": dept,
            "courses_taken": 5,
            "average_marks": avg_m
        })
    return pd.DataFrame(students)

def get_fallback_performance():
    summary = get_fallback_summary().to_dict(orient="records")
    np.random.seed(2026)
    rows = []
    for s in summary:
        sid = s["student_id"]
        # each student takes 5 out of the 6 courses
        for idx in range(5):
            c_info = COURSES_LIST[(sid + idx) % len(COURSES_LIST)]
            code, cname, credits = c_info
            base = s["average_marks"]
            marks = int(np.clip(base + np.random.randint(-10, 11), 50, 99))
            grade = "A+" if marks >= 90 else ("A" if marks >= 80 else ("B+" if marks >= 70 else ("B" if marks >= 60 else "C")))
            gp = 10.0 if marks >= 90 else (9.0 if marks >= 80 else (8.0 if marks >= 70 else (7.0 if marks >= 60 else 6.0)))
            rows.append({
                "student_id": sid,
                "roll_number": s["roll_number"],
                "student_name": s["student_name"],
                "department_name": s["department_name"],
                "course_code": code,
                "course_name": cname,
                "semester": "Semester 1" if idx < 3 else "Semester 2",
                "marks": marks,
                "grade": grade,
                "grade_point": gp
            })
    return pd.DataFrame(rows)

def get_fallback_courses():
    perf = get_fallback_performance()
    grouped = perf.groupby(["course_code", "course_name"]).agg(
        students_enrolled=("student_id", "count"),
        average_marks=("marks", "mean"),
        highest_marks=("marks", "max"),
        lowest_marks=("marks", "min")
    ).reset_index()
    grouped["course_id"] = list(range(1, len(grouped) + 1))
    grouped["average_marks"] = grouped["average_marks"].round(2)
    return grouped

def get_fallback_activities():
    types = ["Video Watched", "Quiz Attempted", "Notes Read", "Assignment Completed"]
    courses = [c[0] for c in COURSES_LIST]
    base_time = datetime(2026, 9, 1, 9, 0)
    data = []
    # Generate 1,500 activity logs
    np.random.seed(2026)
    for i in range(1, 1501):
        sid = (i % 250) + 1
        c_code = courses[i % len(courses)]
        act_type = types[i % len(types)]
        duration = int(np.random.randint(5, 55))
        pct = int(np.random.choice([30, 50, 75, 80, 90, 100]))
        ts = (base_time + timedelta(days=i % 60, hours=(i % 12) + 8, minutes=i % 60)).strftime("%Y-%m-%d %H:%M:%S")
        data.append({
            "student_id": sid,
            "course_code": c_code,
            "activity_type": act_type,
            "content_id": f"EV-LC-{c_code}",
            "duration_minutes": duration,
            "completion_percentage": pct,
            "timestamp": ts
        })
    return pd.DataFrame(data)
