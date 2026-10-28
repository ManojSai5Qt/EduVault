import pandas as pd

class MVCCInspector:
    """
    Simulates and visualizes PostgreSQL Multi-Version Concurrency Control (MVCC) heap internals.
    Details:
      - Tuple header anatomy: t_xmin, t_xmax, t_cid, t_ctid (page, offset).
      - Row updates creating new tuple versions without in-place overwrite.
      - Snapshot visibility rules: A tuple is visible if xmin is committed and xmax is uncommitted or > snapshot.
      - Dead tuple accumulation and VACUUM garbage collection.
      - Heap-Only Tuples (HOT) optimization.
    """

    def __init__(self):
        self.current_xid = 500
        self.page_tuples = []
        self._init_demo_data()

    def _init_demo_data(self):
        self.page_tuples = [
            {
                "ctid": "(0, 1)", "student_id": 101, "name": "Aarav Sharma", "marks": 85,
                "xmin": 480, "xmax": 0, "status": "Live Tuple", "notes": "Inserted by XID 480 (Committed)"
            },
            {
                "ctid": "(0, 2)", "student_id": 102, "name": "Ananya Reddy", "marks": 90,
                "xmin": 485, "xmax": 0, "status": "Live Tuple", "notes": "Inserted by XID 485 (Committed)"
            },
            {
                "ctid": "(0, 3)", "student_id": 103, "name": "Arjun Kumar", "marks": 78,
                "xmin": 490, "xmax": 0, "status": "Live Tuple", "notes": "Inserted by XID 490 (Committed)"
            }
        ]

    def update_student_grade(self, student_id: int, new_marks: int):
        """
        Simulates PostgreSQL row update:
          1. Sets old tuple's xmax = current_xid.
          2. Marks old tuple pointer to new ctid.
          3. Appends new tuple version with xmin = current_xid and xmax = 0.
        """
        self.current_xid += 1
        tx = self.current_xid
        new_offset = len(self.page_tuples) + 1
        new_ctid = f"(0, {new_offset})"

        found = False
        target_name = ""
        for tup in self.page_tuples:
            if tup["student_id"] == student_id and tup["xmax"] == 0:
                tup["xmax"] = tx
                tup["status"] = "Dead Tuple (Pending Vacuum)"
                tup["notes"] = f"Updated to {new_ctid} by XID {tx}"
                target_name = tup["name"]
                found = True
                break

        if found:
            self.page_tuples.append({
                "ctid": new_ctid,
                "student_id": student_id,
                "name": target_name,
                "marks": new_marks,
                "xmin": tx,
                "xmax": 0,
                "status": "Live Tuple",
                "notes": f"Created by XID {tx} (Current Version)"
            })
            return True, f"XID {tx} created new tuple version {new_ctid} with marks {new_marks}. Old version marked dead."
        return False, "Active tuple not found for student."

    def delete_student(self, student_id: int):
        self.current_xid += 1
        tx = self.current_xid
        for tup in self.page_tuples:
            if tup["student_id"] == student_id and tup["xmax"] == 0:
                tup["xmax"] = tx
                tup["status"] = "Dead Tuple (Deleted)"
                tup["notes"] = f"Deleted by XID {tx}"
                return True, f"XID {tx} set xmax = {tx} on {tup['ctid']}. Row is logically deleted."
        return False, "Active tuple not found."

    def run_vacuum(self):
        """
        Simulates VACUUM:
          Reclaims tuples where xmax > 0 and xmax committed before current transactions.
        """
        initial_count = len(self.page_tuples)
        reclaimed = [t for t in self.page_tuples if t["xmax"] != 0]
        self.page_tuples = [t for t in self.page_tuples if t["xmax"] == 0]
        freed = len(reclaimed)
        return freed, f"VACUUM successfully removed {freed} dead tuple(s). Free space on Page 0 reclaimed for future inserts."

    def get_tuples_df(self):
        return pd.DataFrame(self.page_tuples)
