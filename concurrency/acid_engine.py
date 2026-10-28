import pandas as pd
from datetime import datetime

class ACIDTransactionEngine:
    """
    Simulates database ACID properties within the EduVault academic domain.
    Covers:
      - Atomicity: All-or-nothing execution, savepoints, rollback mechanics.
      - Consistency: Integrity constraints (foreign keys, CHECK constraints, balance >= 0).
      - Isolation: Concurrent visibility barriers.
      - Durability: Write-Ahead Logging (WAL) and checkpoint flushing.
    """

    def __init__(self):
        self.reset_state()

    def reset_state(self):
        self.students = {
            1: {"name": "Aarav Sharma", "balance": 1500, "enrolled_courses": ["CS101"], "prereqs_met": True},
            2: {"name": "Ananya Reddy", "balance": 400, "enrolled_courses": [], "prereqs_met": False},
            3: {"name": "Vikram Das", "balance": 2500, "enrolled_courses": ["CS101"], "prereqs_met": True}
        }
        self.courses = {
            "CS205": {"name": "Advanced PostgreSQL & MVCC", "fee": 600, "seats_left": 1, "prereq": "CS101"}
        }
        self.wal_buffer = []
        self.flushed_wal = []
        self.checkpoints = []

    def run_enrollment_transaction(self, student_id: int, course_code: str, simulate_failure_at: str = "none", use_savepoints: bool = False):
        """
        Executes a multi-step student enrollment transaction:
          Step 1: Check prerequisite & eligibility
          Step 2: Deduct course fee from student wallet balance
          Step 3: Reserve seat in course (seats_left - 1)
          Step 4: Record enrollment
          Step 5: Commit & flush WAL
        """
        logs = []
        tx_id = f"TXN-{datetime.now().strftime('%H%M%S%f')[:10]}"
        logs.append({"step": "BEGIN TRANSACTION", "tx_id": tx_id, "status": "ACTIVE", "detail": f"Started transaction for student {student_id} into {course_code}"})

        student = self.students.get(student_id)
        course = self.courses.get(course_code)

        if not student or not course:
            logs.append({"step": "ABORT", "tx_id": tx_id, "status": "FAILED", "detail": "Invalid student or course identifier."})
            return False, logs

        initial_balance = student["balance"]
        initial_seats = course["seats_left"]
        initial_enrollments = list(student["enrolled_courses"])

        try:
            # Step 1: Prerequisite Check
            logs.append({"step": "STEP 1: Prerequisite Check", "tx_id": tx_id, "status": "RUNNING", "detail": f"Checking if {student['name']} completed prerequisite: {course['prereq']}"})
            if simulate_failure_at == "prereq" or (course["prereq"] not in student["enrolled_courses"] and not student["prereqs_met"]):
                raise ValueError(f"Consistency Violation: Prerequisite '{course['prereq']}' not completed by student.")

            if use_savepoints:
                logs.append({"step": "SAVEPOINT sp_eligibility", "tx_id": tx_id, "status": "SAVEPOINT", "detail": "Created Savepoint 'sp_eligibility'"})

            # Step 2: Balance Check & Deduction
            logs.append({"step": "STEP 2: Balance Deduction", "tx_id": tx_id, "status": "RUNNING", "detail": f"Deducting course fee ${course['fee']} from balance ${student['balance']}"})
            if simulate_failure_at == "balance" or student["balance"] < course["fee"]:
                raise ValueError(f"Consistency Violation: Insufficient balance (${student['balance']}) for fee (${course['fee']}). CHECK (balance >= 0) violated.")
            
            student["balance"] -= course["fee"]
            self.wal_buffer.append(f"{tx_id}: UPDATE students SET balance = {student['balance']} WHERE id = {student_id}")

            if use_savepoints:
                logs.append({"step": "SAVEPOINT sp_payment", "tx_id": tx_id, "status": "SAVEPOINT", "detail": "Created Savepoint 'sp_payment'"})

            # Step 3: Seat Availability Check & Decrement
            logs.append({"step": "STEP 3: Course Seat Allocation", "tx_id": tx_id, "status": "RUNNING", "detail": f"Reserving seat in {course_code} (Currently available: {course['seats_left']})"})
            if simulate_failure_at == "seats" or course["seats_left"] <= 0:
                raise ValueError("Consistency Violation: Course is at maximum capacity! CHECK (seats_left > 0) violated.")
            
            course["seats_left"] -= 1
            self.wal_buffer.append(f"{tx_id}: UPDATE courses SET seats_left = {course['seats_left']} WHERE code = '{course_code}'")

            # Step 4: Record Enrollment
            logs.append({"step": "STEP 4: Record Enrollment", "tx_id": tx_id, "status": "RUNNING", "detail": f"Adding {course_code} to student active enrollments"})
            if simulate_failure_at == "crash":
                raise SystemError("Simulated Node/Power Failure right before COMMIT! WAL buffer not fsynced.")

            student["enrolled_courses"].append(course_code)
            self.wal_buffer.append(f"{tx_id}: INSERT INTO enrollments (student_id, course_code) VALUES ({student_id}, '{course_code}')")

            # Step 5: COMMIT & WAL FLUSH (Durability)
            self.flushed_wal.extend(self.wal_buffer)
            self.wal_buffer.clear()
            logs.append({"step": "COMMIT TRANSACTION", "tx_id": tx_id, "status": "COMMITTED", "detail": f"Transaction committed successfully! WAL fsynced to disk for durability."})
            return True, logs

        except Exception as ex:
            # ATOMICITY ROLLBACK
            student["balance"] = initial_balance
            course["seats_left"] = initial_seats
            student["enrolled_courses"] = initial_enrollments
            self.wal_buffer.clear()
            logs.append({"step": "ROLLBACK", "tx_id": tx_id, "status": "ROLLED_BACK", "detail": f"Atomicity Enforced: State fully restored. Error: {str(ex)}"})
            return False, logs

    def get_state_summary(self):
        s_data = []
        for sid, s in self.students.items():
            s_data.append({
                "Student ID": sid,
                "Name": s["name"],
                "Wallet Balance ($)": s["balance"],
                "Enrolled Courses": ", ".join(s["enrolled_courses"]) if s["enrolled_courses"] else "None",
                "Prereq Met": "Yes" if s["prereqs_met"] else "No"
            })
        c_data = []
        for code, c in self.courses.items():
            c_data.append({
                "Course Code": code,
                "Course Name": c["name"],
                "Fee ($)": c["fee"],
                "Seats Left": c["seats_left"],
                "Prerequisite": c["prereq"]
            })
        return pd.DataFrame(s_data), pd.DataFrame(c_data)
