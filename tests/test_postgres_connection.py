import unittest
from sql_communicator import get_connection

class TestPostgresConnection(unittest.TestCase):

    def test_connection(self):
        try:
            # Attempt to connect to the PostgreSQL server
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1 as xx;")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1, "PostgreSQL connection test failed.")
        except Exception as e:
            self.fail(f"Connection to PostgreSQL server failed: {e}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()

if __name__ == "__main__":
    unittest.main()