# EduVault — Academic Intelligence & Distributed Database Engine

EduVault is an enterprise academic information, analytics, and distributed database platform integrating **PostgreSQL**, **MongoDB**, **Python**, **Streamlit**, and **Pandas**.

The platform provides end-to-end coverage of relational data management, NoSQL activity tracking, **Transactions & Concurrency (Module 4)**, and **Replication & Sharding (Module 5)**.

---

## Architecture & Modules

### 🎓 1. Academic Intelligence & Analytics
- **PostgreSQL**: Normalized relational schema for departments, students, instructors, courses, prerequisites, enrollments, and grades.
- **MongoDB**: High-throughput NoSQL activity tracking for student video views, quiz attempts, assignment completions, and learning resources.
- **Analytics Engine**: Cohort summaries, department filtering, grade distributions, and student exploration.

### ⚡ 2. Module 4: Transactions & Concurrency
- **ACID Properties**:
  - **Atomicity**: All-or-nothing enrollment and tuition billing execution with `SAVEPOINT` and `ROLLBACK` support.
  - **Consistency**: Invariants declared via PostgreSQL `CHECK`, `UNIQUE`, and `FOREIGN KEY` constraints.
  - **Isolation**: Concurrent visibility control via MVCC snapshots and SQL isolation levels.
  - **Durability**: Write-Ahead Logging (WAL) and `fsync` flush guarantees.
