-- ============================================================================
-- EduVault Database Architecture
-- Module 4: Transactions & Concurrency
-- Script 05: Two-Phase Commit (2PC) in PostgreSQL
-- ============================================================================

-- PostgreSQL supports distributed transactions using the Two-Phase Commit protocol.
-- In postgresql.conf, set: max_prepared_transactions = 100

-- ============================================================================
-- PHASE 1: PREPARE
-- ============================================================================
-- The distributed coordinator (e.g. EduVault middleware) tells PostgreSQL to prepare:
BEGIN;

UPDATE students 
SET balance = balance - 500 
WHERE student_id = 1;

INSERT INTO enrollments (student_id, course_id, semester, enrollment_date)
VALUES (1, 2, 'Semester 1', CURRENT_DATE);

-- Instead of COMMIT, the transaction is prepared with a globally unique identifier (GID):
PREPARE TRANSACTION 'eduvault_enrollment_tx_901';

-- At this point:
-- 1. The transaction is detached from the current database session.
-- 2. Changes and acquired locks remain HELD on disk.
-- 3. Even if the client connection drops or server restarts, this transaction persists!

-- Check currently prepared (in-doubt) distributed transactions:
SELECT 
    gid, 
    prepared, 
    owner, 
    database 
FROM pg_prepared_xacts;


-- ============================================================================
-- PHASE 2: COMMIT OR ROLLBACK
-- ============================================================================
-- If all participating nodes (e.g. PostgreSQL + MongoDB + Payment Gateway) vote YES:
COMMIT PREPARED 'eduvault_enrollment_tx_901';

-- OR, if any participating node fails or aborts:
-- ROLLBACK PREPARED 'eduvault_enrollment_tx_901';
