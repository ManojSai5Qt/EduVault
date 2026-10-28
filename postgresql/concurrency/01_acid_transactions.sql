-- ============================================================================
-- EduVault Database Architecture
-- Module 4: Transactions & Concurrency
-- Script 01: ACID Transactions & Integrity Constraints
-- ============================================================================

-- 1. ATOMICITY & SAVEPOINTS: Course Enrollment & Fee Payment Transaction
-- If any operation fails, the entire transaction rolls back cleanly.
BEGIN;

-- Check student balance and deduct tuition fee ($600)
UPDATE students 
SET balance = balance - 600
WHERE student_id = 1 AND balance >= 600;

-- Create a SAVEPOINT after payment deduction
SAVEPOINT payment_settled;

-- Attempt to enroll student into CS205
INSERT INTO enrollments (student_id, course_id, semester, enrollment_date)
VALUES (1, 4, 'Semester 2', CURRENT_DATE);

-- Update available course capacity
UPDATE courses
SET seats_available = seats_available - 1
WHERE course_id = 4 AND seats_available > 0;

-- In case of partial optional failures (e.g. elective club sign-up):
-- ROLLBACK TO SAVEPOINT payment_settled;

-- Commit all changes atomically
COMMIT;


-- 2. CONSISTENCY: Enforcing Business Rules via Database Constraints
-- Adding CHECK constraints to prevent invalid academic states
ALTER TABLE courses 
ADD CONSTRAINT check_credits_positive CHECK (credits > 0);

ALTER TABLE courses
ADD CONSTRAINT check_seats_non_negative CHECK (seats_available >= 0);

ALTER TABLE grades
ADD CONSTRAINT check_marks_range CHECK (marks >= 0 AND marks <= 100);

-- Demonstrating Consistency Enforcement:
-- This transaction will ABORT because marks exceed 100
BEGIN;
INSERT INTO grades (enrollment_id, marks, grade, grade_point)
VALUES (999, 105, 'A+', 10.0); -- Fails with check_marks_range violation!
COMMIT; -- Transaction aborted by PostgreSQL


-- 3. DURABILITY: Write-Ahead Logging (WAL) Configuration
-- PostgreSQL ensures committed transactions survive power outages and crashes by
-- writing changes to the Write-Ahead Log (WAL) on disk before modifying heap pages.
SHOW wal_level;
SHOW fsync;
SHOW synchronous_commit;

-- For ultra-reliable financial/grade systems:
-- SET synchronous_commit = 'on'; -- Commits wait for WAL to be written & flushed to disk (fsync).
