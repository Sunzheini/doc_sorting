import random
from tkinter import *
from tkinter import font


class MyGui:
    APP_NAME = 'ZED'
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    DEFAULT_STATUS_TEXT = '\n\n\n\n\n\n\n\n\n\n\n\n' \
                          + 'Няма нови промени'

    def __init__(self):
        # general window looks
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

        self.button1 = Button(
            self.window,
            text='Сканирай за промени (A)',
            command=self.command1,
            width=25,
            height=2,
        )
        self.button1.place(x=10, y=10)

        self.button2 = Button(
            self.window,
            text='Приложи промените (S)',
            command=self.command2,
            width=25,
            height=2,
        )
        self.button2.place(x=10, y=60)

        self.button3 = Button(
            self.window,
            text='Списък (D)',
            command=self.command3,
            width=25,
            height=2,
        )
        self.button3.place(x=10, y=110)

        # Bind keyboard shortcuts
        self.window.bind_all('<a>', self.command1)
        self.window.bind_all('<s>', self.command2)
        self.window.bind_all('<d>', self.command3)

        # Create a line separator under the button
        self.line_sep = Frame(self.window, height=2, bd=1, relief='sunken')
        self.line_sep.place(x=10, y=160, width=186, height=2)

        self.canvas1 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect1 = self.canvas1.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas1.place(x=195, y=10)

        self.canvas2 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect2 = self.canvas2.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas2.place(x=195, y=60)

        self.canvas3 = Canvas(self.window, width=15, height=60, bd=0, highlightthickness=0, bg='#E5E5E5')
        self.rect3 = self.canvas3.create_rectangle(2, 1, 7, 39, fill='gray', outline='gray')
        self.canvas3.place(x=195, y=110)

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

    def command1(self, event=None):
        random_list = ['red', 'green', 'yellow', 'gray']
        random1 = random.choice(random_list)
        self.canvas1.itemconfig(self.rect1, fill=random1, outline=random1)
        print('command1')

    def command2(self, event=None):
        random_list = ['red', 'green', 'yellow', 'gray']
        random2 = random.choice(random_list)
        self.canvas2.itemconfig(self.rect2, fill=random2, outline=random2)
        print('command2')

    def command3(self, event=None):
        random_list = ['red', 'green', 'yellow', 'gray']
        random3 = random.choice(random_list)
        self.canvas3.itemconfig(self.rect3, fill=random3, outline=random3)
        print('command3')

    def run(self):
        self.window.mainloop()