- **SQL Isolation Levels & Concurrency Anomalies**:
  - In-depth interactive simulation of **Dirty Read**, **Non-Repeatable Read**, **Phantom Read**, and **Write Skew (Serialization Anomaly)** across `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, and `SERIALIZABLE`.
  - ANSI SQL standard vs PostgreSQL implementation differences.
- **PostgreSQL MVCC (Multi-Version Concurrency Control)**:
  - Physical tuple header inspection: `xmin`, `xmax`, `cid`, `ctid`.
  - Non-overwriting updates creating new tuple versions.
  - Dead tuple garbage collection via `VACUUM` and `VACUUM FULL`.
  - Heap-Only Tuples (HOT) index bypass optimization.
- **PostgreSQL Lock Matrix & Advisory Locks**:
  - Row locks: `FOR KEY SHARE`, `FOR SHARE`, `FOR NO KEY UPDATE`, `FOR UPDATE`.
  - Table locks: `ACCESS SHARE` through `ACCESS EXCLUSIVE`.
  - Application-level distributed advisory locks (`pg_advisory_lock`, `pg_try_advisory_lock`).
- **Deadlock Detection & Resolution**:
  - Wait-For Graph (WFG) cycle detection.
  - `deadlock_timeout` background detection and transaction abort resolution.
  - Deadlock prevention via deterministic global lock acquisition ordering.
- **Two-Phase Commit (2PC)**:
  - Distributed transaction coordination across PostgreSQL and MongoDB nodes.
  - Phase 1: `PREPARE TRANSACTION` with durable logging.
  - Phase 2: `COMMIT PREPARED` or `ROLLBACK PREPARED`.
- **Optimistic vs Pessimistic Concurrency Control**:
  - Pessimistic locking via `SELECT ... FOR UPDATE`.
  - Optimistic locking via version column verification (`WHERE version = v`).
  - Interactive race condition simulator for scarce course seats.

### 🌐 3. Module 5: Replication & Sharding
- **Replication Patterns & Topologies**:
  - **Synchronous vs Asynchronous Replication**: Durability (RPO = 0) vs Write Latency trade-offs.
  - **Single-Leader**, **Multi-Leader** (Active-Active conflict resolution), and **Leaderless** paradigms.
  - **Dynamo Quorum Consistency**: Interactive $W + R > N$ quorum calculator, tolerated failure metrics, and read repair.
- **PostgreSQL Streaming Replication (Physical)**:
  - Binary WAL streaming via `walsender` and `walreceiver`.
  - `pg_basebackup -R`, `standby.signal`, and replication slots (`pg_create_physical_replication_slot`).
  - Real-time replication lag monitoring via `pg_stat_replication`.
- **PostgreSQL Logical Replication**:
  - Publisher-Subscriber model based on WAL logical decoding.
  - Selective table replication, row filtering (`WHERE`), and cross-version migrations.
- **Database Sharding & Horizontal Partitioning**:
  - Sharding strategies: Hash-based (`hash(id) % N`), Range-based (Admission Year), and List/Directory-based (Department).
  - Query router simulation: Directed Point Queries ($O(1)$) vs Scatter-Gather Parallel Broadcast queries.
  - PostgreSQL declarative partitioning (`PARTITION BY RANGE`, `PARTITION BY HASH`).

---

## Project Structure

```text
EduVault/
│
├── app.py                             # Flagship Streamlit Web Application
├── requirements.txt                   # Project Python dependencies
├── README.md                          # Platform documentation
├── .env.example                       # Environment configuration template
│
├── analytics/                         # Academic Analytics layer
│   ├── student_analysis.py            # Student performance & cohort summaries
│   ├── course_analysis.py             # Course outcomes & grade distributions
│   └── activity_analysis.py           # MongoDB engagement logs
│
├── concurrency/                       # Module 4: Transactions & Concurrency
│   ├── acid_engine.py                 # ACID simulation engine & atomic rollback
│   ├── isolation_simulator.py         # Isolation levels & anomaly simulator
│   ├── mvcc_inspector.py              # PostgreSQL MVCC tuple visualizer & VACUUM
│   ├── locks_deadlock.py              # Row/table/advisory lock & deadlock engine
│   ├── two_phase_commit.py            # Distributed 2PC coordinator simulation
│   └── concurrency_control.py         # Optimistic vs Pessimistic race engine
│
├── replication/                       # Module 5: Replication & Sharding
│   ├── replication_patterns.py        # Topologies, Sync/Async, & Quorum calculator
│   ├── pg_replication.py              # Streaming & Logical replication manager
│   └── sharding_engine.py             # Hash/Range/List sharding & query router
│
├── database/                          # Connection & Storage layer
│   ├── postgres_db.py                 # PostgreSQL connection & query helper
│   ├── mongo_db.py                    # MongoDB database client
│   └── sample_data.py                 # Resilient fallback demo dataset
│
├── postgresql/                        # PostgreSQL SQL Reference Repository
│   ├── EduVault_backup.sql            # Master database backup
│   ├── concurrency/
│   │   ├── 01_acid_transactions.sql
│   │   ├── 02_isolation_levels_anomalies.sql
│   │   ├── 03_mvcc_internals.sql
│   │   ├── 04_locks_and_deadlocks.sql
│   │   ├── 05_two_phase_commit_2pc.sql
│   │   └── 06_optimistic_vs_pessimistic.sql
│   └── replication/
│       ├── 07_streaming_replication_setup.sql
│       ├── 08_logical_replication_setup.sql
│       └── 09_sharding_partitioning.sql
│
└── docs/                              # Detailed Technical Specifications
    ├── MODULE_4_TRANSACTIONS_AND_CONCURRENCY.md
    └── MODULE_5_REPLICATION_AND_SHARDING.md
```

---

## Quick Start & Running the Web App

### 1. Launch the Streamlit Application

You can run the web app directly using Python and Streamlit:

```bash
# If using system Python:
streamlit run app.py

# Or with specific Python executable:
python -m streamlit run app.py
```

### 2. Dual Operation Mode
- **Live Database Mode**: When local PostgreSQL and MongoDB credentials are provided in `.env`, the app queries the active databases.
- **Interactive Simulation Mode**: If PostgreSQL or MongoDB is offline, EduVault seamlessly falls back to interactive simulated engines and pre-loaded sample datasets without crashing.

---

## Testing & Verification

All modules have been developed with self-contained simulators, verified against PostgreSQL 14–18 specifications, and packaged with reproducible interactive demonstrations in the Streamlit application.
