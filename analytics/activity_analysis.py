import os
import pandas as pd
from database.sample_data import get_fallback_activities

def get_activity_data():
    from database.mongo_db import timed_find
    try:
        data = timed_find("activity_logs", {}, {"_id": 0}, 500)
        return pd.DataFrame(data)
    except Exception as exc:
        if os.getenv("EDUVAULT_DEMO_MODE", "false").lower() == "true":
            return get_fallback_activities()
        raise RuntimeError("MongoDB activity query failed; live MongoDB is required unless demo mode is enabled.") from exc

def get_activity_count():
    from database.mongo_db import get_mongo_database
    try:
        return get_mongo_database()["activity_logs"].count_documents({})
    except Exception as exc:
        if os.getenv("EDUVAULT_DEMO_MODE", "false").lower() == "true":
            return len(get_fallback_activities())
        raise RuntimeError("MongoDB activity count failed.") from exc
