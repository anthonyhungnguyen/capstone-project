import os
import logging


def setup_logger(logger_name, log_file, level="INFO"):
    l = logging.getLogger(logger_name)
    template = str(
        "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s")
    formatter = logging.Formatter(template)
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

    if level == "NOTSET":
        l.setLevel(logging.NOTSET)
    elif level == "DEBUG":
        l.setLevel(logging.DEBUG)
    elif level == "INFO":
        l.setLevel(logging.INFO)
    elif level == "WARNING":
        l.setLevel(logging.WARNING)
    elif level == "ERROR":
        l.setLevel(logging.ERROR)
    elif level == "CRITICAL":
        l.setLevel(logging.CRITICAL)
    else:
        l.setLevel(logging.INFO)

    return l
