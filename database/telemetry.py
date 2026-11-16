"""Database health and live query metric helpers."""
import pandas as pd

def get_database_health():
    result = {}
    try:
        from database.postgres_db import postgres_health
        result["PostgreSQL"] = {"connected": True, **postgres_health()}
    except Exception as exc:
        result["PostgreSQL"] = {"connected": False, "error": str(exc)}
    try:
        from database.mongo_db import mongo_health
        result["MongoDB"] = {"connected": True, **mongo_health()}
    except Exception as exc:
        result["MongoDB"] = {"connected": False, "error": str(exc)}
    return result

def get_postgres_query_metrics():
    from database.postgres_db import get_query_metrics
    return get_query_metrics()

def get_mongo_query_metrics():
    from database.mongo_db import get_mongo_metrics
    return pd.DataFrame(get_mongo_metrics())
