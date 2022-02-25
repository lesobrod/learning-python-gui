class ResponseError(Exception):
    """Non-fatal errors of requests"""
    pass



LOGGER_CONFIG = {
    "handlers": [
        {
            "sink": "log.log",
            "format": "{level} | {time:YYYY-MMM-D HH:mm:ss} | {message}",
            "encoding": "utf-8",
            "level": "DEBUG",
            "rotation": "5 MB",
            "compression": "zip"
        },
    ],
}

GEOPOS_API_KEY = '625198479955388839225x120179'

# GUI CONSTANTS
NORTH_PACK_PARAMS = {'side': 'right',
                     'padx': 10,
                     'pady': 10,
                     'anchor': 'nw'}
GUI_SIZE = "700x600"
ENTRY_COLOR = "#bfbfbf"
ENTRY_FONT = "Helvetica 12"
BUTTON_COLOR = "#a3aed9"
BACK_COLOR = "#c9ccd6"
GUI_TITLE = "What are seasons?"
WELCOME_MESSAGE = 'Bla bla bal bla labba lab ba'

MONTHS = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
          'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
          'JAN'
          )
