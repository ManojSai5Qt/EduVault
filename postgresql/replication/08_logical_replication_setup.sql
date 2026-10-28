-- ============================================================================
-- EduVault Database Architecture
-- Module 5: Replication & Sharding
-- Script 08: PostgreSQL Logical Replication (Publisher-Subscriber)
-- ============================================================================

-- ============================================================================
-- STEP 1: PUBLISHER SERVER SETUP (Primary Academic Node)
-- ============================================================================
-- postgresql.conf requires:
-- wal_level = logical

-- Create Publication for EduVault academic tables:
CREATE PUBLICATION eduvault_academic_pub 
FOR TABLE departments, courses, course_prerequisites;

-- Publication with row filtering (e.g. only replicate CS department students):
CREATE PUBLICATION eduvault_cs_students_pub 
FOR TABLE students WHERE (department_id = 1);

-- Inspect active publications:
SELECT * FROM pg_publication;
SELECT * FROM pg_publication_tables;


-- ============================================================================
-- STEP 2: SUBSCRIBER SERVER SETUP (Analytics / Reporting Node)
-- ============================================================================
-- Tables must exist on the subscriber before subscribing (DDL is not replicated).

CREATE SUBSCRIPTION eduvault_academic_sub
CONNECTION 'host=primary_ip port=5432 dbname=eduvault user=repuser password=EduVaultRep2026!'
PUBLICATION eduvault_academic_pub
WITH (copy_data = true, create_slot = true, enabled = true);

-- Inspect subscription worker status:
SELECT 
    subid,
    subname,
    pid,
    relid,
    received_lsn,
    last_msg_receipt_time,
    latest_end_lsn
FROM pg_stat_subscription;

-- Alter or pause subscription if needed:
-- ALTER SUBSCRIPTION eduvault_academic_sub DISABLE;
-- ALTER SUBSCRIPTION eduvault_academic_sub REFRESH PUBLICATION;
