from gui_oop import show_gui
from loguru import logger
from config import LOGGER_CONFIG

logger.configure(**LOGGER_CONFIG)

show_gui()
