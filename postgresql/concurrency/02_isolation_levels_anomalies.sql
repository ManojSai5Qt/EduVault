-- ============================================================================
-- EduVault Database Architecture
-- Module 4: Transactions & Concurrency
-- Script 02: Isolation Levels & Concurrency Anomalies
-- ============================================================================

-- PostgreSQL supports 4 SQL standard isolation levels:
-- 1. READ UNCOMMITTED (Treated as READ COMMITTED in PostgreSQL)
-- 2. READ COMMITTED   (PostgreSQL default)
-- 3. REPEATABLE READ  (Snapshot Isolation)
-- 4. SERIALIZABLE     (Serializable Snapshot Isolation - SSI)

-- ============================================================================
-- SCENARIO A: NON-REPEATABLE READ (Under Read Committed vs Repeatable Read)
-- ============================================================================

-- SESSION 1 (Reviewer)
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT marks FROM grades WHERE enrollment_id = 1; -- Returns e.g. 78

    -- SESSION 2 (Simultaneous Instructor)
    BEGIN;
    UPDATE grades SET marks = 85 WHERE enrollment_id = 1;
    COMMIT;

-- SESSION 1 (Reviewer re-reads in same transaction)
SELECT marks FROM grades WHERE enrollment_id = 1; -- Returns 85! (Non-Repeatable Read)
COMMIT;

-- TO PREVENT THIS: Use REPEATABLE READ
-- SESSION 1 (With Repeatable Read)
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT marks FROM grades WHERE enrollment_id = 1; -- Returns 78
    -- Even after Session 2 commits changes, Session 1 still sees 78 from its snapshot!
SELECT marks FROM grades WHERE enrollment_id = 1; -- Still returns 78!
COMMIT;


-- ============================================================================
-- SCENARIO B: PHANTOM READ (Prevented in PostgreSQL Repeatable Read)
-- ============================================================================

-- SESSION 1 (Dean counting enrollments)
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM enrollments WHERE course_id = 1; -- Returns 25

    -- SESSION 2 (Registrar adding late enrollee)
    BEGIN;
    INSERT INTO enrollments (student_id, course_id, semester, enrollment_date)
    VALUES (45, 1, 'Semester 1', CURRENT_DATE);
    COMMIT;

-- SESSION 1 (Dean re-executes count)
SELECT COUNT(*) FROM enrollments WHERE course_id = 1; 
-- In PG REPEATABLE READ: Returns 25! (Phantom read PREVENTED via snapshot isolation)
COMMIT;


-- ============================================================================
-- SCENARIO C: WRITE SKEW / SERIALIZATION ANOMALY
-- ============================================================================
-- Rule: At least 1 TA must remain on duty in the exam hall.
-- Table: exam_proctors (proctor_id, name, status 'ON_DUTY' / 'ON_LEAVE')

-- SESSION 1 (Proctor Alice wants leave)
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM exam_proctors WHERE status = 'ON_DUTY'; -- Sees 2

    -- SESSION 2 (Proctor Bob also wants leave simultaneously)
    BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    SELECT COUNT(*) FROM exam_proctors WHERE status = 'ON_DUTY'; -- Also sees 2

-- SESSION 1 updates Alice
UPDATE exam_proctors SET status = 'ON_LEAVE' WHERE name = 'Alice';
COMMIT;

    -- SESSION 2 updates Bob
    UPDATE exam_proctors SET status = 'ON_LEAVE' WHERE name = 'Bob';
    COMMIT;
    -- Both commit! Now 0 proctors are on duty (Write Skew!).

-- TO SOLVE: Run with SERIALIZABLE (SSI)
-- Under SERIALIZABLE, PostgreSQL detects the rw-antidependency cycle and terminates
-- Session 2 with: ERROR: could not serialize access due to read/write dependencies
