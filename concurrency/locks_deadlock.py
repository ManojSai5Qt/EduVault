import pandas as pd

class LocksAndDeadlockEngine:
    """
    Manages PostgreSQL Locks, Advisory Locks, and Deadlock Detection/Resolution simulations.
    """

    ROW_LOCKS_INFO = [
        {"Lock Mode": "FOR KEY SHARE", "Acquired By": "Foreign Key checks", "Blocks": "FOR UPDATE", "Allows": "SELECT, FOR NO KEY UPDATE, FOR SHARE, FOR KEY SHARE"},
        {"Lock Mode": "FOR SHARE", "Acquired By": "SELECT ... FOR SHARE", "Blocks": "UPDATE, DELETE, FOR UPDATE, FOR NO KEY UPDATE", "Allows": "SELECT, FOR SHARE, FOR KEY SHARE"},
        {"Lock Mode": "FOR NO KEY UPDATE", "Acquired By": "UPDATE (non-key columns)", "Blocks": "UPDATE, DELETE, FOR UPDATE, FOR NO KEY UPDATE, FOR SHARE", "Allows": "SELECT, FOR KEY SHARE"},
        {"Lock Mode": "FOR UPDATE", "Acquired By": "SELECT ... FOR UPDATE, DELETE, UPDATE (key columns)", "Blocks": "ALL other row lock modes & concurrent updates", "Allows": "Unadorned SELECT (via MVCC)"},
    ]

    TABLE_LOCKS_INFO = [
        {"Lock Mode": "ACCESS SHARE", "Typical SQL": "SELECT", "Conflicting Modes": "ACCESS EXCLUSIVE"},
        {"Lock Mode": "ROW SHARE", "Typical SQL": "SELECT ... FOR UPDATE / FOR SHARE", "Conflicting Modes": "EXCLUSIVE, ACCESS EXCLUSIVE"},
        {"Lock Mode": "ROW EXCLUSIVE", "Typical SQL": "INSERT, UPDATE, DELETE", "Conflicting Modes": "SHARE, SHARE ROW EXCL, EXCLUSIVE, ACCESS EXCL"},
        {"Lock Mode": "SHARE UPDATE EXCLUSIVE", "Typical SQL": "VACUUM, ANALYZE, CREATE INDEX CONCURRENTLY", "Conflicting Modes": "SHARE UPDATE EXCL, SHARE, SHARE ROW EXCL, EXCLUSIVE, ACCESS EXCL"},
        {"Lock Mode": "SHARE", "Typical SQL": "CREATE INDEX", "Conflicting Modes": "ROW EXCLUSIVE, SHARE UPDATE EXCL, SHARE ROW EXCL, EXCLUSIVE, ACCESS EXCL"},
        {"Lock Mode": "ACCESS EXCLUSIVE", "Typical SQL": "ALTER TABLE, DROP TABLE, TRUNCATE, VACUUM FULL", "Conflicting Modes": "ALL OTHER MODES (Complete Table Lock)"},
    ]

    ADVISORY_LOCKS_INFO = [
        {"Type": "Session-Level Advisory Lock", "Acquire SQL": "SELECT pg_advisory_lock(42);", "Release SQL": "SELECT pg_advisory_unlock(42);", "Scope": "Remains held until explicitly released or database session disconnects."},
        {"Type": "Transaction-Level Advisory Lock", "Acquire SQL": "SELECT pg_advisory_xact_lock(42);", "Release SQL": "Automatic on COMMIT / ROLLBACK", "Scope": "Automatically released when current transaction ends."},
        {"Type": "Non-Blocking Try Lock", "Acquire SQL": "SELECT pg_try_advisory_lock(42);", "Release SQL": "SELECT pg_advisory_unlock(42);", "Scope": "Returns immediately with TRUE if acquired or FALSE if busy without blocking."},
    ]

    @staticmethod
    def get_row_locks_df():
        return pd.DataFrame(LocksAndDeadlockEngine.ROW_LOCKS_INFO)

    @staticmethod
    def get_table_locks_df():
        return pd.DataFrame(LocksAndDeadlockEngine.TABLE_LOCKS_INFO)

    @staticmethod
    def get_advisory_locks_df():
        return pd.DataFrame(LocksAndDeadlockEngine.ADVISORY_LOCKS_INFO)

    @staticmethod
    def simulate_deadlock(strategy: str = "detect_and_abort"):
        """
        Simulates two concurrent transactions competing for two student balance records:
          Resource A: Student #101
          Resource B: Student #102
        """
        events = []
        events.append({"Step": 1, "Time": "T0", "Tx": "TX-1", "Action": "BEGIN; UPDATE student_wallets SET balance = balance - 100 WHERE student_id = 101;", "State": "Acquired Exclusive Row Lock on Student #101"})
        events.append({"Step": 2, "Time": "T1", "Tx": "TX-2", "Action": "BEGIN; UPDATE student_wallets SET balance = balance - 150 WHERE student_id = 102;", "State": "Acquired Exclusive Row Lock on Student #102"})

        if strategy == "prevent_ordered_locking":
            events.append({"Step": 3, "Time": "T2", "Tx": "TX-1", "Action": "UPDATE student_wallets SET balance = balance + 100 WHERE student_id = 102;", "State": "Strict Lock Ordering: TX-1 and TX-2 acquire locks in ascending order (101 then 102). TX-2 waits cleanly without cycle."})
            events.append({"Step": 4, "Time": "T3", "Tx": "TX-1", "Action": "COMMIT;", "State": "TX-1 finishes, releases locks. TX-2 proceeds smoothly."})
            summary = "✅ DEADLOCK PREVENTED: By enforcing a global lock acquisition order (lock smaller student_id first), cyclic dependency cannot form!"
            return pd.DataFrame(events), summary, False

        # Cyclic deadlock scenario
        events.append({"Step": 3, "Time": "T2", "Tx": "TX-1", "Action": "UPDATE student_wallets SET balance = balance + 100 WHERE student_id = 102;", "State": "⏳ TX-1 BLOCKED: Waiting for Row Lock on Student #102 (held by TX-2)"})
        events.append({"Step": 4, "Time": "T3", "Tx": "TX-2", "Action": "UPDATE student_wallets SET balance = balance + 150 WHERE student_id = 101;", "State": "⏳ TX-2 BLOCKED: Waiting for Row Lock on Student #101 (held by TX-1)"})
        events.append({"Step": 5, "Time": "T3 + 1000ms", "Tx": "PG Lock Manager", "Action": "deadlock_timeout expired! Evaluated Wait-For Graph: [TX-1 -> TX-2 -> TX-1] Cycle detected!", "State": "💥 DEADLOCK CONFIRMED"})
        events.append({"Step": 6, "Time": "T4", "Tx": "PG Resolver", "Action": "ABORT TX-2 with: ERROR: deadlock detected (SQLSTATE 40P01)", "State": "TX-2 rolled back. Locks released. TX-1 unblocks and commits."})

        summary = "💥 DEADLOCK RESOLVED: PostgreSQL detected cycle in the Wait-For Graph (WFG) after `deadlock_timeout` (1s default). It aborted the younger/cheaper transaction (TX-2) allowing TX-1 to complete."
        return pd.DataFrame(events), summary, True
