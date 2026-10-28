import pandas as pd

class ConcurrencyControlEngine:
    """
    Compares Optimistic Concurrency Control (OCC) vs Pessimistic Concurrency Control (PCC).
    """

    COMPARISON_MATRIX = [
        {
            "Aspect": "Locking Mechanism",
            "Pessimistic (PCC)": "Eager locking (`SELECT ... FOR UPDATE`) upon read. Blocks competitors.",
            "Optimistic (OCC)": "No read locks. Validates version/timestamp at write time (`WHERE version = v`)."
        },
        {
            "Aspect": "Deadlock Risk",
            "Pessimistic (PCC)": "High risk if multiple resources are locked in different orders.",
            "Optimistic (OCC)": "Zero deadlock risk during read phase (locks only held momentarily during atomic update)."
        },
        {
            "Aspect": "Throughput in Low Contention",
            "Pessimistic (PCC)": "Moderate (lock acquisition and release overhead on every read/write).",
            "Optimistic (OCC)": "Maximum throughput (lock-free reads, no blocking)."
        },
        {
            "Aspect": "Behavior in High Contention",
            "Pessimistic (PCC)": "Transactions queue sequentially; high wait times but zero wasted work.",
            "Optimistic (OCC)": "High rollback/retry rates; transactions waste CPU aborting and retrying."
        },
        {
            "Aspect": "Best Fit Use Case",
            "Pessimistic (PCC)": "High-conflict transactions, financial ledgers, ticket reservations for scarce inventory.",
            "Optimistic (OCC)": "Web forms, student profile updates, catalog browsing, low-conflict writes."
        }
    ]

    @staticmethod
    def get_comparison_df():
        return pd.DataFrame(ConcurrencyControlEngine.COMPARISON_MATRIX)

    @staticmethod
    def simulate_race(strategy: str, total_seats: int = 1):
        """
        Simulates two concurrent students (Student A and Student B) trying to claim the last seat in CS205.
        """
        logs = []

        if strategy == "Pessimistic (SELECT ... FOR UPDATE)":
            logs.append({"Step": 1, "Actor": "Student A", "Action": "BEGIN; SELECT seats_left FROM courses WHERE code = 'CS205' FOR UPDATE;", "Result": "Acquired Exclusive Row Lock. seats_left = 1."})
            logs.append({"Step": 2, "Actor": "Student B", "Action": "BEGIN; SELECT seats_left FROM courses WHERE code = 'CS205' FOR UPDATE;", "Result": "⏳ BLOCKED: Student B waits for lock held by Student A."})
            logs.append({"Step": 3, "Actor": "Student A", "Action": "UPDATE courses SET seats_left = seats_left - 1 WHERE code = 'CS205'; COMMIT;", "Result": "Seats becomes 0. Lock released. Student A enrolled!"})
            logs.append({"Step": 4, "Actor": "Student B", "Action": "Lock granted! Reads updated row: seats_left = 0;", "Result": "Evaluates: No seats left! ROLLBACK. Clean rejection without collision."})
            summary = "🔒 PESSIMISTIC SUCCESS: Student A locked the seat first. Student B cleanly waited and observed 0 seats remaining. No conflicting updates occurred."

        else: # Optimistic Concurrency Control (OCC)
            logs.append({"Step": 1, "Actor": "Student A", "Action": "SELECT seats_left, version FROM courses WHERE code = 'CS205'; -- No lock taken", "Result": "Reads seats_left = 1, version = 10."})
            logs.append({"Step": 2, "Actor": "Student B", "Action": "SELECT seats_left, version FROM courses WHERE code = 'CS205'; -- No lock taken", "Result": "Reads seats_left = 1, version = 10 simultaneously!"})
            logs.append({"Step": 3, "Actor": "Student A", "Action": "UPDATE courses SET seats_left = 0, version = 11 WHERE code = 'CS205' AND version = 10;", "Result": "✅ SUCCESS: 1 row affected. Student A booked seat!"})
            logs.append({"Step": 4, "Actor": "Student B", "Action": "UPDATE courses SET seats_left = 0, version = 11 WHERE code = 'CS205' AND version = 10;", "Result": "❌ CONFLICT DETECTED: 0 rows affected! (version is now 11, expected 10)."})
            logs.append({"Step": 5, "Actor": "Student B", "Action": "OCC Retry Logic: Re-read course state", "Result": "Re-reads: seats_left = 0. Seat no longer available. Aborts retry."})
            summary = "⚡ OPTIMISTIC SUCCESS: Both read lock-free. Student A committed first, incrementing version to 11. Student B's conditional update failed safely because version mismatch was caught!"

        return pd.DataFrame(logs), summary
