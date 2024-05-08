# -*- coding: windows-1251 -*-
import sqlite3
import time


class DatabaseController:
    """
    This class is responsible for all database related operations.
    """
    def __init__(self, db_name, paths_table_name, previous_state_table_name):
        """
        Initialize the DatabaseController.
        :param str db_name: The name of the database.
        :param str paths_table_name: The name of the table for paths.
        :param str previous_state_table_name: The name of the table for previous state information.
        """
        self.db_name = db_name
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name
        self.connection = None
        self.cursor = None

        self._initialize_connection()

    # ------------------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------------------
    def _initialize_connection(self):
        """
        Initialize the database connection and cursor.
        :return: None
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def _execute_query(self, query, params=None):
        """
        Execute a query with optional parameters.
        :param str query: The SQL query.
        :param tuple params: Optional parameters for the query.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {query}\nError: {e}")

    def _fetch_one(self, query, params=None):
        """
        Fetch one row from the database.
        :param str query: The SQL query.
        :param tuple params: Optional parameters for the query.
        :return: The fetched row.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def _fetch_all(self, query):
        """
        Fetch all rows from the database.

        :param str query: The SQL query.
        :return: All fetched rows.
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []

    # ------------------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------------------
    def retrieve_all_data_from_a_table(self, table_name):
        """
        Retrieve all data from the given table.
        :param str table_name: The name of the table to retrieve data from.
        :return: All data from the given table.
        """
        query = f'SELECT * FROM {table_name}'
        return self._fetch_all(query)

    def does_entry_exist(self, table_name, column_name, column_value):
        """
        Check if an entry with the specified condition exists in the given table.
        :param str table_name: The name of the table to search.
        :param str column_name: The name of the column to check against.
        :param column_value: The value to check for in the specified column.
        :return: True if an entry exists, False otherwise.
        :rtype: bool
        """
        query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
        return self._fetch_one(query, (column_value,)) is not None

    def update_entry(self, table_name, condition_column_name, condition_value, new_path_column_name, new_path_value):
        """
        Update the entry in the specified table with the new path.
        :param str table_name: The name of the table to update.
        :param str condition_column_name: The name of the column to use for the condition.
        :param condition_value: The value in the condition column to identify the entry.
        :param str new_path_column_name: The name of the column to update with the new path.
        :param new_path_value: The new path to set in the specified column.
        """
        query = f"UPDATE {table_name} SET {new_path_column_name} = ? WHERE {condition_column_name} = ?"
        self._execute_query(query, (new_path_value, condition_value))

        # check if the update was successful
        if not self.does_entry_exist(table_name, condition_column_name, condition_value):
            print(f"Update failed for {condition_value} in {table_name}")

    def insert_data(self, table_name, column1_name, column2_name, column1_value, data):
        """
        Insert a new entry into the specified table.
        :param str table_name: The name of the table to insert data into.
        :param str column1_name: The name of the first column.
        :param str column2_name: The name of the second column.
        :param column1_value: The value for the first column.
        :param data: The data to be inserted into the second column.
        """
        query = f'INSERT INTO {table_name} ({column1_name}, {column2_name}) VALUES (?, ?)'
        self._execute_query(query, (column1_value, data))

    def create_the_2_predefined_tables(self):
        """
        Create the two predefined tables in the database.
        Create a table in the database with two columns, including the button_identifier column.
        Create a table in the database with three columns, for the prev condition of the folder.
        :return: None
        """
        query1 = (f'CREATE TABLE IF NOT EXISTS {self.paths_table_name}'
                  f' (id INTEGER PRIMARY KEY, button_identifier TEXT, path TEXT)')

        query2 = (f'CREATE TABLE IF NOT EXISTS {self.previous_state_table_name}'
                  f' (id INTEGER PRIMARY KEY, dir_path TEXT, file_names TEXT)')
        self._execute_query(query1)
        time.sleep(0.1)
        self._execute_query(query2)

    def delete_all_data(self, table_name):
        """
        Delete all data from the given table.
        :param str table_name: The name of the table to delete data from.
        """
        query = f'DELETE FROM {table_name}'
        self._execute_query(query)

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
