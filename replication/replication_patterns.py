import pandas as pd

class ReplicationPatternsEngine:
    """
    Simulates database replication topologies and patterns:
      1. Sync vs Async Replication (Latency vs Durability Trade-off)
      2. Single-Leader vs Multi-Leader vs Leaderless
      3. Dynamo-Style Leaderless Quorum Consistency (W + R > N)
    """

    PATTERNS_OVERVIEW = [
        {
            "Pattern": "Synchronous Single-Leader",
            "Write Path": "Primary flushes WAL and waits for Standby confirmation before responding to client.",
            "RPO (Data Loss)": "0 (Zero data loss)",
            "RTO (Recovery Time)": "Fast (Standby is 100% up-to-date)",
            "Write Latency": "High (bound by network RTT)",
            "Failure Impact": "If Standby crashes or disconnects, Primary writes block (or downgrade to async)."
        },
        {
            "Pattern": "Asynchronous Single-Leader (PG Default)",
            "Write Path": "Primary commits locally immediately; WAL sender streams changes in background.",
            "RPO (Data Loss)": "> 0 (Replication lag window can cause data loss on hard failover)",
            "RTO (Recovery Time)": "Fast",
            "Write Latency": "Low (Immediate local commit)",
            "Failure Impact": "Standby downtime has zero impact on primary write throughput."
        },
        {
            "Pattern": "Multi-Leader (Active-Active)",
            "Write Path": "Writes accepted by multiple regional leaders and cross-replicated.",
            "RPO (Data Loss)": "Low (multi-region durability)",
            "RTO (Recovery Time)": "Instant local routing",
            "Write Latency": "Very Low (local write in each region)",
            "Failure Impact": "Requires conflict resolution algorithms (Last-Write-Wins LWW, CRDTs)."
        },
        {
            "Pattern": "Leaderless (Dynamo-Style Quorum)",
            "Write Path": "Client or coordinator sends writes concurrently to N replicas; commits when W agree.",
            "RPO (Data Loss)": "Tunable via Quorum (W + R > N)",
            "RTO (Recovery Time)": "High fault tolerance (no single point of failure)",
            "Write Latency": "Tunable based on W value",
            "Failure Impact": "Tolerates N - W write node failures and N - R read node failures."
        }
    ]

    @staticmethod
    def get_patterns_df():
        return pd.DataFrame(ReplicationPatternsEngine.PATTERNS_OVERVIEW)

    @staticmethod
    def calculate_quorum(n: int, w: int, r: int):
        """
        Calculates consistency guarantees according to quorum rule:
          Strong consistency if W + R > N.
          Tolerated write failures = N - W.
          Tolerated read failures = N - R.
        """
        is_strong = (w + r) > n
        write_fault_tolerance = max(0, n - w)
        read_fault_tolerance = max(0, n - r)

        overlap = (w + r) - n
        status = "[STRONG] Strict Quorum (W + R > N Guaranteed Overlap)" if is_strong else "[WEAK] Eventual Consistency (Weak Quorum - Stale Reads Possible)"

        details = {
            "Total Replicas (N)": n,
            "Write Quorum (W)": w,
            "Read Quorum (R)": r,
            "W + R": w + r,
            "Quorum Status": status,
            "Guaranteed Overlap Nodes": max(0, overlap),
            "Tolerated Failed Nodes during Write": write_fault_tolerance,
            "Tolerated Failed Nodes during Read": read_fault_tolerance,
            "Read Repair Active": "Yes (nodes compare timestamps & update stale replicas)",
            "Anti-Entropy Mechanism": "Merkle Trees & Hinted Handoff"
        }
        return details
