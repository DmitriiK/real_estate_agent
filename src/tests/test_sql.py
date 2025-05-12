import unittest
from  pprint import pprint
from src.utils.sql_communicator import engine, get_table_metadata, execute_select_query, get_records_by_ids
from sqlalchemy import inspect


class TestSQL(unittest.TestCase):


    def test_list_tables(self):
        try:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            self.assertIsInstance(tables, list, "Failed to retrieve list of tables from the database.")
            print("Tables in the database:", tables)
        except Exception as e:
            self.fail(f"Failed to retrieve tables from the database: {e}")

    def test_get_table_metadata(self):
        table_name = 'v_emlak_data_mart'
        try:
            metadata = get_table_metadata(table_name)
            self.assertIsInstance(metadata, list, "Metadata should be a list.")
            self.assertGreater(len(metadata), 0, "Metadata list should not be empty.")
            expected_keys = {'name', 'type', 'column_description'}
            self.assertTrue(expected_keys.issubset(metadata[0].keys()), "Metadata dictionary is missing expected keys.")
            pprint( metadata, width=40)
        except Exception as e:
            self.fail(f"Failed to retrieve metadata for table '{table_name}': {e}")

    def test_execute_select_query(self):
        query = "SELECT 1 as test_column;"
        try:
            result = execute_select_query(query)
            self.assertIsInstance(result, list, "Result should be a list.")
            self.assertGreater(len(result), 0, "Result list should not be empty.")
            self.assertIn('test_column', result[0], "Result dictionary should contain 'test_column'.")
            self.assertEqual(result[0]['test_column'], 1, "The value of 'test_column' should be 1.")
        except Exception as e:
            self.fail(f"Failed to execute select query: {e}")

    def test_get_records_by_ids(self):
        input_ids = [1, 2, 3]
        try:
            records = get_records_by_ids('v_emlak_data_mart', input_ids)
            self.assertIsInstance(records, list, "Records should be a list.")
            self.assertGreater(len(records), 0, "Records list should not be empty.")
            for record in records:
                self.assertIn('id', record, "Each record should have an 'id' key.")
            retrieved_ids = {record['id'] for record in records}
            self.assertEqual(retrieved_ids, set(input_ids), "The set of 'id' values in records should match the input_ids.")
            print(records)
        except Exception as e:
            self.fail(f"Failed to retrieve records by IDs: {e}")



if __name__ == "__main__":
    unittest.main()