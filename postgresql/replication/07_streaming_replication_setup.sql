-- ============================================================================
-- EduVault Database Architecture
-- Module 5: Replication & Sharding
-- Script 07: PostgreSQL Physical Streaming Replication
-- ============================================================================

-- ============================================================================
-- STEP 1: PRIMARY SERVER CONFIGURATION (postgresql.conf & pg_hba.conf)
-- ============================================================================
-- postgresql.conf:
-- wal_level = replica
-- max_wal_senders = 10
-- wal_keep_size = 1024MB
-- synchronous_commit = on   -- 'on' for sync, 'off' for async, 'remote_apply' for read-after-write
-- synchronous_standby_names = 'FIRST 1 (standby_node_1, standby_node_2)'

-- Create dedicated replication user on PRIMARY:
CREATE ROLE repuser WITH REPLICATION LOGIN ENCRYPTED PASSWORD 'EduVaultRep2026!';

-- pg_hba.conf (allow standby IP connection):
-- host  replication  repuser  10.0.0.0/16  scram-sha-256


-- ============================================================================
-- STEP 2: CREATE REPLICATION SLOT ON PRIMARY
-- ============================================================================
-- Ensures Primary retains WAL files until the replica confirms receiving them.
SELECT * FROM pg_create_physical_replication_slot('standby_slot_1');


-- ============================================================================
-- STEP 3: INITIALIZE STANDBY NODE (Run on Standby server)
-- ============================================================================
-- Stop standby postgres service, clear data directory, and clone base backup:
-- pg_basebackup -h primary_ip -p 5432 -U repuser -D /var/lib/postgresql/data -Fp -Xs -P -R --slot=standby_slot_1

-- The -R option automatically:
-- 1. Creates 'standby.signal' file in the standby data directory.
-- 2. Appends primary_conninfo into postgresql.auto.conf.


-- ============================================================================
-- STEP 4: MONITOR STREAMING REPLICATION & LAG
-- ============================================================================
-- Run on PRIMARY to inspect connected standbys:
SELECT 
    client_addr AS standby_ip,
    application_name,
    state,
    sync_state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replication_lag_bytes,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;

-- Run on STANDBY to verify standby receiver state:
SELECT 
    status,
    receive_start_lsn,
    received_lsn,
    last_msg_send_time,
    last_msg_receipt_time,
    latest_end_lsn
FROM pg_stat_wal_receiver;
