"""MongoDB access with real health checks, operation timing, and explain statistics."""
from __future__ import annotations
import os, time
from collections import deque
from threading import Lock
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
_METRICS = deque(maxlen=1000)
_LOCK = Lock()
_CLIENT = None

def get_mongo_client():
    global _CLIENT
    if _CLIENT is None:
        from pymongo import MongoClient
        _CLIENT = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"),
            serverSelectionTimeoutMS=int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", "3000")),
            connectTimeoutMS=int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", "3000")),
            appname="EduVault", retryReads=True, retryWrites=True)
    return _CLIENT

def get_mongo_database():
    return get_mongo_client()[os.getenv("MONGO_DB", "eduvault_mongo")]

def mongo_health() -> dict:
    started = time.perf_counter()
    result = get_mongo_database().command("ping")
    return {"ok": bool(result.get("ok")), "latency_ms": round((time.perf_counter()-started)*1000, 3),
            "database": os.getenv("MONGO_DB", "eduvault_mongo")}

def timed_find(collection_name: str, filter_doc: dict | None = None,
               projection: dict | None = None, limit: int = 500):
    started = time.perf_counter()
    docs = list(get_mongo_database()[collection_name].find(filter_doc or {}, projection).limit(limit))
    with _LOCK:
        _METRICS.append({"operation":"find", "collection":collection_name,
            "elapsed_ms":round((time.perf_counter()-started)*1000,3),
            "documents":len(docs), "timestamp":time.time()})
    return docs

def explain_find(collection_name: str, filter_doc: dict | None = None, limit: int = 500) -> dict:
    return get_mongo_database().command({"explain":{"find":collection_name,
        "filter":filter_doc or {}, "limit":limit}, "verbosity":"executionStats"})

def get_mongo_metrics():
    with _LOCK:
        return list(_METRICS)

def mongo_collection_stats(collection_name: str) -> dict:
    return get_mongo_database().command("collStats", collection_name)
