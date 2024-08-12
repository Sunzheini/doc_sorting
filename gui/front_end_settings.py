# -*- coding: utf-8 -*-
from tkinter import Button, Label, Canvas

# general -----------------------------------------------------------------------------
app_name = 'ZED'
app_version = 'v.01'
window_width = 800
window_height = 705
roboto_font_family = 'Roboto'
roboto_font_size = 9


# button names -------------------------------------------------------------------------
name_of_browse_label1 = 'Път към проекта: няма'
name_of_browse_button1 = 'Избери пътя към проекта'
name_of_browse_label2 = 'Път към `Ready`: няма'
name_of_browse_button2 = 'Промени пътя към `Ready`'
name_of_browse_label3 = 'Път към `020 CLASSIFICATION DRAWINGS`: няма'
name_of_browse_button3 = 'Промени пътя към `020`'
name_of_browse_label4 = 'Път към актуалния списък в Excel: няма'
name_of_browse_button4 = 'Промени пътя към списъка'
name_of_button1 = 'Сканирай за промени (A)'
name_of_button2 = 'Приложи промените (S)'
name_of_button3 = 'Изчисти конзолата (D)'
name_of_button4 = 'Справка за проекта (F)'
name_of_shortcut_button = '>>'


# button settings ----------------------------------------------------------------------
browse_button_width = 25
browse_button_height = 1
shortcut_button_width = 5
shortcut_button_height = 1
shortcut_button_relief = 'flat'
shortcut_button_cursor = 'hand2'
work_button_width = 20
work_button_height = 2


# label settings -----------------------------------------------------------------------
browse_label_width = 84
browse_label_height = 1
label_background_color = '#E5E5E5'
label_relief = 'ridge'
label_foreground_color = 'grey'


# lights settings ----------------------------------------------------------------------
light_width = 15
light_height = 60
light_background_color = '#E5E5E5'
light_fill_color = 'gray'
light_outline_color = 'gray'


def apply_the_front_end_settings(window):
    """
    Applies the front end settings to the window
    :param window: to apply the settings to
    :return: the window with the applied settings
    """
    window.title(app_name + ', ' + app_version)
    window.eval("tk::PlaceWindow . center")
    x = window.winfo_screenwidth() * 3 // 10
    y = int(window.winfo_screenheight() * 0.2)
    window.geometry(f'{str(window_width)}x{str(window_height)}+' + str(x) + '+' + str(y))
    window.iconbitmap('static\\icon.ico')
    window.config(background='#E5E5E5')

    return window


def apply_the_browse_buttons(window):
    """
    Applies the browse buttons to the window
    :param window: to apply the buttons to
    :return: the buttons applied to the window
    """
    browse_button_1 = Button(
        window,
        text=name_of_browse_button1,
        width=browse_button_width,
        height=browse_button_height,
    )

    browse_button_2 = Button(
        window,
        text=name_of_browse_button2,
        width=browse_button_width,
        height=browse_button_height,
    )

    browse_button_3 = Button(
        window,
        text=name_of_browse_button3,
        width=browse_button_width,
        height=browse_button_height,
    )

    browse_button_4 = Button(
        window,
        text=name_of_browse_button4,
        width=browse_button_width,
        height=browse_button_height,
    )

    return browse_button_1, browse_button_2, browse_button_3, browse_button_4


def apply_the_browse_labels(window):
    """
    Applies the browse labels to the window
    :param window: to apply the labels to
    :return: the labels applied to the window
    """
    browse_label_1 = Label(
        window,
        text=name_of_browse_label1,
        width=browse_label_width,
        height=browse_label_height,
        bg=label_background_color,
        borderwidth=0,
        relief=label_relief,
        fg=label_foreground_color,
        pady=4,
    )

    browse_label_2 = Label(
        window,
        text=name_of_browse_label2,
        width=browse_label_width,
        height=browse_label_height,
        bg=label_background_color,
        borderwidth=0,
        relief=label_relief,
        fg=label_foreground_color,
        pady=4,
    )

    browse_label_3 = Label(
        window,
        text=name_of_browse_label3,
        width=browse_label_width,
        height=browse_label_height,
        bg=label_background_color,
        borderwidth=0,
        relief=label_relief,
        fg=label_foreground_color,
        pady=4,
    )

    browse_label_4 = Label(
        window,
        text=name_of_browse_label4,
        width=browse_label_width,
        height=browse_label_height,
        bg=label_background_color,
        borderwidth=0,
        relief=label_relief,
        fg=label_foreground_color,
        pady=4,
    )

    return browse_label_1, browse_label_2, browse_label_3, browse_label_4


