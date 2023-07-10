import os
import time
from os import walk
from os.path import exists
from tkinter import filedialog
from openpyxl import Workbook
from tkinter import *


def time_measurement_decorator(some_function):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = some_function(*args, **kwargs)
        end = time.time()
        measurement = end - start
        new_gui.label3.config(text=f"generated in: {measurement:.5f}")
        return result
    return wrapper


class DirWalkerGui:
    def __init__(self):
        self.current_folder = ''
        self.generated_txt_file_path = './generated_txt_file.txt'
        self.generated_excel_file_path = './generated_excel_file.xlsx'
        self.current_excel_cell = 'A1'

        self.workbook = None
        self.worksheet = None

        self.window = Tk()
        self.window.geometry("300x300")
        self.window.title("dir walker")
        self.window.config(background='#2b2828')

        self.label1 = Label(
            self.window, text='select target dir', width=30, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label1.pack()

        self.button1 = Button(
            self.window, text='browse', width=30, height=1,
            command=self.open_dir
        )
        self.button1.pack()

        self.label2 = Label(
            self.window, text=self.current_folder, width=30, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label2.pack()

        self.button2 = Button(
            self.window, text='generate', width=30, height=1,
            command=self.the_walk_loop
        )
        self.button2.pack()

        self.label3 = Label(
            self.window, text='', width=30, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label3.pack()

    @staticmethod
    def empty_the_output_txt_file(file_path):
        if exists(file_path):
            os.remove(file_path)

    def empty_the_output_excel_file(self, file_path):
        if exists(file_path):
            os.remove(file_path)

        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        self.worksheet.title = "Data"

    @staticmethod
    def write_into_txt_file(file_path, content):
        with open(file_path, 'a') as output_file:
            output_file.write(content + '\n')

    def write_into_excel_file(self, file_path, content):
        self.worksheet.append([content])
        self.workbook.save(file_path)

    def open_dir(self):
        filepath = filedialog.askdirectory()
        self.current_folder = filepath
        self.label2.config(text=f"selected: '{self.current_folder}'")

    @staticmethod
    def fix_the_dir_path_str(dir_path):
        dir_path = dir_path[0:2] + '/' + dir_path[3:]
        return dir_path

    @time_measurement_decorator
    def the_walk_loop(self):
        self.empty_the_output_txt_file(self.generated_txt_file_path)
        self.empty_the_output_excel_file(self.generated_excel_file_path)

        folder = self.current_folder

        for (dir_path, dir_names, file_names) in walk(folder):
            dir_path = self.fix_the_dir_path_str(dir_path)

            self.write_into_txt_file(self.generated_txt_file_path, f'Directory: {dir_path}')
            self.write_into_excel_file(self.generated_excel_file_path, f'Directory: {dir_path}')

            for directory in dir_names:
                self.write_into_txt_file(self.generated_txt_file_path, f'a directory: {directory}')
                self.write_into_excel_file(self.generated_excel_file_path, f'a directory: {directory}')

            for file in file_names:
                self.write_into_txt_file(self.generated_txt_file_path, f'a file: {file}')
                self.write_into_excel_file(self.generated_excel_file_path, f'a file: {file}')

            self.write_into_txt_file(self.generated_txt_file_path, '\n')
            self.write_into_excel_file(self.generated_excel_file_path, '\n')

    def run(self):
        self.window.mainloop()


new_gui = DirWalkerGui()
new_gui.run()
