import pandas as pd

class IsolationSimulator:
    """
    Simulates SQL transaction isolation levels and concurrency anomalies in PostgreSQL.
    Levels:
      1. Read Uncommitted
      2. Read Committed (PostgreSQL Default)
      3. Repeatable Read
      4. Serializable
    Anomalies:
      - Dirty Read: Transaction reads uncommitted data from another concurrent transaction.
      - Non-Repeatable Read: Re-reading the same row returns modified data committed by another transaction.
      - Phantom Read: Re-executing a range query returns newly inserted rows committed by another transaction.
      - Serialization Anomaly / Write Skew: Concurrent transactions produce an invalid state that could not have occurred serially.
    """

    ISOLATION_MATRIX = [
        {"Isolation Level": "Read Uncommitted", "Dirty Read": "Permitted (ANSI) / Prevented (PG)", "Non-Repeatable Read": "Permitted", "Phantom Read": "Permitted", "Serialization Anomaly": "Permitted"},
        {"Isolation Level": "Read Committed (PG Default)", "Dirty Read": "Prevented", "Non-Repeatable Read": "Permitted", "Phantom Read": "Permitted", "Serialization Anomaly": "Permitted"},
        {"Isolation Level": "Repeatable Read", "Dirty Read": "Prevented", "Non-Repeatable Read": "Prevented", "Phantom Read": "Prevented (in PG via Snapshot)", "Serialization Anomaly": "Permitted (Write Skew)"},
        {"Isolation Level": "Serializable (SSI)", "Dirty Read": "Prevented", "Non-Repeatable Read": "Prevented", "Phantom Read": "Prevented", "Serialization Anomaly": "Prevented (SIREAD locks)"},
    ]

    @staticmethod
    def get_matrix_df():
        return pd.DataFrame(IsolationSimulator.ISOLATION_MATRIX)

    @staticmethod
    def simulate_anomaly(anomaly_type: str, isolation_level: str):
        """
        Simulates step-by-step concurrent execution between Transaction A (T1) and Transaction B (T2).
        Returns timeline events, query text, and explanation.
        """
        timeline = []
        is_pg = True

        if anomaly_type == "Dirty Read":
            # T1 updates grade from 75 to 95, doesn't commit yet. T2 reads. T1 rolls back!
            timeline.append({
                "Step": 1, "Time": "T0", "Transaction": "T1 (Instructor)",
                "Action": "BEGIN; UPDATE grades SET marks = 95 WHERE student_id = 1 AND course_code = 'CS101';",
                "Observed State": "Marks updated in T1 workspace to 95. Not committed."
            })
            if isolation_level == "Read Uncommitted" and not is_pg:
                timeline.append({
                    "Step": 2, "Time": "T1", "Transaction": "T2 (Student / Registrar)",
                    "Action": "SELECT marks FROM grades WHERE student_id = 1 AND course_code = 'CS101';",
                    "Observed State": "❌ DIRTY READ OCCURRED! T2 reads uncommitted value: 95."
                })
            else:
                timeline.append({
                    "Step": 2, "Time": "T1", "Transaction": "T2 (Student / Registrar)",
                    "Action": "SELECT marks FROM grades WHERE student_id = 1 AND course_code = 'CS101';",
                    "Observed State": "✅ SAFE: T2 reads original committed value: 75. (In PostgreSQL, Read Uncommitted acts as Read Committed)."
                })
            timeline.append({
                "Step": 3, "Time": "T2", "Transaction": "T1 (Instructor)",
                "Action": "ROLLBACK; -- Instructor made a mistake!",
                "Observed State": "T1 changes are undone. Marks remain 75."
            })
            explanation = (
                "**Dirty Read**: In ANSI Read Uncommitted, T2 could observe uncommitted data that was subsequently rolled back. "
                "**PostgreSQL Detail**: PostgreSQL does NOT support dirty reads. Even if you specify `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED`, "
                "PostgreSQL transparently treats it as `READ COMMITTED` because MVCC requires every visible tuple to have a committed transaction ID."
            )

        elif anomaly_type == "Non-Repeatable Read":
            # T1 reads row. T2 updates and commits. T1 re-reads row in same transaction.
            timeline.append({
                "Step": 1, "Time": "T0", "Transaction": "T1 (Scholarship Reviewer)",
                "Action": f"BEGIN TRANSACTION ISOLATION LEVEL {isolation_level.upper()};\nSELECT marks FROM grades WHERE student_id = 1;",
                "Observed State": "T1 reads initial marks = 75."
            })
            timeline.append({
                "Step": 2, "Time": "T1", "Transaction": "T2 (Department Head)",
                "Action": "BEGIN;\nUPDATE grades SET marks = 88 WHERE student_id = 1;\nCOMMIT;",
                "Observed State": "T2 commits marks = 88 to the database."
            })
            if isolation_level in ["Read Uncommitted", "Read Committed"]:
                timeline.append({
                    "Step": 3, "Time": "T2", "Transaction": "T1 (Scholarship Reviewer)",
                    "Action": "SELECT marks FROM grades WHERE student_id = 1;",
                    "Observed State": "❌ NON-REPEATABLE READ OCCURRED! T1 now reads marks = 88 within the same transaction!"
                })
                explanation = (
                    "**Non-Repeatable (Fuzzy) Read**: Under `READ COMMITTED`, every SQL statement receives a **new snapshot** of the database taken at query start. "
                    "Thus, T1 sees the modifications committed by T2 between statement 1 and statement 2."
                )
            else:
                timeline.append({
                    "Step": 3, "Time": "T2", "Transaction": "T1 (Scholarship Reviewer)",
                    "Action": "SELECT marks FROM grades WHERE student_id = 1;",
                    "Observed State": "✅ REPEATABLE READ PREVENTED ANOMALY: T1 still reads marks = 75 from its transaction snapshot."
                })
                explanation = (
                    "**Prevented**: Under `REPEATABLE READ` or `SERIALIZABLE`, the transaction snapshot is acquired at the **start of the first query in the transaction**, "
                    "so subsequent queries see the exact same snapshot."
                )

        elif anomaly_type == "Phantom Read":
            # T1 counts rows with filter. T2 inserts matching row and commits. T1 counts again.
            timeline.append({
                "Step": 1, "Time": "T0", "Transaction": "T1 (Dean / Audit)",
                "Action": f"BEGIN TRANSACTION ISOLATION LEVEL {isolation_level.upper()};\nSELECT COUNT(*) FROM enrollments WHERE course_code = 'CS101';",
                "Observed State": "T1 receives count = 25 enrollments."
            })
            timeline.append({
                "Step": 2, "Time": "T1", "Transaction": "T2 (Registrar)",
                "Action": "BEGIN;\nINSERT INTO enrollments (student_id, course_code) VALUES (101, 'CS101');\nCOMMIT;",
                "Observed State": "T2 inserts a 26th student and commits."
            })
            if isolation_level in ["Read Uncommitted", "Read Committed"]:
                timeline.append({
                    "Step": 3, "Time": "T2", "Transaction": "T1 (Dean / Audit)",
                    "Action": "SELECT COUNT(*) FROM enrollments WHERE course_code = 'CS101';",
                    "Observed State": "❌ PHANTOM READ OCCURRED! T1 now counts 26 enrollments! A phantom row appeared."
                })
                explanation = (
                    "**Phantom Read**: A query retrieves a set of rows satisfying a search condition; a second transaction inserts new rows "
                    "satisfying that condition and commits; the first transaction re-executes the query and receives a different set of rows."
                )
            else:
                timeline.append({
                    "Step": 3, "Time": "T2", "Transaction": "T1 (Dean / Audit)",
                    "Action": "SELECT COUNT(*) FROM enrollments WHERE course_code = 'CS101';",
                    "Observed State": "✅ PHANTOM PREVENTED: T1 still sees exactly 25 enrollments. In PostgreSQL, Repeatable Read snapshot isolation prevents phantom reads!"
                })
                explanation = (
                    "**PostgreSQL Highlight**: In the standard SQL spec, `REPEATABLE READ` is only required to prevent non-repeatable reads. "
                    "However, PostgreSQL's `REPEATABLE READ` is implemented via **Snapshot Isolation (SI)**, which freezes the entire table state and **naturally prevents Phantom Reads** too!"
                )

        elif anomaly_type == "Write Skew / Serialization Anomaly":
            # Two TA's proctoring: rule is at least one TA must be on duty. Both check count (2). Both take leave concurrently.
            timeline.append({
                "Step": 1, "Time": "T0", "Transaction": "T1 (TA Alice)",
                "Action": f"BEGIN TRANSACTION ISOLATION LEVEL {isolation_level.upper()};\nSELECT COUNT(*) FROM proctors WHERE status = 'ON_DUTY'; -- returns 2",
                "Observed State": "T1 sees 2 TAs on duty. Constraint is >= 1 on duty. Safe to take leave."
            })
            timeline.append({
                "Step": 2, "Time": "T0+", "Transaction": "T2 (TA Bob)",
                "Action": f"BEGIN TRANSACTION ISOLATION LEVEL {isolation_level.upper()};\nSELECT COUNT(*) FROM proctors WHERE status = 'ON_DUTY'; -- returns 2",
                "Observed State": "T2 also sees 2 TAs on duty. Safe to take leave."
            })
            timeline.append({
                "Step": 3, "Time": "T1", "Transaction": "T1 (TA Alice)",
                "Action": "UPDATE proctors SET status = 'LEAVE' WHERE name = 'Alice';\nCOMMIT;",
                "Observed State": "Alice takes leave. 1 TA remaining."
            })
            if isolation_level != "Serializable":
                timeline.append({
                    "Step": 4, "Time": "T2", "Transaction": "T2 (TA Bob)",
                    "Action": "UPDATE proctors SET status = 'LEAVE' WHERE name = 'Bob';\nCOMMIT;",
                    "Observed State": "❌ WRITE SKEW OCCURRED! Both committed! Now 0 TAs are on duty, violating invariant (>=1)."
                })
                explanation = (
                    "**Write Skew**: Neither transaction read what the other wrote, and neither modified the same row. "
                    "Both transactions satisfied business invariants individually, but their concurrent execution violated the invariant. "
                    "This is permitted in `REPEATABLE READ`!"
                )
            else:
                timeline.append({
                    "Step": 4, "Time": "T2", "Transaction": "T2 (TA Bob)",
                    "Action": "UPDATE proctors SET status = 'LEAVE' WHERE name = 'Bob';\nCOMMIT;",
                    "Observed State": "✅ SERIALIZATION FAILURE DETECTED: PostgreSQL SSI aborts T2 with: ERROR: could not serialize access due to read/write dependencies among transactions (SQLSTATE 40001)."
                })
                explanation = (
                    "**Prevented by PostgreSQL SSI**: Serializable Snapshot Isolation tracks lock dependencies (SIREAD locks) "
                    "and detects dangerous rw-antidependency cycles. It automatically aborts T2 so the application can retry safely."
                )
        else:
            explanation = "Invalid anomaly selection."

        return pd.DataFrame(timeline), explanation
