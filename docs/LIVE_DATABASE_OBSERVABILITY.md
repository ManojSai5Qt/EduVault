# EduVault Live Database Observability

## Connection behavior
EduVault checks PostgreSQL and MongoDB at startup and reports their actual health. In live mode, connection failures are visible and stop the analytics UI instead of silently substituting synthetic records.

Set `EDUVAULT_DEMO_MODE=true` only when you deliberately want sample data for a presentation. In demo mode the status banner still shows which databases are offline and clearly labels synthetic data.

## Configuration
Copy `.env.example` to `.env` and provide:
- `DATABASE_URL`, or `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `POSTGRES_POOL_MAX` (maximum pooled PostgreSQL connections)
- `MONGO_URI` and `MONGO_DB`

Never commit `.env` or production credentials.

## Query visibility
- PostgreSQL queries sent through `fetch_dataframe` and `execute_readonly` are timed and recorded in a bounded in-process metrics buffer.
- PostgreSQL connection borrowing uses a thread-safe psycopg2 pool when psycopg2 is installed.
- PostgreSQL `EXPLAIN (BUFFERS, VERBOSE, FORMAT JSON)` is available in the dashboard. `EXPLAIN ANALYZE` is opt-in because it executes the SELECT.
- Server-wide historical query statistics come from `pg_stat_statements`, if a DBA has enabled it.
- MongoDB find, count, and explain operations expose measured client latency and explain execution statistics.
- Query timings are per Streamlit application process; they are not a durable, cross-worker time-series store.

## PostgreSQL server statistics
A database administrator can enable `pg_stat_statements` by adding it to `shared_preload_libraries` in PostgreSQL configuration and restarting the server. Then, in the EduVault database, run:

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

The dashboard reports an unavailable message if the extension is not installed or the connecting role lacks permission.

## Replication and partition monitoring
- On a primary, replication details are read from `pg_stat_replication`.
- On a standby, WAL receiver details are read from `pg_stat_wal_receiver`.
- PostgreSQL partition metadata is read from the system catalogs.
- MongoDB topology is inspected using the server `hello` command; `listShards` is requested only when connected through `mongos`.
- An empty replication/partition result is displayed as “not configured/not found”, not as a healthy cluster.
- The dashboard does not automatically trigger failover, shard migration, or production cluster rebalancing.

## Index workflow
The Index Advisor displays current-schema table scan statistics and existing index definitions. An index is created only after the operator chooses the table/columns and confirms the action. Identifiers and column existence are checked, the index uses `CREATE INDEX CONCURRENTLY`, and `ANALYZE` refreshes planner statistics. Indexes increase storage and write overhead, so review the workload first.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
