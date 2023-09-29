import random
import os
import time
from os import walk
from os.path import exists
from tkinter import filedialog
from openpyxl import Workbook
from tkinter import *
from tkinter import font

from custom_functions.custom_functions_lib import time_measurement_decorator


class MyGui:
    APP_NAME = 'ZED, v0.1a'
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    DEFAULT_STATUS_TEXT = '\n' * 12 + 'Няма нови промени'

    def __init__(self, engine_object):

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
        # Objects
        # -----------------------------------------------------------------------------
        self.engine_object = engine_object

        # -----------------------------------------------------------------------------
        # Locations
        # -----------------------------------------------------------------------------
        self.location_of_dox_list = None
        self.location_of_work_dir = None
        self.location_of_ready_dir = None

        # -----------------------------------------------------------------------------
        # Browse Buttons
        # -----------------------------------------------------------------------------
        self.label11 = Label(
            self.window, text='select target dir', width=26, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white',
        )
        self.label11.place(x=10, y=10)

        self.button11 = Button(
            self.window, text='browse', width=25, height=1,
            command=self.select_location_of_dox_list
        )
        self.button11.place(x=10, y=40)

        self.label12 = Label(
            self.window, text='select target dir', width=26, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label12.place(x=10, y=70)

        self.button12 = Button(
            self.window, text='browse', width=25, height=1,
            command=self.select_location_of_work_dir
        )
        self.button12.place(x=10, y=100)

        self.label13 = Label(
            self.window, text='select target dir', width=26, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label13.place(x=10, y=130)

        self.button13 = Button(
            self.window, text='browse', width=25, height=1,
            command=self.select_location_of_ready_dir
        )
        self.button13.place(x=10, y=160)

        # Create a line separator under the button
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=200, width=186, height=2)

        # -----------------------------------------------------------------------------
        # Work Buttons
        # -----------------------------------------------------------------------------
        self.button1 = Button(
            self.window,
            text='Сканирай за промени (A)',
            command=self.command1,
            width=25,
            height=2,
        )
        self.button1.place(x=10, y=210)

        self.button2 = Button(
            self.window,
            text='Приложи промените (S)',
            command=self.command2,
            width=25,
            height=2,
        )
        self.button2.place(x=10, y=260)

        self.button3 = Button(
            self.window,
            text='Списък (D)',
            command=self.command3,
            width=25,
            height=2,
        )
        self.button3.place(x=10, y=310)

        # Bind keyboard shortcuts
        self.window.bind_all('<a>', self.command1)
        self.window.bind_all('<s>', self.command2)
        self.window.bind_all('<d>', self.command3)

        # Lights next to buttons
        self.canvas1 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect1 = self.canvas1.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas1.place(x=195, y=210)

        self.canvas2 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect2 = self.canvas2.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas2.place(x=195, y=260)

        self.canvas3 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect3 = self.canvas3.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas3.place(x=195, y=310)

        # Create a line separator under the button
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=360, width=186, height=2)

        # -----------------------------------------------------------------------------
        # Status label
        # -----------------------------------------------------------------------------
        self.label1 = Label(
            self.window,
            text=self.DEFAULT_STATUS_TEXT,
            anchor='n',
            width=53,
            height=25,
            bg='#FAFAFA',
            fg='#444444',
            border=1,
            relief='solid',
        )

        self.label1.place(x=412, y=10)

    # -----------------------------------------------------------------------------
    # Methods on buttons
    # -----------------------------------------------------------------------------
    @time_measurement_decorator
    def command1(self, event=None):
        result = self.engine_object.functions_bound_to_button1()
        self.canvas1.itemconfig(self.rect1, fill=result, outline=result)
        self.label1.config(text=f"command1: '{result}'")

    @time_measurement_decorator
    def command2(self, event=None):
        result = self.engine_object.functions_bound_to_button2()
        self.canvas2.itemconfig(self.rect2, fill=result, outline=result)
        self.label1.config(text=f"command2: '{result}'")

    @time_measurement_decorator
    def command3(self, event=None):
        result = self.engine_object.functions_bound_to_button3()
        self.canvas3.itemconfig(self.rect3, fill=result, outline=result)
        self.label1.config(text=f"command3: '{result}'")

    # -----------------------------------------------------------------------------
    # Other methods
    # -----------------------------------------------------------------------------
    def select_location_of_dox_list(self):
        filepath = filedialog.askdirectory()
        self.current_folder = filepath
        self.label11.config(text=f"{self.current_folder}")
        self.label11.config(anchor='w')
        self.label1.config(text=f"selected: '{self.current_folder}'")

    def select_location_of_work_dir(self):
        filepath = filedialog.askdirectory()
        self.current_folder = filepath
        self.label12.config(text=f"{self.current_folder}")
        self.label12.config(anchor='w')
        self.label1.config(text=f"selected: '{self.current_folder}'")

    def select_location_of_ready_dir(self):
        filepath = filedialog.askdirectory()
        self.current_folder = filepath
        self.label13.config(text=f"{self.current_folder}")
        self.label13.config(anchor='w')
        self.label1.config(text=f"selected: '{self.current_folder}'")

    def run(self):
        self.window.mainloop()
