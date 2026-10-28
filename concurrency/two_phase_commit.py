import pandas as pd

class TwoPhaseCommitEngine:
    """
    Simulates Distributed Two-Phase Commit (2PC) protocol across heterogeneous/sharded nodes:
      - Coordinator Node
      - Participant 1: PostgreSQL Core Node (Academic records & tuition billing)
      - Participant 2: MongoDB Learning Activity Cluster (Activity logs & course assets)
    """

    def __init__(self):
        self.participants = ["PostgreSQL Core Node", "MongoDB Activity Cluster"]

    def run_2pc_transaction(self, participant_failure: str = "none"):
        logs = []
        gid = "eduvault_tx_88192"

        # Phase 1: Prepare
        logs.append({"Phase": "PHASE 1: PREPARE", "Actor": "Coordinator", "Action": f"Broadcast PREPARE request for Global ID: {gid}", "Result": "Dispatched"})

        all_agreed = True
        votes = {}

        for p in self.participants:
            if participant_failure == p:
                votes[p] = "VOTE_ABORT"
                all_agreed = False
                logs.append({
                    "Phase": "PHASE 1: PREPARE", "Actor": p,
                    "Action": f"Execute local logic; verify constraints for {gid}",
                    "Result": "❌ FAILED (Network timeout or Constraint violation) -> VOTE_ABORT"
                })
            else:
                votes[p] = "VOTE_COMMIT"
                logs.append({
                    "Phase": "PHASE 1: PREPARE", "Actor": p,
                    "Action": f"PREPARE TRANSACTION '{gid}'; acquire locks, flush prepare WAL to durable storage",
                    "Result": "✅ SUCCESS -> VOTE_COMMIT (In-Doubt / Prepared State)"
                })

        # Coordinator Decision
        if all_agreed:
            decision = "GLOBAL_COMMIT"
            logs.append({"Phase": "DECISION POINT", "Actor": "Coordinator", "Action": "All participants voted YES. Log GLOBAL_COMMIT to coordinator durable log.", "Result": "DECISION: COMMIT"})
            # Phase 2: Commit
            for p in self.participants:
                logs.append({
                    "Phase": "PHASE 2: COMMIT", "Actor": p,
                    "Action": f"COMMIT PREPARED '{gid}'; release row and table locks, mark transaction committed",
                    "Result": "✅ COMMITTED"
                })
            summary = "🎉 2PC TRANSACTION COMMITTED: Distributed consistency achieved across both PostgreSQL and MongoDB!"
            success = True
        else:
            decision = "GLOBAL_ABORT"
            logs.append({"Phase": "DECISION POINT", "Actor": "Coordinator", "Action": "One or more participants voted ABORT. Log GLOBAL_ABORT to coordinator durable log.", "Result": "DECISION: ABORT"})
            # Phase 2: Abort
            for p in self.participants:
                logs.append({
                    "Phase": "PHASE 2: ROLLBACK", "Actor": p,
                    "Action": f"ROLLBACK PREPARED '{gid}'; undo local changes, release acquired locks",
                    "Result": "🔄 ROLLED BACK"
                })
            summary = "⚠️ 2PC TRANSACTION ABORTED: Atomic rollback guaranteed across all participating nodes. No partial writes!"
            success = False

        return pd.DataFrame(logs), summary, success
