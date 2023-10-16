from tkinter import filedialog
from tkinter import *
from tkinter import font
from tkinter import scrolledtext

from support.custom_functions_lib import time_measurement_decorator


class MyGui:
    APP_NAME = 'ZED, v0.1a'
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    DEFAULT_STATUS_TEXT = '\n' * 12 + 'Няма нови промени'

    def __init__(self, engine_object, db_object):

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
        self.db_object.create_table()

        # -----------------------------------------------------------------------------
        # Internal objects
        # -----------------------------------------------------------------------------
        self.contents_of_status_label = self.DEFAULT_STATUS_TEXT

        # -----------------------------------------------------------------------------
        # Locations
        # -----------------------------------------------------------------------------
        self.location_of_documents_list_file = None
        self.location_of_work_dir = None
        self.location_of_ready_dir = None

        # -----------------------------------------------------------------------------
        # Names of elements
        # -----------------------------------------------------------------------------
        self.name_of_browse_label1 = 'избран файл: няма'
        self.name_of_browse_button1 = 'Избери списъка с документи'

        self.name_of_browse_label2 = 'избрана папка: няма'
        self.name_of_browse_button2 = 'Избери папка `Work`'

        self.name_of_browse_label3 = 'избрана папка: няма'
        self.name_of_browse_button3 = 'Избери папка `Ready`'

        self.name_of_button1 = 'Сканирай за промени (A)'
        self.name_of_button2 = 'Приложи промените (S)'
        self.name_of_button3 = 'Изчисти конзолата (D)'

        # -----------------------------------------------------------------------------
        # Browse Buttons
        # -----------------------------------------------------------------------------
        self.label11 = Label(
            self.window, text=self.name_of_browse_label1, width=26, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white',
        )
        self.label11.place(x=10, y=10)

        self.button11 = Button(
            self.window, text=self.name_of_browse_button1, width=25, height=1,
            command=self.select_location_of_dox_list
        )
        self.button11.place(x=10, y=30)

        self.label12 = Label(
            self.window, text=self.name_of_browse_label2, width=26, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label12.place(x=10, y=70)

        self.button12 = Button(
            self.window, text=self.name_of_browse_button2, width=25, height=1,
            command=self.select_location_of_work_dir
        )
        self.button12.place(x=10, y=90)

        self.label13 = Label(
            self.window, text=self.name_of_browse_label3, width=26, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label13.place(x=10, y=130)

        self.button13 = Button(
            self.window, text=self.name_of_browse_button3, width=25, height=1,
            command=self.select_location_of_ready_dir
        )
        self.button13.place(x=10, y=150)

        # Create a line separator under the button
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=190, width=186, height=2)

        # -----------------------------------------------------------------------------
        # Initial query of the database for the directories
        # -----------------------------------------------------------------------------
        self.initial_query_of_database()

        if self.location_of_documents_list_file is not None:
            self.update_label_next_to_browse_button(self.label11, f"{self.location_of_documents_list_file}")
        if self.location_of_work_dir is not None:
            self.update_label_next_to_browse_button(self.label12, f"{self.location_of_work_dir}")
        if self.location_of_ready_dir is not None:
            self.update_label_next_to_browse_button(self.label13, f"{self.location_of_ready_dir}")

        # -----------------------------------------------------------------------------
        # Work Buttons
        # -----------------------------------------------------------------------------
        self.button1 = Button(
            self.window,
            text=self.name_of_button1,
            command=self.command1,
            width=25,
            height=2,
        )
        self.button1.place(x=10, y=205)

        self.button2 = Button(
            self.window,
            text=self.name_of_button2,
            command=self.command2,
            width=25,
            height=2,
        )
        self.button2.place(x=10, y=255)

        self.button3 = Button(
            self.window,
            text=self.name_of_button3,
            command=self.command3,
            width=25,
            height=2,
        )
        self.button3.place(x=10, y=305)

        # Bind keyboard shortcuts
        self.window.bind_all('<a>', self.command1)
        self.window.bind_all('<s>', self.command2)
        self.window.bind_all('<d>', self.command3)

        # Lights next to buttons
        self.canvas1 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect1 = self.canvas1.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas1.place(x=195, y=205)

        self.canvas2 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect2 = self.canvas2.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas2.place(x=195, y=255)

        self.canvas3 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect3 = self.canvas3.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas3.place(x=195, y=305)

        # Create a line separator under the button
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=360, width=186, height=2)

        # -----------------------------------------------------------------------------
        # Status label
        # -----------------------------------------------------------------------------
        self.status_label = scrolledtext.ScrolledText(
            self.window,
            width=45,
            height=23,
            wrap=WORD,
            bg='#FAFAFA',
            fg='#444444',
            border=1,
            relief='solid',
        )
        self.status_label.place(x=412, y=10)

    # -----------------------------------------------------------------------------
    # Initial query of the database for the directories
    # -----------------------------------------------------------------------------
    def initial_query_of_database(self):
        try:
            result = self.db_object.retrieve_data()
            self.location_of_documents_list_file = result[0][2]
            self.location_of_work_dir = result[1][2]
            self.location_of_ready_dir = result[2][2]
        except Exception as e:
            pass

    # -----------------------------------------------------------------------------
    # Methods on buttons
    # -----------------------------------------------------------------------------
    @time_measurement_decorator
    def command1(self, event=None):
        # function
        result, color = self.engine_object.functions_bound_to_button1(
            self.location_of_documents_list_file,
            self.location_of_work_dir,
            self.location_of_ready_dir,
        )

        # feedback
        self.update_light_next_to_button(self.canvas1, self.rect1, color)
        self.update_status_label(f"Операция 1: '{result}'")

    @time_measurement_decorator
    def command2(self, event=None):
        # function
        result = self.engine_object.functions_bound_to_button2()

        # feedback
        self.update_light_next_to_button(self.canvas2, self.rect2, result)
        self.update_status_label(f"Операция 2: '{result}'")

    @time_measurement_decorator
    def command3(self, event=None):
        # clear the status label
        self.contents_of_status_label = self.DEFAULT_STATUS_TEXT
        self.status_label.delete('1.0', END)

        # set the light to green for 1 second
        self.update_light_next_to_button(self.canvas3, self.rect3, 'green')
        self.window.after(1000, self.update_light_next_to_button, self.canvas3, self.rect3, 'gray')

    # -----------------------------------------------------------------------------
    # Browse methods
    # -----------------------------------------------------------------------------
    @time_measurement_decorator
    def select_location_of_dox_list(self):
        # function
        filepath = filedialog.askopenfilename()
        self.location_of_documents_list_file = filepath

        # check if entry exists
        button_identifier = 'location_of_documents_list_file'
        if self.db_object.entry_exists(button_identifier):
            # Entry already exists; update it
            self.db_object.update_entry(button_identifier, filepath)
        else:
            # Entry doesn't exist; insert a new one
            self.db_object.insert_data(button_identifier, filepath)

        # feedback
        self.update_label_next_to_browse_button(self.label11, f"{filepath}")
        self.update_status_label(f"selected: '{filepath}'")

    @time_measurement_decorator
    def select_location_of_work_dir(self):
        # function
        filepath = filedialog.askdirectory()
        self.location_of_work_dir = filepath

        # check if entry exists
        button_identifier = 'location_of_work_dir'
        if self.db_object.entry_exists(button_identifier):
            # Entry already exists; update it
            self.db_object.update_entry(button_identifier, filepath)
        else:
            # Entry doesn't exist; insert a new one
            self.db_object.insert_data(button_identifier, filepath)

        # feedback
        self.update_label_next_to_browse_button(self.label12, f"{filepath}")
        self.update_status_label(f"selected: '{filepath}'")

    @time_measurement_decorator
    def select_location_of_ready_dir(self):
        # function
        filepath = filedialog.askdirectory()
        self.location_of_ready_dir = filepath

        # check if entry exists
        button_identifier = 'location_of_ready_dir'
        if self.db_object.entry_exists(button_identifier):
            # Entry already exists; update it
            self.db_object.update_entry(button_identifier, filepath)
        else:
            # Entry doesn't exist; insert a new one
            self.db_object.insert_data(button_identifier, filepath)

        # feedback
        self.update_label_next_to_browse_button(self.label13, f"{filepath}")
        self.update_status_label(f"selected: '{filepath}'")

    # -----------------------------------------------------------------------------
    # Browse methods
    # -----------------------------------------------------------------------------
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
