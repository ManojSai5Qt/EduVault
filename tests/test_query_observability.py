import unittest
from unittest.mock import patch

from database import postgres_db


class QuerySafetyTests(unittest.TestCase):
    def test_fetch_dataframe_rejects_write_statements(self):
        with self.assertRaises(ValueError):
            postgres_db.fetch_dataframe("DELETE FROM students")

    def test_readonly_helper_rejects_write_statements(self):
        with self.assertRaises(ValueError):
            postgres_db.execute_readonly("UPDATE students SET student_name='x'")

    def test_explain_rejects_ddl(self):
        with self.assertRaises(ValueError):
            postgres_db.explain_query("CREATE INDEX idx_x ON students(student_id)")

    def test_explain_uses_actual_readonly_plan_endpoint(self):
        expected = {"Plan": {"Node Type": "Index Scan"}}
        with patch("database.postgres_db.execute_readonly",
                   return_value=[{"QUERY PLAN": [expected]}]) as execute:
            result = postgres_db.explain_query("SELECT student_id FROM students WHERE student_id = 1")
        self.assertEqual(result, expected)
        execute.assert_called_once()
        self.assertIn("EXPLAIN (BUFFERS, VERBOSE, FORMAT JSON)", execute.call_args.args[0])

    def test_index_identifiers_are_validated_before_connecting(self):
        with self.assertRaises(ValueError):
            postgres_db.create_index_concurrently("bad-name", "students", ["student_id"])


if __name__ == "__main__":
    unittest.main()
