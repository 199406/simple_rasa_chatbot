import sqlite3


class DatabaseUtility:
    @staticmethod
    def create_connection(db_path="chatbot_db/testdatabase.db"):
        """Create and return a database connection."""
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except sqlite3.Error as error:
            print(f"Error connecting to database: {error}")
            return None

    @staticmethod
    def execute_query(conn, query, params=()):
        """Execute a query and return the results."""
        try:
            cur = conn.cursor()
            cur.execute(query, params)
            results = cur.fetchall()
            return results
        except sqlite3.Error as error:
            print(f"Error executing query: {error}")
            return None



