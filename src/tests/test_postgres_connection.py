import unittest
from  pprint import pprint
from text2SQLagent.sql_communicator import engine, get_table_metadata
from sqlalchemy import inspect
from sqlalchemy.sql import text

class TestSQL(unittest.TestCase):

    def test_connection(self):
        try:
            # Attempt to connect to the PostgreSQL server using SQLAlchemy
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1 as xx;")).fetchone()
                self.assertEqual(result[0], 1, "PostgreSQL connection test failed.")
        except Exception as e:
            self.fail(f"Connection to PostgreSQL server failed: {e}")

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
            expected_keys = {'name', 'type', 'comment'}
            self.assertTrue(expected_keys.issubset(metadata[0].keys()), "Metadata dictionary is missing expected keys.")
            pprint( metadata, width=40)
        except Exception as e:
            self.fail(f"Failed to retrieve metadata for table '{table_name}': {e}")

if __name__ == "__main__":
    unittest.main()