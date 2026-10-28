import hashlib
import pandas as pd

class ShardingEngine:
    """
    Simulates database horizontal sharding architectures:
      1. Hash-based Sharding
      2. Range-based Sharding
      3. List/Directory-based Sharding
      4. Query Routing (Single Shard vs Scatter-Gather)
    """

    def __init__(self, num_shards: int = 3):
        self.num_shards = num_shards
        self.shards = {f"Shard-{i+1} (Node {i+1})": [] for i in range(num_shards)}
        self._populate_demo_data()

    def _populate_demo_data(self):
        sample_students = [
            {"id": 101, "name": "Aarav Sharma", "year": 2024, "dept": "Computer Science"},
            {"id": 102, "name": "Ananya Reddy", "year": 2025, "dept": "Information Technology"},
            {"id": 103, "name": "Arjun Kumar", "year": 2024, "dept": "Computer Science"},
            {"id": 104, "name": "Diya Patel", "year": 2026, "dept": "Electronics"},
            {"id": 105, "name": "Ishaan Verma", "year": 2025, "dept": "Computer Science"},
            {"id": 106, "name": "Kavya Rao", "year": 2024, "dept": "Information Technology"},
            {"id": 107, "name": "Rahul Singh", "year": 2026, "dept": "Electrical"},
            {"id": 108, "name": "Priya Gupta", "year": 2025, "dept": "Computer Science"},
            {"id": 109, "name": "Sneha Naidu", "year": 2024, "dept": "Electronics"},
            {"id": 110, "name": "Vikram Das", "year": 2026, "dept": "Mechanical"},
        ]
        self.students = sample_students

    def route_hash(self, key_val: int):
        """
        MD5 hash modulo num_shards
        """
        h = int(hashlib.md5(str(key_val).encode()).hexdigest(), 16)
        shard_idx = (h % self.num_shards) + 1
        return f"Shard-{shard_idx} (Node {shard_idx})"

    def route_range(self, year: int):
        """
        Range sharding based on student admission year
        """
        if year <= 2024:
            return "Shard-1 (Node 1) [<= 2024]"
        elif year == 2025:
            return "Shard-2 (Node 2) [2025]"
        else:
            return "Shard-3 (Node 3) [>= 2026]"

    def route_directory(self, dept: str):
        """
        List/Directory sharding based on academic department
        """
        dept_lower = dept.lower()
        if "computer" in dept_lower or "information" in dept_lower:
            return "Shard-1 (Node 1) [Computing & IT]"
        elif "electron" in dept_lower or "electr" in dept_lower:
            return "Shard-2 (Node 2) [Circuits & Hardware]"
        else:
            return "Shard-3 (Node 3) [Core Engineering]"

    def simulate_routing(self, strategy: str):
        routes = []
        for s in self.students:
            if strategy == "Hash-Based (hash(id) % N)":
                dest = self.route_hash(s["id"])
            elif strategy == "Range-Based (Admission Year)":
                dest = self.route_range(s["year"])
            else: # List/Directory
                dest = self.route_directory(s["dept"])

            routes.append({
                "Student ID": s["id"],
                "Student Name": s["name"],
                "Department": s["dept"],
                "Admission Year": s["year"],
                "Target Shard": dest
            })
        return pd.DataFrame(routes)

    def route_query(self, query_type: str, filter_val: str, strategy: str):
        """
        Simulates query router behavior: Directed Point Query vs Scatter-Gather.
        """
        if query_type == "Point Query (with Shard Key)":
            target = self.route_hash(int(filter_val)) if "Hash" in strategy else (self.route_range(int(filter_val)) if "Range" in strategy else self.route_directory(filter_val))
            return {
                "Query": f"SELECT * FROM students WHERE shard_key = '{filter_val}'",
                "Execution Plan": "Single-Shard Direct Route (O(1))",
                "Target Shards Contacted": [target],
                "Scatter-Gather Required": "No",
                "Network Overhead": "Minimal (1 RPC round-trip)",
                "Explanation": f"The query router inspects the WHERE clause, hashes/matches the shard key, and forwards the SQL request directly to {target}."
            }
        else:
            targets = [f"Shard-{i+1} (Node {i+1})" for i in range(self.num_shards)]
            return {
                "Query": "SELECT * FROM students WHERE marks > 90 ORDER BY marks DESC",
                "Execution Plan": "Scatter-Gather Parallel Broadcast",
                "Target Shards Contacted": targets,
                "Scatter-Gather Required": "Yes (All Shards)",
                "Network Overhead": f"High ({self.num_shards} parallel RPCs + Coordinator Merge)",
                "Explanation": "Because the query filter does NOT contain the shard key, the router must broadcast the SQL query to all shards, wait for all partial results, and merge-sort them at the coordinator."
            }
