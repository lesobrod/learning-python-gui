import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from request_api import get_data
from config import GUI_SIZE, GUI_TITLE, MONTHS, ResponseError


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


def show_gui():
    def get_user_data() -> list:
        user_year = int(entry_year.get())
        user_city = entry_city.get()
        try:
            data = get_data(user_year, user_city)
        except ResponseError as e:
            print(e)
        else:
            return data

    def plot_data() -> plt.figure:
        # print(data)
        data = get_user_data()
        args = range(len(data))

        fig = plt.figure(figsize=(8, 5), dpi=80)
        ax = fig.add_subplot(111)

        mean = sum(data) / len(data)
        cross_days = zero_days(data, mean)
        cross_values = [mean for _ in cross_days]
        ax.axhline(y=mean, color='r', linestyle='-', linewidth=1.5, zorder=10)
        ax.scatter(cross_days, cross_values, marker='s', color='r', zorder=5)
        ax.plot(args, data, linewidth=0.5, zorder=0)

        ax.set_xticklabels(MONTHS)
        ax.grid(which='major', axis='x')
        return fig

    def show_plot():
        # Show plot inside gui
        fig = plot_data()
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().place(x=20, y=40)


    def quit_gui():
        # Correct exit GUI
        root.quit()
        root.destroy()

    root = tkinter.Tk()
    root.geometry(GUI_SIZE)
    root.wm_title(GUI_TITLE)

    # Create elements
    button_plotdata = tkinter.Button(master=root, width=15, height=2,
                                     text="PLot", command=show_plot)
    button_plotdata.place(x=420, y=10)
    button_quit = tkinter.Button(master=root, width=15, height=2,
                                 text="Quit", command=quit_gui)
    button_quit.place(x=300, y=450)

    entry_year = tkinter.Entry(master=root, width=20)
    entry_year.place(x=20, y=20)
    entry_city = tkinter.Entry(master=root, width=30)
    entry_city.place(x=200, y=20)

    tkinter.mainloop()
