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
    started = time.perf_counter()
    result = get_mongo_database().command({"explain":{"find":collection_name,
        "filter":filter_doc or {}, "limit":limit}, "verbosity":"executionStats"})
    with _LOCK:
        _METRICS.append({"operation":"explain", "collection":collection_name,
            "elapsed_ms":round((time.perf_counter()-started)*1000,3),
            "documents":result.get("executionStats", {}).get("nReturned"),
            "timestamp":time.time()})
    return result

def timed_count(collection_name: str, filter_doc: dict | None = None) -> int:
    started = time.perf_counter()
    count = get_mongo_database()[collection_name].count_documents(filter_doc or {})
    with _LOCK:
        _METRICS.append({"operation":"count", "collection":collection_name,
            "elapsed_ms":round((time.perf_counter()-started)*1000,3),
            "documents":count, "timestamp":time.time()})
    return count

def get_mongo_metrics():
    with _LOCK:
        return list(_METRICS)

def mongo_collection_stats(collection_name: str) -> dict:
    return get_mongo_database().command("collStats", collection_name)

def mongo_cluster_status() -> dict:
    """Inspect the connected MongoDB topology; never invent shard nodes."""
    admin = get_mongo_client().admin
    hello = admin.command("hello")
    if hello.get("msg") == "isdbgrid":
        try:
            shards = admin.command("listShards").get("shards", [])
        except Exception as exc:
            shards = []
            return {"topology": "mongos", "sharding": "enabled", "shards": shards,
                    "shard_error": str(exc)}
        return {"topology": "mongos", "sharding": "enabled", "shards": shards}
    if hello.get("setName"):
        return {"topology": "replica set", "replica_set": hello["setName"],
                "members": hello.get("hosts", []), "primary": hello.get("primary")}
    return {"topology": "standalone", "sharding": "not detected", "message": "Connected to a standalone MongoDB server."}

def timed_create_index(collection_name: str, keys: list[tuple[str, int]], name: str) -> str:
    """Create a specifically selected MongoDB index and record the operation duration."""
    started = time.perf_counter()
    result = get_mongo_database()[collection_name].create_index(keys, name=name)
    with _LOCK:
        _METRICS.append({"operation":"create_index", "collection":collection_name,
            "elapsed_ms":round((time.perf_counter()-started)*1000,3),
            "index_name":result, "timestamp":time.time()})
    return result
