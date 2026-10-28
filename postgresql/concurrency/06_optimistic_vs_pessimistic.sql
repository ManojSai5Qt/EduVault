-- ============================================================================
-- EduVault Database Architecture
-- Module 4: Transactions & Concurrency
-- Script 06: Optimistic vs Pessimistic Concurrency Control
-- ============================================================================

-- ============================================================================
-- 1. PESSIMISTIC CONCURRENCY CONTROL (PCC)
-- Approach: Lock the resource immediately on read; hold lock until finished.
-- ============================================================================
BEGIN;

-- Lock the target course row with FOR UPDATE
SELECT course_id, seats_available 
FROM courses 
WHERE course_code = 'CS205' 
FOR UPDATE;

-- Only one concurrent transaction can reach this line at any time!
UPDATE courses 
SET seats_available = seats_available - 1 
WHERE course_code = 'CS205';

INSERT INTO enrollments (student_id, course_id, semester, enrollment_date)
VALUES (1, 4, 'Semester 2', CURRENT_DATE);

COMMIT; -- Lock released


-- ============================================================================
-- 2. OPTIMISTIC CONCURRENCY CONTROL (OCC)
-- Approach: Read without locks. Check version column at update time.
-- If another transaction modified the row, the UPDATE matches 0 rows!
-- ============================================================================

-- Step A: Add version column to course table
ALTER TABLE courses ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

-- Step B: Read without holding any locks
SELECT course_id, seats_available, version 
FROM courses 
WHERE course_code = 'CS205';
-- Suppose this returned: seats_available = 5, version = 12

-- Step C: Perform conditional atomic update
UPDATE courses 
SET 
    seats_available = seats_available - 1,
    version = version + 1
WHERE course_code = 'CS205' 
  AND version = 12; -- MUST match the version read earlier!

-- Application checks affected row count:
-- If affected_rows == 1: Update succeeded!
-- If affected_rows == 0: Concurrent conflict occurred! Rollback and retry.
