# -*- coding: windows-1251 -*-

import os
from tkinter import filedialog
from tkinter import *
from tkinter import font
from tkinter import scrolledtext

from support.custom_functions_lib import time_measurement_decorator


class MyGui:
    APP_NAME = 'ZED, v0.3a'
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 705
    DEFAULT_STATUS_TEXT = (
        'Правилно име на фолдър:\n' +
        '`20230928 - MC077-021-001-Leak proof joint design and drawing for hull`\n' +
        'или:\n'
        '`20230928 - MC077-021-001-Leak proof joint design and drawing for hull - 1`\n' +
        '\n' +
        'Правилно име на файл:\n' +
        '`MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023.dwg`\n' +
        'или:\n' +
        '`MC077-022-001-Leak proof joint design and drawing for tank and deck surface - 30092023-A1.pdf`\n' +
        '\n' +
        'правилен формат на Excel-ския файл: .xlsx\n' +
        '\n' +
        'Програмата чете от първия Sheet на Excel-ския файл!'
    )

    def __init__(
            self,
            engine_object,
            db_object,
            default_path_for_ready_after_project_name,
            default_path_for_finished_after_project_name,
            default_path_for_excel_after_project_name,
            paths_table_name,
            previous_state_table_name,
    ):

        # -----------------------------------------------------------------------------
        # General window looks
        # -----------------------------------------------------------------------------
        self.window = Tk()
        self.window.title(self.APP_NAME)
        self.window.eval("tk::PlaceWindow . center")
        x = self.window.winfo_screenwidth() * 3 // 10
        y = int(self.window.winfo_screenheight() * 0.2)
        # self.window.geometry('400x400+' + str(x) + '+' + str(y))
        self.window.geometry(f'{str(self.WINDOW_WIDTH)}x{str(self.WINDOW_HEIGHT)}+'
                             + str(x) + '+' + str(y))
        self.window.iconbitmap('static\\icon.ico')
        # self.window.config(background='#D3D3D3')
        self.window.config(background='#E5E5E5')
        roboto_font = font.Font(family="Roboto", size=9)

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
        self.name_of_browse_label1 = 'Път към проекта: няма'
        self.name_of_browse_button1 = 'Избери пътя към проекта'

        self.name_of_browse_label2 = 'Път към `Ready`: няма'
        self.name_of_browse_button2 = 'Промени пътя към `Ready`'

        self.name_of_browse_label3 = 'Път към `020 CLASSIFICATION DRAWINGS`: няма'
        self.name_of_browse_button3 = 'Промени пътя към `020`'

        self.name_of_browse_label4 = 'Път към актуалния списък в Excel: няма'
        self.name_of_browse_button4 = 'Промени пътя към списъка'

        self.name_of_button1 = 'Сканирай за промени (A)'
        self.name_of_button2 = 'Приложи промените (S)'
        self.name_of_button3 = 'Изчисти конзолата (D)'

        self.name_of_shortcut_button = '>>'

        # -----------------------------------------------------------------------------
        # Browse Buttons
        # -----------------------------------------------------------------------------
        self.button11 = Button(
            self.window, text=self.name_of_browse_button1, width=25, height=1,
            # cursor='hand2',
            command=self.select_location_of_project_dir
        )
        self.button11.place(x=10, y=10)

        self.label11 = Label(
            self.window, text=self.name_of_browse_label1, width=84, height=1,
            bg='#E5E5E5', borderwidth=0, relief="ridge", fg='grey', pady=4,
        )
        self.label11.place(x=200, y=11)
        self.label11.config(font=("Roboto", 9, "italic"))

        self.button12 = Button(
            self.window, text=self.name_of_browse_button2, width=25, height=1,
            # cursor='hand2',
            command=self.select_location_of_ready_dir
        )
        self.button12.place(x=10, y=40)

        self.label12 = Label(
            self.window, text=self.name_of_browse_label2, width=84, height=1,
            bg='#E5E5E5', borderwidth=0, relief="ridge", fg='grey', pady=4,
        )
        self.label12.place(x=200, y=41)
        self.label12.config(font=("Roboto", 9, "italic"))

        self.button13 = Button(
            self.window, text=self.name_of_browse_button3, width=25, height=1,
            # cursor='hand2',
            command=self.select_location_of_finished_dir
        )
        self.button13.place(x=10, y=70)

        self.label13 = Label(
            self.window, text=self.name_of_browse_label3, width=84, height=1,
            bg='#E5E5E5', borderwidth=0, relief="ridge", fg='grey', pady=4,
        )
        self.label13.place(x=200, y=71)
        self.label13.config(font=("Roboto", 9, "italic"))

        self.button14 = Button(
            self.window, text=self.name_of_browse_button4, width=25, height=1,
            # cursor='hand2',
            command=self.select_location_of_documents_list_file
        )
        self.button14.place(x=10, y=100)

        self.label14 = Label(
            self.window, text=self.name_of_browse_label4, width=84, height=1,
            bg='#E5E5E5', borderwidth=0, relief="ridge", fg='grey', pady=4,
        )
        self.label14.place(x=200, y=101)
        self.label14.config(font=("Roboto", 9, "italic"))

        # Create a line separator under the button
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=140, width=780, height=2)

        # -----------------------------------------------------------------------------
        # Shortcut buttons
        # -----------------------------------------------------------------------------
        self.button21 = Button(
            self.window, text=self.name_of_shortcut_button, width=5, height=1,
            relief="flat", cursor='hand2',
            command=self.open_project_dir
        )
        self.button21.place(x=730, y=10)

        self.button22 = Button(
            self.window, text=self.name_of_shortcut_button, width=5, height=1,
            relief="flat", cursor='hand2',
            command=self.open_ready_dir
        )
        self.button22.place(x=730, y=40)

        self.button23 = Button(
            self.window, text=self.name_of_shortcut_button, width=5, height=1,
            relief="flat", cursor='hand2',
            command=self.open_finished_dir
        )
        self.button23.place(x=730, y=70)

        self.button24 = Button(
            self.window, text=self.name_of_shortcut_button, width=5, height=1,
            relief="flat", cursor='hand2',
            command=self.open_documents_list_file
        )
        self.button24.place(x=730, y=100)

        # -----------------------------------------------------------------------------
        # Initial query of the database for the directories
        # -----------------------------------------------------------------------------
        self.initial_query_of_database()

        if self.location_of_project_dir is not None:
            self.update_label_next_to_browse_button(self.label11, f"{self.location_of_project_dir}")
        if self.location_of_ready_dir is not None:
            self.update_label_next_to_browse_button(self.label12, f"{self.location_of_ready_dir}")
        if self.location_of_finished_dir is not None:
            self.update_label_next_to_browse_button(self.label13, f"{self.location_of_finished_dir}")
        if self.location_of_documents_list_file is not None:
            self.update_label_next_to_browse_button(self.label14, f"{self.location_of_documents_list_file}")

        # -----------------------------------------------------------------------------
        # Work Buttons
        # -----------------------------------------------------------------------------
        self.button1 = Button(
            self.window,
            text=self.name_of_button1,
            command=self.commands_of_button1,
            width=25,
            height=2,
            # cursor='hand2',
        )
        self.button1.place(x=10, y=155)

        self.button2 = Button(
            self.window,
            text=self.name_of_button2,
            command=self.commands_of_button2,
            width=25,
            height=2,
            # cursor='hand2',
        )
        self.button2.place(x=295, y=155)

        self.button3 = Button(
            self.window,
            text=self.name_of_button3,
            command=self.commands_of_button3,
            width=25,
            height=2,
            # cursor='hand2',
        )
        self.button3.place(x=580, y=155)

        # Bind keyboard shortcuts
        self.window.bind_all('<a>', self.commands_of_button1)
        self.window.bind_all('<s>', self.commands_of_button2)
        self.window.bind_all('<d>', self.commands_of_button3)

        # Lights next to buttons
        self.canvas1 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect1 = self.canvas1.create_rectangle(2, 1, 10, 39, fill='gray', outline='gray')
        self.canvas1.place(x=195, y=155)

        self.canvas2 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect2 = self.canvas2.create_rectangle(2, 1, 10, 39, fill='gray', outline='gray')
        self.canvas2.place(x=480, y=155)

        self.canvas3 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect3 = self.canvas3.create_rectangle(2, 1, 10, 39, fill='gray', outline='gray')
        self.canvas3.place(x=765, y=155)

        # Create a line separator under the button
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
            font=roboto_font,
        )
        # self.status_label.place(x=412, y=10)
        self.status_label.place(x=10, y=225)
        self.status_label.insert(END, self.contents_of_status_label)

    # -----------------------------------------------------------------------------
    # Initial query of the database for the directories
    # -----------------------------------------------------------------------------
    def initial_query_of_database(self):
        try:
            result = self.db_object.retrieve_data(self.paths_table_name)
            self.location_of_project_dir = result[0][2]
            self.location_of_ready_dir = result[1][2]
            self.location_of_finished_dir = result[2][2]
            self.location_of_documents_list_file = result[3][2]
        except Exception as e:
            pass

    # -----------------------------------------------------------------------------
    # Methods on buttons
    # -----------------------------------------------------------------------------
    @time_measurement_decorator
    def commands_of_button1(self, event=None):
        # functions
        result, color, message = self.engine_object.functions_bound_to_button1(
            self.location_of_project_dir,   # project_folder
            self.location_of_ready_dir,     # ready_folder
            self.location_of_finished_dir,  # finished_folder
            self.location_of_documents_list_file,  # documents_list_file
        )

        # feedback
        self.update_light_next_to_button(self.canvas1, self.rect1, color)

        # if there is an additional message, show it
        if message is not None:
            self.update_status_label(f"Операция 1: '{result}'\n{message}")
        else:
            self.update_status_label(f"Операция 1: '{result}'")

    @time_measurement_decorator
    def commands_of_button2(self, event=None):
        # functions
        result, color, message = self.engine_object.functions_bound_to_button2(
            self.location_of_ready_dir,      # source_folder
            self.location_of_finished_dir,   # destination_folder
            self.location_of_finished_dir,   # archive_folder
        )

        # feedback
        self.update_light_next_to_button(self.canvas2, self.rect2, color)

        # if there is an additional message, show it
        if message is not None:
            self.update_status_label(f"Операция 2: '{result}'\n{message}")
        else:
            self.update_status_label(f"Операция 2: '{result}'")

    @time_measurement_decorator
    def commands_of_button3(self, event=None):
        # clear the status label
        self.contents_of_status_label = self.DEFAULT_STATUS_TEXT
        self.status_label.delete('1.0', END)

        # set the light to green for 1 second
        self.update_light_next_to_button(self.canvas3, self.rect3, 'green')
        self.window.after(1000, self.update_light_next_to_button, self.canvas3, self.rect3, 'gray')

    # -----------------------------------------------------------------------------
    # Browse methods
    # -----------------------------------------------------------------------------
    def _select_location_template(self, button_identifier, label_number, filepath):
        # check if entry exists
        # if self.db_object.entry_exists(button_identifier):
        if self.db_object.entry_exists(self.paths_table_name, "button_identifier", button_identifier):
            # Entry already exists; update it
            self.db_object.update_entry(self.paths_table_name, "button_identifier", "path", button_identifier, filepath)
        else:
            # Entry doesn't exist; insert a new one
            self.db_object.insert_data(self.paths_table_name, "button_identifier", "path", button_identifier, filepath)

        # feedback
        self.update_label_next_to_browse_button(label_number, f"{filepath}")
        self.update_status_label(f"избрано: '{filepath}'")

    @staticmethod
    def _choose_the_excel_with_latest_revision(path):
        # get a list of all Excel files in the folder
        list_of_files = os.listdir(path)

        # filter the list to contain only Excel files
        list_of_files = [file for file in list_of_files if file.endswith('.xlsx')]

        # sort the list by date
        list_of_files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))

        # get the latest file
        latest_file = list_of_files[-1]

        # return the path to the latest file
        return os.path.join(path, latest_file)

    def _actualize_all_dirs_based_on_project_dir(self):
        # actualize the other directories based on the project directory
        if self.location_of_project_dir is not None:
            self.location_of_ready_dir = os.path.join(self.location_of_project_dir, self.default_path_for_ready_after_project_name)
            self.select_location_of_ready_dir(self.location_of_ready_dir)

            self.location_of_finished_dir = os.path.join(self.location_of_project_dir, self.default_path_for_finished_after_project_name)
            self.select_location_of_finished_dir(self.location_of_finished_dir)

            self.location_of_documents_list_file = os.path.join(self.location_of_project_dir, self.default_path_for_excel_after_project_name)
            self.select_location_of_documents_list_file(self._choose_the_excel_with_latest_revision(self.location_of_documents_list_file))

    @time_measurement_decorator
    def select_location_of_project_dir(self, path=None):
        # function
        if path is None:
            filepath = filedialog.askdirectory()
        else:
            filepath = path

        self.location_of_project_dir = filepath
        self._select_location_template('location_of_project_dir', self.label11, filepath)

        # actualize the other directories based on the project directory
        self._actualize_all_dirs_based_on_project_dir()

    @time_measurement_decorator
    def select_location_of_ready_dir(self, path=None):
        # function
        if path is None:
            filepath = filedialog.askdirectory()
        else:
            filepath = path

        self.location_of_ready_dir = filepath
        self._select_location_template('location_of_ready_dir', self.label12, filepath)

    @time_measurement_decorator
    def select_location_of_finished_dir(self, path=None):
        # function
        if path is None:
            filepath = filedialog.askdirectory()
        else:
            filepath = path

        self.location_of_finished_dir = filepath
        self._select_location_template('location_of_finished_dir', self.label13, filepath)

    @time_measurement_decorator
    def select_location_of_documents_list_file(self, path=None):
        # function
        if path is None:
            filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        else:
            filepath = path

        self.location_of_documents_list_file = filepath
        self._select_location_template('location_of_documents_list_file', self.label14, filepath)

    # -----------------------------------------------------------------------------
    # Support methods
    # -----------------------------------------------------------------------------
    def open_project_dir(self):
        os.startfile(self.location_of_project_dir)

    def open_ready_dir(self):
        os.startfile(self.location_of_ready_dir)

    def open_finished_dir(self):
        os.startfile(self.location_of_finished_dir)

    def open_documents_list_file(self):
        os.startfile(self.location_of_documents_list_file)

    @staticmethod
    def update_label_next_to_browse_button(label_number, text):
        label_number.config(text=text)
        label_number.config(anchor='w')

    @staticmethod
    def update_light_next_to_button(canvas_number, rect_number, color):
        canvas_number.itemconfig(rect_number, fill=color, outline=color)

    def update_status_label(self, text):
        if self.contents_of_status_label == self.DEFAULT_STATUS_TEXT:
            self.contents_of_status_label = ''

        self.contents_of_status_label += '\n' + text

        # Clear the existing text and insert the updated text
        self.status_label.delete('1.0', END)
        self.status_label.insert(END, self.contents_of_status_label)

    # -----------------------------------------------------------------------------
    def run(self):
        self.window.mainloop()

    def on_exit(self):
        # This is just an example function; you should adapt it to your application's logic
        # Perform any final operations or save data
        # Close the database connection
        self.db_object.close_connection()
        self.window.quit()
