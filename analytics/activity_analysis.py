import pandas as pd
from database.sample_data import get_fallback_activities

def get_activity_data():
    try:
        from database.mongo_db import get_mongo_database
        db = get_mongo_database()
        collection = db["activity_logs"]
        data = list(collection.find({}, {"_id": 0}).limit(500))
        if data:
            return pd.DataFrame(data)
        return get_fallback_activities()
    except Exception:
        return get_fallback_activities()


def get_activity_count():
    try:
        from database.mongo_db import get_mongo_database
        db = get_mongo_database()
        return db["activity_logs"].count_documents({})
    except Exception:
        return len(get_fallback_activities())
