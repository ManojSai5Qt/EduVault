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


from database.mongo_db import get_mongo_database

db = get_mongo_database()

for name in ["learning_content", "activity_logs"]:
    collection = db[name]

    print(f"\n--- {name} ---")
    print("Total records:", collection.count_documents({}))

    for doc in collection.find({}, {"_id": 0}).limit(2):
        print("Fields:", list(doc.keys()))
        print("Sample:", doc)