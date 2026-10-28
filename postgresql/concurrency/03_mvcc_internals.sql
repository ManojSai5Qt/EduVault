-- ============================================================================
-- EduVault Database Architecture
-- Module 4: Transactions & Concurrency
-- Script 03: PostgreSQL MVCC Internals & Heap Inspection
-- ============================================================================

-- PostgreSQL uses Multi-Version Concurrency Control (MVCC).
-- Updates never overwrite in place; they write a new tuple version.
-- Deletes set xmax without immediately freeing disk space.

-- 1. Inspect Hidden System Attributes of Rows:
--   ctid: Physical location (page_number, item_offset)
--   xmin: Transaction ID that inserted this tuple
--   xmax: Transaction ID that deleted or replaced this tuple (0 if live)
SELECT 
    ctid,
    xmin,
    xmax,
    student_id,
    roll_number,
    student_name
FROM students
LIMIT 5;

-- 2. Observe Row Version Creation during UPDATE:
-- Current row version
SELECT ctid, xmin, xmax, marks FROM grades WHERE enrollment_id = 1;

-- Run UPDATE in a transaction
BEGIN;
SELECT txid_current(); -- Note current transaction ID
UPDATE grades SET marks = marks + 2 WHERE enrollment_id = 1;
COMMIT;

-- Observe that ctid and xmin have changed!
-- The previous tuple now has its xmax set to the transaction ID, marking it dead.
SELECT ctid, xmin, xmax, marks FROM grades WHERE enrollment_id = 1;


-- 3. Dead Tuples and VACUUM
-- Inspect table bloat and dead tuple count via pg_stat_user_tables
SELECT 
    relname AS table_name,
    n_live_tup AS live_tuples,
    n_dead_tup AS dead_tuples,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE relname IN ('students', 'grades', 'courses');

-- Reclaim space occupied by dead tuples:
VACUUM VERBOSE grades;

-- Full table rewrite to reclaim disk space back to the Operating System:
-- VACUUM FULL grades; -- Note: Requires ACCESS EXCLUSIVE lock!


-- 4. Heap-Only Tuples (HOT) Optimization
-- When an UPDATE does NOT alter indexed columns and there is free space
-- on the same heap page, PostgreSQL creates a HOT tuple, skipping index updates.
SELECT 
    relname, 
    n_tup_upd, 
    n_tup_hot_upd,
    ROUND((n_tup_hot_upd::numeric / NULLIF(n_tup_upd, 0)) * 100, 2) AS hot_update_percentage
FROM pg_stat_user_tables
WHERE relname = 'grades';
