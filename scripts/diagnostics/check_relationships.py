# Add the repository root to the import path so this script works
# when launched directly from its new scripts/ subfolder.
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


from database.postgres_db import fetch_dataframe
from database.mongo_db import get_mongo_database

print("\n--- DEPARTMENTS ---")
print(fetch_dataframe(
    "SELECT department_id, department_name FROM departments"
).to_string(index=False))

print("\n--- STUDENTS ---")
print(fetch_dataframe(
    "SELECT student_id, roll_number, student_name, department_id "
    "FROM students ORDER BY student_id"
).to_string(index=False))

print("\n--- COURSES ---")
print(fetch_dataframe(
    "SELECT course_id, course_code, course_name, department_id "
    "FROM courses ORDER BY course_id"
).to_string(index=False))

db = get_mongo_database()

print("\n--- MONGODB COURSE CODES ---")
print("Learning content:", db["learning_content"].distinct("course_code"))
print("Activity logs:", db["activity_logs"].distinct("course_code"))

print("\n--- MONGODB STUDENT IDS ---")
print(db["activity_logs"].distinct("student_id"))