import sqlite3

class DbController():
    def __init__(self):
        # Connect to or create the database file
        self._conn = sqlite3.connect("mydatabase.db", check_same_thread=False)
        # Create a cursor object to execute SQL commands
        self._cursor = self._conn.cursor()

    def drop_table(self, table_name = "tbl"):
        # drop table
        self._cursor.execute(f"DROP TABLE {table_name}")

    def create_table(self, table_name = "tbl"):
        # Create a table to store data
        self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            contract TEXT PRIMARY KEY,
            entered_date TEXT,
            last_updated_date TEXT
            )""")

    def run_dml(self, dml):
        self._cursor.execute(dml)
        self._conn.commit()

    def run_query(self, query):
        results = self._cursor.execute(query).fetchone()
        return results
    
    def close_conn(self):
        # Close the connection
        self._conn.close()

if __name__ == "__main__":
    dbc = DbController()
    dbc.create_table()
    dbc.run_query("insert into tbl values('AAPL/STK/USD','2023-01-01','2023-02-10')")
    dbc._conn.commit()
