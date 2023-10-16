import sqlite3


class DatabaseController:
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name

        # Initialize the database connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        # Create a table in the database with two columns, including the button_identifier column
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY, button_identifier TEXT, path TEXT)'
        self.cursor.execute(query)

    def entry_exists(self, button_identifier):
        # Check if an entry with the specified button identifier exists
        query = f"SELECT * FROM {self.table_name} WHERE button_identifier = ?"
        self.cursor.execute(query, (button_identifier,))
        data = self.cursor.fetchone()
        return data is not None

    def update_entry(self, button_identifier, new_path):
        # Update the entry with the new path
        query = f"UPDATE {self.table_name} SET path = ? WHERE button_identifier = ?"
        self.cursor.execute(query, (new_path, button_identifier))
        self.connection.commit()

    def insert_data(self, button_identifier, data):
        # Insert data into the database
        query = f'INSERT INTO {self.table_name} (button_identifier, path) VALUES (?, ?)'
        self.cursor.execute(query, (button_identifier, data))
        self.connection.commit()

    def retrieve_data(self):
        # Retrieve data from the database
        query = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(*data, sep='\n')
        return data

    def delete_all_data(self):
        # Delete all records from the table
        query = f'DELETE FROM {self.table_name}'
        self.cursor.execute(query)
        self.connection.commit()

    def close_connection(self):
        # Close the database connection
        self.connection.close()
