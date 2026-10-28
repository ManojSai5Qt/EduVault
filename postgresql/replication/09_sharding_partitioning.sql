-- ============================================================================
-- EduVault Database Architecture
-- Module 5: Replication & Sharding
-- Script 09: Declarative Partitioning & Sharding
-- ============================================================================

-- ============================================================================
-- 1. RANGE PARTITIONING: Partitioning Activity Logs by Date Range
-- ============================================================================
CREATE TABLE student_activity_partitioned (
    log_id BIGSERIAL,
    student_id INTEGER NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    duration_minutes INTEGER,
    log_date DATE NOT NULL,
    PRIMARY KEY (log_id, log_date)
) PARTITION BY RANGE (log_date);

-- Create individual partitions (shards)
CREATE TABLE activity_y2025_q1 PARTITION OF student_activity_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

CREATE TABLE activity_y2025_q2 PARTITION OF student_activity_partitioned
    FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');

CREATE TABLE activity_y2025_q3 PARTITION OF student_activity_partitioned
    FOR VALUES FROM ('2025-07-01') TO ('2025-10-01');

CREATE TABLE activity_y2025_q4 PARTITION OF student_activity_partitioned
    FOR VALUES FROM ('2025-10-01') TO ('2026-01-01');

-- Partition Pruning Query:
-- PostgreSQL will ONLY scan activity_y2025_q3 and skip all others!
EXPLAIN SELECT * FROM student_activity_partitioned 
WHERE log_date BETWEEN '2025-08-01' AND '2025-08-31';


-- ============================================================================
-- 2. HASH PARTITIONING: Distributing Students across 3 Shard Partitions
-- ============================================================================
CREATE TABLE students_sharded (
    student_id INTEGER NOT NULL,
    roll_number VARCHAR(20) NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    department_id INTEGER NOT NULL,
    PRIMARY KEY (student_id)
) PARTITION BY HASH (student_id);

CREATE TABLE students_shard_0 PARTITION OF students_sharded
    FOR VALUES WITH (MODULUS 3, REMAINDER 0);

CREATE TABLE students_shard_1 PARTITION OF students_sharded
    FOR VALUES WITH (MODULUS 3, REMAINDER 1);

CREATE TABLE students_shard_2 PARTITION OF students_sharded
    FOR VALUES WITH (MODULUS 3, REMAINDER 2);


-- ============================================================================
-- 3. CROSS-NODE SHARDING WITH POSTGRES_FDW (Foreign Data Wrapper)
-- ============================================================================
-- Allows PostgreSQL to query remote physical database shards transparently:
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- Create server link to Shard Node 2:
-- CREATE SERVER shard2_server
-- FOREIGN DATA WRAPPER postgres_fdw
-- OPTIONS (host '10.0.2.10', port '5432', dbname 'eduvault_shard2');

-- CREATE USER MAPPING FOR current_user
-- SERVER shard2_server
-- OPTIONS (user 'postgres', password 'secret');

-- CREATE FOREIGN TABLE foreign_students_shard2 (
--     student_id INTEGER,
--     student_name VARCHAR(100)
-- ) SERVER shard2_server OPTIONS (table_name 'students');
