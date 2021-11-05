import os
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter
import datetime


def initialize_logger(logging_level=logging.INFO, output_dir="/Logs", filename=None, save_log=True):
    logger = getLogger()
    logger.setLevel(logging_level)

    handler_format = Formatter(
        '%(asctime)s.%(msecs)03d [%(levelname)s] (%(filename)s:%(lineno)s) %(message)s',
        "%H:%M:%S")  # If you want to show date, add %Y-%m-%d
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging_level)
    stream_handler.setFormatter(handler_format)

    if save_log:
        if filename is not None:
            filename = filename
        else:
            if not os.path.exists(os.path.dirname(os.getcwd()) + '/Logs/'):
                os.mkdir(os.path.dirname(os.getcwd()) + '/Logs/')
            filename = os.path.join(
                os.path.dirname(os.getcwd()) + '/Logs/', datetime.datetime.now().strftime("%Y%m%dT%H%M%S.%f") + '.log')

        file_handler = FileHandler(filename, 'a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(handler_format)

    if len(logger.handlers) == 0:
        logger.addHandler(stream_handler)
        if save_log:
            logger.addHandler(file_handler)
    else:
        # Overwrite logging setting
        logger.handlers[0] = stream_handler
        if save_log:
            logger.handlers[1].close()
            logger.handlers[1] = file_handler

    logger.propagate = False

    return logger