def apply_the_shortcut_buttons(window):
    """
    Applies the shortcut buttons to the window
    :param window: to apply the buttons to
    :return: the buttons applied to the window
    """
    shortcut_button_1 = Button(
        window,
        text=name_of_shortcut_button,
        width=shortcut_button_width,
        height=shortcut_button_height,
        relief=shortcut_button_relief,
        cursor=shortcut_button_cursor,
    )

    shortcut_button_2 = Button(
        window,
        text=name_of_shortcut_button,
        width=shortcut_button_width,
        height=shortcut_button_height,
        relief=shortcut_button_relief,
        cursor=shortcut_button_cursor,
    )

    shortcut_button_3 = Button(
        window,
        text=name_of_shortcut_button,
        width=shortcut_button_width,
        height=shortcut_button_height,
        relief=shortcut_button_relief,
        cursor=shortcut_button_cursor,
    )

    shortcut_button_4 = Button(
        window,
        text=name_of_shortcut_button,
        width=shortcut_button_width,
        height=shortcut_button_height,
        relief=shortcut_button_relief,
        cursor=shortcut_button_cursor,
    )

    return shortcut_button_1, shortcut_button_2, shortcut_button_3, shortcut_button_4


def apply_the_work_buttons(window):
    """
    Applies the work buttons to the window
    :param window: to apply the buttons to
    :return: the buttons applied to the window
    """
    work_button1 = Button(
        window,
        text=name_of_button1,
        width=work_button_width,
        height=work_button_height,
    )

    work_button2 = Button(
        window,
        text=name_of_button2,
        width=work_button_width,
        height=work_button_height,
    )

    work_button3 = Button(
        window,
        text=name_of_button3,
        width=work_button_width,
        height=work_button_height,
    )

    work_button4 = Button(
        window,
        text=name_of_button4,
        width=work_button_width,
        height=work_button_height,
    )

    return work_button1, work_button2, work_button3, work_button4


def apply_light_next_to_work_buttons(window):
    """
    Applies the lights next to the work buttons and creates the rectangles inside them
    :param window: to apply the lights to
    :return: the lights applied to the window and the rectangles inside them
    """
    light1 = Canvas(
        window,
        width=light_width,
        height=light_height,
        bd=0,
        highlightthickness=0,
        bg=light_background_color,
    )

    light2 = Canvas(
        window,
        width=light_width,
        height=light_height,
        bd=0,
        highlightthickness=0,
        bg=light_background_color,
    )

    light3 = Canvas(
        window,
        width=light_width,
        height=light_height,
        bd=0,
        highlightthickness=0,
        bg=light_background_color,
    )

    light4 = Canvas(
        window,
        width=light_width,
        height=light_height,
        bd=0,
        highlightthickness=0,
        bg=light_background_color,
    )

    rect1 = light1.create_rectangle(
        2, 1, 10, 39,
        fill=light_fill_color,
        outline=light_outline_color,
    )

    rect2 = light2.create_rectangle(
        2, 1, 10, 39,
        fill=light_fill_color,
        outline=light_outline_color,
    )

    rect3 = light3.create_rectangle(
        2, 1, 10, 39,
        fill=light_fill_color,
        outline=light_outline_color,
    )

    rect4 = light4.create_rectangle(
        2, 1, 10, 39,
        fill=light_fill_color,
        outline=light_outline_color,
    )

    return light1, light2, light3, light4, rect1, rect2, rect3, rect4
