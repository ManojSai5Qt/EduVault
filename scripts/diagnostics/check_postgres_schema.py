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

from database.postgres_db import get_postgres_connection

conn = get_postgres_connection()
cur = conn.cursor()

cur.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position
""")

for row in cur.fetchall():
    print(row)

cur.close()
conn.close()