from loguru import logger
import tkinter
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as plt_bck
from request_api import get_data
from config import *
import time


def zero_days(data: list, mean: float) -> list:
    """
    :param data: list of values
    :param mean: float mean of data
    :return: list of mean-line crossing
    """
    res = []
    prev_value = data[0]
    for index, value in enumerate(data[1:]):
        if (prev_value - mean) * (value - mean) < 0:
            res.append(index)
        prev_value = value
    return res


class MyButton(tkinter.Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = root
        self.configure(width=20,
                       height=2,
                       bg=BUTTON_COLOR)


class MyEntry(tkinter.Entry):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = root
        self.configure(width=15,
                       bg=ENTRY_COLOR,
                       font=ENTRY_FONT)


class MyLabel(tkinter.Label):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = root
        self.configure(width=12,
                       height=1,
                       bg='#ffffff')


class MyFigure(plt.Figure):
    def __init__(self):
        super().__init__(figsize=(8, 5),
                         dpi=80)


class MyCanvas(plt_bck.FigureCanvasTkAgg):
    def __init__(self, figure, root):
        super().__init__(figure, root)
        self.draw()
        self.get_tk_widget().place_forget()


class MyApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(GUI_SIZE)
        self.wm_title(GUI_TITLE)
        # Quit button on bottom
        self.button_quit = MyButton(self, text="Quit", command=self.quit_gui)
        self.button_quit.configure(bg="#d1b6bd")
        self.button_quit.pack(side='bottom', pady=10)

        self.button_plot = MyButton(self, text="Plot", command=self.plot_data)

        self.label_year = MyLabel(self, text='Year: ')
        self.label_city = MyLabel(self, text='City: ')
        self.entry_year = MyEntry(self)
        self.entry_year.configure(width=10)
        self.entry_city = MyEntry(self)

        self.button_plot.pack(**NORTH_PACK_PARAMS)
        self.entry_city.pack(**NORTH_PACK_PARAMS)
        self.entry_city.insert('end', 'london')
        self.label_city.pack(**NORTH_PACK_PARAMS)
        self.entry_year.pack(**NORTH_PACK_PARAMS)
        self.entry_year.insert('end', '2000')
        self.label_year.pack(**NORTH_PACK_PARAMS)

        self.info_label = MyLabel(self)
        self.info_label.configure(width=33,
                                  height=12,
                                  wraplength=300,
                                  bg='#ffffff',
                                  font=("Courier", 13))
        self.info_label.place(relx=0.5, rely=0.5, anchor='center')
        self.info_label['text'] = WELCOME_MESSAGE

        self.figure = MyFigure()
        self.canvas = MyCanvas(self.figure, self)

    def quit_gui(self):
        # Correct exit GUI
        logger.info('Quit GUI')
        self.quit()
        self.destroy()

    def get_user_data(self) -> list:

        try:
            user_year = self.entry_year.get()
            if not user_year.isdigit() or int(user_year) < 1990 or int(user_year) > 2021:
                raise ValueError('Year must be a number between 1990 and 2021')
            user_city = self.entry_city.get()
            if not user_city.isalpha():
                raise ValueError('City name is not valid')
            data = get_data(int(user_year), user_city)

        except (ResponseError, SystemExit, ValueError) as e:
            logger.error(e)
            return [e]

        else:
            return data

    def plot_data(self):

        data = self.get_user_data()

        if len(data) == 1:
            self.canvas.get_tk_widget().place_forget()
            self.info_label.place(relx=0.5, rely=0.5, anchor='center')
            self.info_label.config(bg='#ba9396',
                                   font=("Courier", 15),
                                   text=data[0])
            return
        self.info_label.place_forget()
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor='center')
        ax = self.figure.add_subplot(111)
        args = range(len(data))
        mean = sum(data) / len(data)
        cross_days = zero_days(data, mean)
        cross_values = [mean for _ in cross_days]
        ax.axhline(y=mean, color='r', linestyle='-', linewidth=1.5, zorder=10)
        ax.scatter(cross_days, cross_values, marker='s', color='r', zorder=5)
        ax.plot(args, data, linewidth=0.5, zorder=0)
        self.canvas.draw()
        ax.set_xticks(range(0, len(data) + 1, len(data) // 12))
        ax.set_xticklabels(MONTHS)
        ax.grid(which='both', axis='x')


def show_gui():
    logger.info('Run GUI')
    root = MyApp()
    root.mainloop()
