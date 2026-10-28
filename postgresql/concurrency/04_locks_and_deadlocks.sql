-- ============================================================================
-- EduVault Database Architecture
-- Module 4: Transactions & Concurrency
-- Script 04: PostgreSQL Locks & Deadlock Detection
-- ============================================================================

-- 1. ROW-LEVEL LOCKING
-- FOR UPDATE: Locks selected rows exclusively against concurrent updates/deletes.
BEGIN;
SELECT * FROM courses 
WHERE course_code = 'CS205' 
FOR UPDATE;

-- Concurrent transactions trying to SELECT ... FOR UPDATE or UPDATE CS205 will block!
UPDATE courses SET seats_available = seats_available - 1 WHERE course_code = 'CS205';
COMMIT;

-- FOR SHARE: Shared lock; prevents concurrent updates but allows concurrent FOR SHARE.
BEGIN;
SELECT * FROM courses WHERE course_code = 'CS101' FOR SHARE;
COMMIT;


-- 2. TABLE-LEVEL LOCKS
-- Check currently active locks in PostgreSQL:
SELECT 
    locktype, 
    relation::regclass AS table_name, 
    mode, 
    granted, 
    pid
FROM pg_locks
WHERE relation IS NOT NULL;


-- 3. ADVISORY LOCKS (Application-level distributed coordination)
-- Acquire a session-level advisory lock using an arbitrary 64-bit integer
SELECT pg_advisory_lock(9001);

-- Critical section: Only one backend worker can run this logic at any moment!
-- ... do batch academic grading or payroll generation ...

-- Release the advisory lock
SELECT pg_advisory_unlock(9001);

-- Transaction-level advisory lock (automatically released on COMMIT/ROLLBACK)
BEGIN;
SELECT pg_advisory_xact_lock(9001);
-- ... work ...
COMMIT; -- Lock released automatically


-- 4. DEADLOCK SIMULATION & RESOLUTION
-- PostgreSQL detects deadlocks automatically using a background timer: deadlock_timeout (default 1s).

-- SESSION 1:
-- BEGIN;
-- UPDATE student_wallets SET balance = balance - 100 WHERE student_id = 1;

-- SESSION 2:
-- BEGIN;
-- UPDATE student_wallets SET balance = balance - 150 WHERE student_id = 2;

-- SESSION 1:
-- UPDATE student_wallets SET balance = balance + 100 WHERE student_id = 2; -- BLOCKS on Session 2

-- SESSION 2:
-- UPDATE student_wallets SET balance = balance + 150 WHERE student_id = 1; -- BLOCKS on Session 1!
-- RESULT: Deadlock detected! PostgreSQL aborts Session 2:
-- ERROR: deadlock detected
-- DETAIL: Process 1423 waits for ShareLock on transaction 8891; blocked by process 1424.
-- Process 1424 waits for ShareLock on transaction 8890; blocked by process 1423.
-- HINT: See server log for query details.
