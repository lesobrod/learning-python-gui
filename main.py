from matplotlib.figure import Figure
from request_api import get_data
from plot import plot_data
from config import ResponseError


try:
    data = get_data(2016,'Panama')
except ResponseError as e:
    print(e)
else:
    plot_data(data)

