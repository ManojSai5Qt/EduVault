"""PostgreSQL access with query telemetry and safe query-plan inspection."""
from __future__ import annotations
import os, re, time
from collections import deque
from threading import Lock
from typing import Any
import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_METRICS = deque(maxlen=1000)
_METRICS_LOCK = Lock()

def _record(sql: str, elapsed_ms: float, rows: int | None, ok: bool, error: str | None = None) -> None:
    normalized = re.sub(r"\\s+", " ", sql).strip()[:500]
    with _METRICS_LOCK:
        _METRICS.append({"query": normalized, "elapsed_ms": round(elapsed_ms, 3), "rows": rows,
                         "success": ok, "error": error, "timestamp": time.time()})

def get_postgres_connection():
    """Open a configured PostgreSQL connection. No silent fallback is performed."""
    dsn = os.getenv("DATABASE_URL")
    try:
        import psycopg2
        if dsn:
            return psycopg2.connect(dsn, connect_timeout=int(os.getenv("DB_CONNECT_TIMEOUT", "5")),
                                    application_name="EduVault")
        return psycopg2.connect(host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")), dbname=os.getenv("POSTGRES_DB", "eduvault"),
            user=os.getenv("POSTGRES_USER", "postgres"), password=os.getenv("POSTGRES_PASSWORD", ""),
            connect_timeout=int(os.getenv("DB_CONNECT_TIMEOUT", "5")), application_name="EduVault")
    except ImportError:
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError("Install psycopg2-binary or psycopg to use PostgreSQL.") from exc
        if dsn:
            return psycopg.connect(dsn, connect_timeout=int(os.getenv("DB_CONNECT_TIMEOUT", "5")),
                                   application_name="EduVault")
        return psycopg.connect(host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")), dbname=os.getenv("POSTGRES_DB", "eduvault"),
            user=os.getenv("POSTGRES_USER", "postgres"), password=os.getenv("POSTGRES_PASSWORD", ""),
            connect_timeout=int(os.getenv("DB_CONNECT_TIMEOUT", "5")), application_name="EduVault")

def fetch_dataframe(query: str, params: tuple | dict | None = None) -> pd.DataFrame:
    """Execute an application query and record actual client-side elapsed time."""
    started, conn = time.perf_counter(), None
    try:
        conn = get_postgres_connection()
        frame = pd.read_sql_query(query, conn, params=params)
        _record(query, (time.perf_counter()-started)*1000, len(frame), True)
        return frame
    except Exception as exc:
        _record(query, (time.perf_counter()-started)*1000, None, False, str(exc)[:300])
        raise
    finally:
        if conn is not None:
            conn.close()

def execute_readonly(query: str, params: tuple | dict | None = None) -> list[dict[str, Any]]:
    """Run one read-only SQL statement with server-side read-only transaction guard."""
    if not re.match(r"^\\s*(SELECT|WITH|SHOW|EXPLAIN)\\b", query, re.IGNORECASE):
        raise ValueError("Only read-only SQL statements are accepted.")
    started, conn = time.perf_counter(), None
    try:
        conn = get_postgres_connection()
        conn.set_session(readonly=True, autocommit=False)
        cur = conn.cursor()
        cur.execute("SET LOCAL statement_timeout = '10s'")
        cur.execute(query, params)
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = [dict(zip(columns, row)) for row in cur.fetchall()] if columns else []
        conn.rollback()
        _record(query, (time.perf_counter()-started)*1000, len(rows), True)
        return rows
    except Exception as exc:
        if conn is not None:
            conn.rollback()
        _record(query, (time.perf_counter()-started)*1000, None, False, str(exc)[:300])
        raise
    finally:
        if conn is not None:
            conn.close()

def explain_query(query: str, params: tuple | dict | None = None, analyze: bool = False) -> dict:
    """Explain SELECT/WITH only. ANALYZE is opt-in because it executes the query."""
    if not re.match(r"^\\s*(SELECT|WITH)\\b", query, re.IGNORECASE):
        raise ValueError("EXPLAIN is restricted to SELECT/WITH queries.")
    mode = "ANALYZE, BUFFERS, VERBOSE, FORMAT JSON" if analyze else "BUFFERS, VERBOSE, FORMAT JSON"
    result = execute_readonly(f"EXPLAIN ({mode}) {query}", params)
    return result[0]["QUERY PLAN"][0] if result else {}

def get_query_metrics() -> pd.DataFrame:
    with _METRICS_LOCK:
        return pd.DataFrame(list(_METRICS))

def postgres_health() -> dict:
    rows = execute_readonly("""SELECT current_database() AS database, current_user AS username,
        version() AS version, pg_is_in_recovery() AS is_replica, now() AS checked_at""")
    return rows[0]

def get_slow_queries(limit: int = 50) -> pd.DataFrame:
    """Requires pg_stat_statements to be installed and enabled by the DBA."""
    return pd.DataFrame(execute_readonly("""SELECT queryid, calls,
        round(total_exec_time::numeric, 2) AS total_ms,
        round(mean_exec_time::numeric, 2) AS mean_ms, rows, shared_blks_hit, shared_blks_read,
        left(query, 500) AS query FROM pg_stat_statements
        ORDER BY mean_exec_time DESC LIMIT %s""", (limit,)))

def get_replication_status() -> pd.DataFrame:
    return pd.DataFrame(execute_readonly("""SELECT application_name, client_addr, state, sync_state,
        sent_lsn, write_lsn, flush_lsn, replay_lsn, write_lag, flush_lag, replay_lag
        FROM pg_stat_replication ORDER BY application_name"""))

def get_table_index_stats(limit: int = 100) -> pd.DataFrame:
    return pd.DataFrame(execute_readonly("""SELECT schemaname, relname AS table_name, seq_scan,
        seq_tup_read, idx_scan, idx_tup_fetch, n_live_tup, n_dead_tup
        FROM pg_stat_user_tables ORDER BY seq_tup_read DESC LIMIT %s""", (limit,)))

def list_indexes() -> pd.DataFrame:
    return pd.DataFrame(execute_readonly("""SELECT schemaname, tablename, indexname, indexdef
        FROM pg_indexes WHERE schemaname NOT IN ('pg_catalog','information_schema')
        ORDER BY schemaname, tablename, indexname"""))

def create_index_concurrently(index_name: str, table_name: str, columns: list[str]) -> None:
    """Create a reviewed B-tree index; identifiers are validated and DDL is never automatic."""
    valid = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    if not valid.fullmatch(index_name) or not valid.fullmatch(table_name):
        raise ValueError("Invalid index/table identifier.")
    if not columns or any(not valid.fullmatch(c) for c in columns):
        raise ValueError("Invalid index columns.")
    conn = get_postgres_connection()
    try:
        conn.autocommit = True
        cur = conn.cursor()
        cols = ", ".join('"' + c + '"' for c in columns)
        cur.execute(f'CREATE INDEX CONCURRENTLY IF NOT EXISTS "{index_name}" ON "{table_name}" ({cols})')
    finally:
        conn.close()
