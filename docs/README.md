# EduVault Technical Documentation

This directory contains in-depth architectural and theoretical documentation for EduVault:

- **[MODULE_4_TRANSACTIONS_AND_CONCURRENCY.md](MODULE_4_TRANSACTIONS_AND_CONCURRENCY.md)**:
  - ACID properties (Atomicity, Consistency, Isolation, Durability)
  - SQL isolation levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable)
  - Concurrency anomalies (Dirty Read, Non-Repeatable Read, Phantom Read, Write Skew)
  - PostgreSQL MVCC internals (xmin, xmax, cmin, cmax, ctid, VACUUM, HOT)
  - Lock hierarchy (Row locks, Table locks, Advisory locks)
  - Deadlock detection and Wait-For Graph (WFG) cycle resolution
  - Two-Phase Commit (2PC) distributed protocol
  - Optimistic Concurrency Control (OCC) vs Pessimistic Concurrency Control (PCC)

- **[MODULE_5_REPLICATION_AND_SHARDING.md](MODULE_5_REPLICATION_AND_SHARDING.md)**:
  - Replication patterns: Synchronous vs Asynchronous replication
  - Topologies: Single-Leader (Primary-Replica), Multi-Leader (Active-Active), and Leaderless (Dynamo quorum: W + R > N)
  - PostgreSQL Physical Streaming Replication (WAL streaming, pg_basebackup, standby.signal, replication slots)
  - PostgreSQL Logical Replication (Publisher-Subscriber, row filtering, CDC)
  - Database Sharding and Horizontal Partitioning (Hash-based, Range-based, List-based, Query routing, Scatter-Gather)
