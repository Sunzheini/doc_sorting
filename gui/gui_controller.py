# -*- coding: utf-8 -*-
import os
from tkinter import filedialog
from tkinter import *
from tkinter import font
from tkinter import scrolledtext

from gui.default_status_text import default_status_text
from support.decorators import time_measurement_decorator
from gui.front_end_settings import (roboto_font_family, roboto_font_size,
                                    apply_the_front_end_settings, apply_the_browse_buttons,
                                    apply_the_browse_labels, apply_the_shortcut_buttons, apply_the_work_buttons,
                                    apply_light_next_to_work_buttons,
                                    name_of_browse_label1, name_of_browse_label2, name_of_browse_label3,
                                    name_of_browse_label4, name_of_browse_button1, name_of_browse_button2,
                                    name_of_browse_button3, name_of_browse_button4, name_of_button1,
                                    name_of_button2, name_of_button3, name_of_shortcut_button)
from core.global_error_handler import GlobalErrorHandler


class MyGui:
    """
    This class is responsible for the GUI of the application.
    """
    DEFAULT_STATUS_TEXT = default_status_text
    FONT_FAMILY = roboto_font_family
    FONT_SIZE = roboto_font_size

    def __init__(
            self,
            engine_object,                                  # responsible for the logic of the application
            db_object,                                      # responsible for the database
            default_path_for_ready_after_project_name,      # see main.py
            default_path_for_finished_after_project_name,   # see main.py
            default_path_for_excel_after_project_name,      # see main.py
            paths_table_name,                               # see main.py
            previous_state_table_name,                      # see main.py
    ):
        """
        This is the constructor of the class.
        Creates the window and all the elements inside it, see below.
        :param engine_object: responsible for the logic of the application
        :param db_object: responsible for the database
        :param default_path_for_ready_after_project_name: see main.py
        :param default_path_for_finished_after_project_name: see main.py
        :param default_path_for_excel_after_project_name: see main.py
        :param paths_table_name: see main.py
        :param previous_state_table_name: see main.py
        """

        # -----------------------------------------------------------------------------
        # General window looks
        # -----------------------------------------------------------------------------
        self.window = Tk()
        self.window = apply_the_front_end_settings(self.window)
        app_font = font.Font(family=self.FONT_FAMILY, size=self.FONT_SIZE)

        # -----------------------------------------------------------------------------
        # External objects
        # -----------------------------------------------------------------------------
        self.engine_object = engine_object
        self.db_object = db_object
        self.db_object.create_the_2_predefined_tables()

        # -----------------------------------------------------------------------------
        # Default paths
        # -----------------------------------------------------------------------------
        self.default_path_for_ready_after_project_name = default_path_for_ready_after_project_name
        self.default_path_for_finished_after_project_name = default_path_for_finished_after_project_name
        self.default_path_for_excel_after_project_name = default_path_for_excel_after_project_name

        # -----------------------------------------------------------------------------
        # External strings
        # -----------------------------------------------------------------------------
        self.paths_table_name = paths_table_name
        self.previous_state_table_name = previous_state_table_name

        # -----------------------------------------------------------------------------
        # Internal objects
        # -----------------------------------------------------------------------------
        self.contents_of_status_label = self.DEFAULT_STATUS_TEXT

        # -----------------------------------------------------------------------------
        # Locations
        # -----------------------------------------------------------------------------
        self.location_of_project_dir = None
        self.location_of_ready_dir = None
        self.location_of_finished_dir = None
        self.location_of_documents_list_file = None

        # -----------------------------------------------------------------------------
        # Names of elements
        # -----------------------------------------------------------------------------
        self.name_of_browse_label1 = name_of_browse_label1
        self.name_of_browse_button1 = name_of_browse_button1
        self.name_of_browse_label2 = name_of_browse_label2
        self.name_of_browse_button2 = name_of_browse_button2
        self.name_of_browse_label3 = name_of_browse_label3
        self.name_of_browse_button3 = name_of_browse_button3
        self.name_of_browse_label4 = name_of_browse_label4
        self.name_of_browse_button4 = name_of_browse_button4
        self.name_of_button1 = name_of_button1
        self.name_of_button2 = name_of_button2
        self.name_of_button3 = name_of_button3
        self.name_of_shortcut_button = name_of_shortcut_button

        # -----------------------------------------------------------------------------
        # Browse Buttons
        # -----------------------------------------------------------------------------
        self.browse_button_1, self.browse_button_2, self.browse_button_3, self.browse_button_4 = (
            apply_the_browse_buttons(self.window))

        self.browse_button_1.config(command=self.select_location_of_project_dir)
        self.browse_button_2.config(command=self.select_location_of_ready_dir)
        self.browse_button_3.config(command=self.select_location_of_finished_dir)
        self.browse_button_4.config(command=self.select_location_of_documents_list_file)

        self.browse_button_1.place(x=10, y=10)
        self.browse_button_2.place(x=10, y=40)
        self.browse_button_3.place(x=10, y=70)
        self.browse_button_4.place(x=10, y=100)

        # -----------------------------------------------------------------------------
        # Browse Labels
        # -----------------------------------------------------------------------------
        self.browse_label_1, self.browse_label_2, self.browse_label_3, self.browse_label_4 = (
            apply_the_browse_labels(self.window))

        self.browse_label_1.config(font=(self.FONT_FAMILY, self.FONT_SIZE, "italic"))
        self.browse_label_2.config(font=(self.FONT_FAMILY, self.FONT_SIZE, "italic"))
        self.browse_label_3.config(font=(self.FONT_FAMILY, self.FONT_SIZE, "italic"))
        self.browse_label_4.config(font=(self.FONT_FAMILY, self.FONT_SIZE, "italic"))

        self.browse_label_1.place(x=200, y=11)
        self.browse_label_2.place(x=200, y=41)
        self.browse_label_3.place(x=200, y=71)
        self.browse_label_4.place(x=200, y=101)

        # -----------------------------------------------------------------------------
        # Shortcut buttons
        # -----------------------------------------------------------------------------
        self.shortcut_button_1, self.shortcut_button_2, self.shortcut_button_3, self.shortcut_button_4 = (
            apply_the_shortcut_buttons(self.window))

        self.shortcut_button_1.config(command=self.open_project_dir)
        self.shortcut_button_2.config(command=self.open_ready_dir)
        self.shortcut_button_3.config(command=self.open_finished_dir)
        self.shortcut_button_4.config(command=self.open_documents_list_file)

        self.shortcut_button_1.place(x=730, y=10)
        self.shortcut_button_2.place(x=730, y=40)
        self.shortcut_button_3.place(x=730, y=70)
        self.shortcut_button_4.place(x=730, y=100)

        # -----------------------------------------------------------------------------
        # Create a line separator under the browse section
        # -----------------------------------------------------------------------------
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=140, width=780, height=2)

        # -----------------------------------------------------------------------------
        # Initial query of the database for the directories then update labels
        # -----------------------------------------------------------------------------
        self.initial_query_of_database()

        if self.location_of_project_dir is not None:
            self.update_label_next_to_browse_button(self.browse_label_1, f"{self.location_of_project_dir}")
        if self.location_of_ready_dir is not None:
            self.update_label_next_to_browse_button(self.browse_label_2, f"{self.location_of_ready_dir}")
        if self.location_of_finished_dir is not None:
            self.update_label_next_to_browse_button(self.browse_label_3, f"{self.location_of_finished_dir}")
        if self.location_of_documents_list_file is not None:
            self.update_label_next_to_browse_button(self.browse_label_4, f"{self.location_of_documents_list_file}")

        # -----------------------------------------------------------------------------
        # Work Buttons
        # -----------------------------------------------------------------------------
        self.work_button_1, self.work_button_2, self.work_button_3 = (
            apply_the_work_buttons(self.window))

        self.work_button_1.config(command=self.commands_bound_to_work_button_1)
        self.work_button_2.config(command=self.commands_bound_to_work_button_2)
        self.work_button_3.config(command=self.commands_bound_to_work_button_3)

        self.work_button_1.place(x=10, y=155)
        self.work_button_2.place(x=295, y=155)
        self.work_button_3.place(x=580, y=155)

        # -----------------------------------------------------------------------------
        # Bind keyboard shortcuts to work buttons
        # -----------------------------------------------------------------------------
        self.window.bind_all('<a>', self.commands_bound_to_work_button_1)
        self.window.bind_all('<s>', self.commands_bound_to_work_button_2)
        self.window.bind_all('<d>', self.commands_bound_to_work_button_3)

        # -----------------------------------------------------------------------------
        # Lights next to work buttons
        # -----------------------------------------------------------------------------
        self.canvas1, self.canvas2, self.canvas3, self.rect1, self.rect2, self.rect3 = (
            apply_light_next_to_work_buttons(self.window))

        self.canvas1.place(x=195, y=155)
        self.canvas2.place(x=480, y=155)
        self.canvas3.place(x=765, y=155)

        # -----------------------------------------------------------------------------
        # Create a line separator under the work buttons section
        # -----------------------------------------------------------------------------
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=210, width=780, height=2)

        # -----------------------------------------------------------------------------
        # Status label
        # -----------------------------------------------------------------------------
        self.status_label = scrolledtext.ScrolledText(
            self.window,
            width=109,
            height=31,
            wrap=WORD,
            bg='#FAFAFA',
            fg='#444444',
            border=1,
            relief='solid',
            font=app_font,
        )
        self.status_label.place(x=10, y=225)
        self.status_label.insert(END, self.contents_of_status_label)

    # -----------------------------------------------------------------------------
    # Initial query of the database for the directories
    # -----------------------------------------------------------------------------
    def initial_query_of_database(self):
        """
        Queries the database for the directories and updates the internal variables.
        If there is no data in the database, the internal variables are set to None.
        :return: None
        """
        try:
            result = self.db_object.retrieve_all_data_from_a_table(self.paths_table_name)

            # Check if there is any data in the result
            if result and len(result) >= 4:
                self.location_of_project_dir = result[0][2]
                self.location_of_ready_dir = result[1][2]
                self.location_of_finished_dir = result[2][2]
                self.location_of_documents_list_file = result[3][2]

            else:
                # If there is no data, you may want to handle this case accordingly
                self.location_of_project_dir = None
                self.location_of_ready_dir = None
                self.location_of_finished_dir = None
                self.location_of_documents_list_file = None

        except Exception as e:
            self.update_status_label(f"Грешка: '{e}'")

    # -----------------------------------------------------------------------------
    # Methods on work buttons
    # -----------------------------------------------------------------------------
    @time_measurement_decorator
    def commands_bound_to_work_button_1(self, event=None):
        """
        This method is bound to the first work button and executes the functions
        bound to it. It also updates the light next to the button and the status label.
        :param event: not used
        :return: None
        """
        GlobalErrorHandler.CURRENT_OPERATION = ""
        GlobalErrorHandler.CURRENT_ITEM = ""

        # execute functions and get the result, color and additional message if any
        try:
            return_result, status_color, additional_message = self.engine_object.methods_bound_to_button_1(
                self.location_of_project_dir,           # project_folder
                self.location_of_ready_dir,             # ready_folder
                self.location_of_finished_dir,          # finished_folder
                self.location_of_documents_list_file,   # documents_list_file
            )
        except Exception as e:
            return_result, status_color, additional_message = f"Грешка: '{e}'", 'red', None

        # additional error handling
        if return_result is None and status_color == 'red':
            return_result = GlobalErrorHandler.CURRENT_OPERATION
            return_result += ', ' + GlobalErrorHandler.CURRENT_ITEM
        elif return_result is not None and status_color == 'red':
            return_result += ', ' + GlobalErrorHandler.CURRENT_OPERATION
            return_result += ', ' + GlobalErrorHandler.CURRENT_ITEM

        # feedback to the light next to the button
        self.update_light_next_to_button(self.canvas1, self.rect1, status_color)

        # if there is an additional message, show it
        if additional_message is not None:
            self.update_status_label(f"Операция 1: '{return_result}'\n{additional_message}")
        else:
            self.update_status_label(f"Операция 1: '{return_result}'")

    @time_measurement_decorator
    def commands_bound_to_work_button_2(self, event=None):
        """
        This method is bound to the second work button and executes the functions
        bound to it. It also updates the light next to the button and the status label.
        :param event: not used
        :return: None
        """
        GlobalErrorHandler.CURRENT_OPERATION = ""
        GlobalErrorHandler.CURRENT_ITEM = ""

        # execute functions and get the result, color and additional message if any
        try:
            return_result, status_color, additional_message = self.engine_object.methods_bound_to_button2(
                self.location_of_ready_dir,         # source_folder
                self.location_of_finished_dir,      # destination_folder
                self.location_of_finished_dir,      # archive_folder
            )
        except Exception as e:
            return_result, status_color, additional_message = f"Грешка: '{e}'", 'red', None

        # additional error handling
        if return_result is None and status_color == 'red':
            return_result = GlobalErrorHandler.CURRENT_OPERATION
            return_result += ', ' + GlobalErrorHandler.CURRENT_ITEM
        elif return_result is not None and status_color == 'red':
            return_result += ', ' + GlobalErrorHandler.CURRENT_OPERATION
            return_result += ', ' + GlobalErrorHandler.CURRENT_ITEM

        # feedback to the light next to the button
        self.update_light_next_to_button(self.canvas2, self.rect2, status_color)

        # if there is an additional message, show it
        if additional_message is not None:
            self.update_status_label(f"Операция 2: '{return_result}'\n{additional_message}")
        else:
            self.update_status_label(f"Операция 2: '{return_result}'")

    @time_measurement_decorator
    def commands_bound_to_work_button_3(self, event=None):
        """
        This method is bound to the third work button and clears the status label.
        :param event: not used
        :return: None
        """
        # clear the status label
        self.contents_of_status_label = self.DEFAULT_STATUS_TEXT
        self.status_label.delete('1.0', END)

        # set the light to green for 1 second
        self.update_light_next_to_button(self.canvas3, self.rect3, 'green')
        self.window.after(1000, self.update_light_next_to_button, self.canvas3, self.rect3, 'gray')

    # -----------------------------------------------------------------------------
    # Browse main methods
    # -----------------------------------------------------------------------------
    @time_measurement_decorator
    def select_location_of_project_dir(self, path=None):
        """
        Select the location of the project directory. If the path is not specified,
        a file dialog is opened. Otherwise, the specified path is used. Then the
        location is updated in the database and the label next to the browse button.
        :param path: the path to be used if specified
        :return: None
        """
        if path is None:
            filepath = filedialog.askdirectory()
        else:
            filepath = path

        self.location_of_project_dir = filepath
        self._update_location('location_of_project_dir', self.browse_label_1, filepath)

        # actualize the other directories based on the project directory
        self._actualize_all_dirs_based_on_project_dir()

    @time_measurement_decorator
    def select_location_of_ready_dir(self, path=None):
        """
        Select the location of the ready directory. If the path is not specified,
        a file dialog is opened. Otherwise, the specified path is used. Then the
        location is updated in the database and the label next to the browse button.
        :param path: the path to be used if specified
        :return: None
        """
        if path is None:
            filepath = filedialog.askdirectory()
        else:
            filepath = path

        self.location_of_ready_dir = filepath
        self._update_location('location_of_ready_dir', self.browse_label_2, filepath)

    @time_measurement_decorator
    def select_location_of_finished_dir(self, path=None):
        """
        Select the location of the finished directory. If the path is not specified,
        a file dialog is opened. Otherwise, the specified path is used. Then the
        location is updated in the database and the label next to the browse button.
        :param path: the path to be used if specified
        :return: None
        """
        if path is None:
            filepath = filedialog.askdirectory()
        else:
            filepath = path

        self.location_of_finished_dir = filepath
        self._update_location('location_of_finished_dir', self.browse_label_3, filepath)

    @time_measurement_decorator
    def select_location_of_documents_list_file(self, path=None):
        """
        Select the location of the documents list file. If the path is not specified,
        a file dialog is opened. Otherwise, the specified path is used. Then the
        location is updated in the database and the label next to the browse button.
        :param path: the path to be used if specified
        :return: None
        """
        if path is None:
            filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        else:
            filepath = path

        self.location_of_documents_list_file = filepath
        self._update_location('location_of_documents_list_file', self.browse_label_4, filepath)

    # -----------------------------------------------------------------------------
    # Browse support methods
    # -----------------------------------------------------------------------------
    def _update_location(self, column_value, label_number, filepath):
        """
        Update the database entry or insert a new one based on the specified button identifier,
        and provide feedback by updating the label next to the browse button and the status label.
        :param str column_value: The value for the 'button_identifier' column.
        :param tk.Label label_number: The label next to the browse button.
        :param str filepath: The file path to be associated with the specified button identifier.
        :return: None
        """

        # check if entry exists
        if self.db_object.does_entry_exist(
                self.paths_table_name,      # table name
                "button_identifier",        # column name
                column_value                # column value
        ):
            # If entry already exists, update it
            # self.db_object.update_entry(
            #     self.paths_table_name,      # table name
            #     "button_identifier",        # condition column name
            #     "path",                     # condition value
            #     column_value,               # new path column name
            #     filepath                    # new path value
            # )

            self.db_object.update_entry(
                self.paths_table_name,  # table name
                "button_identifier",  # condition column name
                column_value,  # condition value
                "path",  # new path column name
                filepath  # new path value
            )

        else:
            # Entry doesn't exist; insert a new one
            self.db_object.insert_data(
                self.paths_table_name,      # table name
                "button_identifier",        # column1 name
                "path",                     # column2 name
                column_value,               # column1 value
                filepath                    # data
            )

        # feedback
        self.update_label_next_to_browse_button(label_number, f"{filepath}")
        self.update_status_label(f"избрано: '{filepath}'")

    def _actualize_all_dirs_based_on_project_dir(self):
        """
        Actualize the other directories based on the project directory.
        :return: None
        """
        try:
            # actualize the other directories based on the project directory
            if self.location_of_project_dir is not None:
                self.location_of_ready_dir = os.path.join(self.location_of_project_dir,
                                                          self.default_path_for_ready_after_project_name)
                self.select_location_of_ready_dir(self.location_of_ready_dir)

                self.location_of_finished_dir = os.path.join(self.location_of_project_dir,
                                                             self.default_path_for_finished_after_project_name)
                self.select_location_of_finished_dir(self.location_of_finished_dir)

                self.location_of_documents_list_file = os.path.join(self.location_of_project_dir,
                                                                    self.default_path_for_excel_after_project_name)
                self.select_location_of_documents_list_file(
                    self.choose_latest_excel_file(self.location_of_documents_list_file))

            # check if they are existing folders
            if not os.path.exists(self.location_of_ready_dir):
                return f"Грешка: '{self.location_of_ready_dir}' не съществува!", 'red', None
            if not os.path.exists(self.location_of_finished_dir):
                return f"Грешка: '{self.location_of_finished_dir}' не съществува!", 'red', None
            if not os.path.exists(self.location_of_documents_list_file):
                return f"Грешка: '{self.location_of_documents_list_file}' не съществува!", 'red', None

        except Exception as e:
            return f"Грешка: '{e}'""", 'red', None

    @staticmethod
    def choose_latest_excel_file(path):
        """
        Choose the latest Excel file in the specified folder.
        :param path: The path of the folder containing Excel files.
        :return: The path to the latest Excel file.
        """
        try:
            # Get a list of all Excel files in the folder
            excel_files = [file for file in os.listdir(path) if file.endswith('.xlsx')]

            if not excel_files:
                raise FileNotFoundError(f"No Excel files found in the folder: {path}")

            # Sort the list of files by modification time
            excel_files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))

            # Get the latest file
            latest_file = excel_files[-1]

            # Return the path to the latest file
            return os.path.join(path, latest_file)

        except FileNotFoundError as file_not_found_error:
            # If no Excel files are found
            return f"Грешка: {file_not_found_error}", 'red', None

        except Exception as e:
            # If there are other exceptions
            return f"Грешка: {e}", 'red', None

    # -----------------------------------------------------------------------------
    # Shortcut button methods
    # -----------------------------------------------------------------------------
    def open_project_dir(self):
        os.startfile(self.location_of_project_dir)

    def open_ready_dir(self):
        os.startfile(self.location_of_ready_dir)

    def open_finished_dir(self):
        os.startfile(self.location_of_finished_dir)

    def open_documents_list_file(self):
        os.startfile(self.location_of_documents_list_file)

    # -----------------------------------------------------------------------------
    # General support methods
    # -----------------------------------------------------------------------------
    @staticmethod
    def update_label_next_to_browse_button(label_number, text):
        """
        Updates the label next to the browse button.
        :param label_number: the label to update
        :param text: the text to update the label with
        :return: None
        """
        label_number.config(text=text)
        label_number.config(anchor='w')

    @staticmethod
    def update_light_next_to_button(canvas_number, rect_number, color):
        """
        Updates the light next to the work button.
        :param canvas_number: the canvas to update
        :param rect_number: the rectangle to update
        :param color: the color to update the light with
        :return: None
        """
        canvas_number.itemconfig(rect_number, fill=color, outline=color)

    def update_status_label(self, text):
        """
        Updates the status label. If the label is empty, it clears it first. Otherwise,
        it adds the new text to the existing text. Then it clears the existing text and
        inserts the updated text.
        :param text: the text to update the label with
        :return: None
        """
        # if the status label is empty, clear it
        if self.contents_of_status_label == self.DEFAULT_STATUS_TEXT:
            self.contents_of_status_label = ''

        # add the new text to the existing text
        self.contents_of_status_label += '\n' + text

        # Clear the existing text and insert the updated text
        self.status_label.delete('1.0', END)
        self.status_label.insert(END, self.contents_of_status_label)

    # -----------------------------------------------------------------------------
    # Running the frontend
    # -----------------------------------------------------------------------------
    def run(self):
        """
        Runs the frontend.
        :return: None
        """
        self.window.mainloop()

    def on_exit(self):
        """
        This function is executed when the user closes the window. You can override it
        to perform any final operations or save data before the window is closed.
        Currently, it closes the database connection and quits the window.
        :return: None
        """
        self.db_object.close_connection()       # Close the database connection
        self.window.quit()
