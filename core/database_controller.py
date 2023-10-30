import sqlite3
import time


class DatabaseController:
    def __init__(self, db_name, paths_table_name, previous_state_table_name):
        self.db_name = db_name
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name

        # Initialize the database connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        # Create a table in the database with two columns, including the button_identifier column
        query = (f'CREATE TABLE IF NOT EXISTS {self.paths_table_name}'
                 f' (id INTEGER PRIMARY KEY, button_identifier TEXT, path TEXT)')
        self.cursor.execute(query)

        # Create a table in the database with three columns, for the prev condition of folder
        time.sleep(0.1)
        query2 = (f'CREATE TABLE IF NOT EXISTS {self.previous_state_table_name}'
                  f' (id INTEGER PRIMARY KEY, dir_path TEXT, file_names TEXT)')
        self.cursor.execute(query2)

    def entry_exists(self, table_name, condition_name, condition):
        # Check if an entry with the specified button identifier exists
        query = f"SELECT * FROM {table_name} WHERE {condition_name} = ?"
        self.cursor.execute(query, (condition,))
        data = self.cursor.fetchone()
        return data is not None

    def update_entry(self, table_name, condition1_name, condition2_name, condition1, new_path):
        # Update the entry with the new path
        query = f"UPDATE {table_name} SET {condition2_name} = ? WHERE {condition1_name} = ?"
        self.cursor.execute(query, (new_path, condition1))
        self.connection.commit()

    def insert_data(self, table_name, condition1_name, condition2_name, condition1, data):
        # Insert data into the database
        query = f'INSERT INTO {table_name} ({condition1_name}, {condition2_name}) VALUES (?, ?)'
        self.cursor.execute(query, (condition1, data))
        self.connection.commit()

    def retrieve_data(self, table_name):
        # Retrieve data from the database
        query = f'SELECT * FROM {table_name}'
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # print(*data, sep='\n')
        return data

    def delete_all_data(self, table_name):
        # Delete all records from the table
        query = f'DELETE FROM {table_name}'
        self.cursor.execute(query)
        self.connection.commit()

    def close_connection(self):
        # Close the database connection
        self.connection.close()
