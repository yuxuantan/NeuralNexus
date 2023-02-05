import sqlite3

class DbController():
    def __init__(self):
        # Connect to or create the database file
        self._conn = sqlite3.connect("mydatabase.db")
        # Create a cursor object to execute SQL commands
        self._cursor = self._conn.cursor()

    def drop_table(self, table_name):
        # drop table
        self._cursor.execute(f"DROP TABLE {table_name}")

    def create_table(self, table_name):
        # Create a table to store data
        self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            address TEXT
            )""")


    def insert_into_table(self, table_name, values_csv):
        # Insert data into the table
        self._cursor.execute(f"INSERT INTO {table_name} VALUES ({values_csv})")
        # Save the changes
        self._conn.commit()


    def select_all_from_table(self, table_name):
        # Query the data
        self._cursor.execute(f"SELECT * FROM {table_name}")
        # Fetch all the results
        results = self._cursor.fetchall()
        # Iterate through the results and print them
        for result in results:
            print(result)
    
    def close_conn(self):
        # Close the connection
        self._conn.close()
