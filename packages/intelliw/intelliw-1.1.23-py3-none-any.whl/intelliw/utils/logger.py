#!/usr/bin/env python
# coding: utf-8
from intelliw.config import config
import logging.handlers
import time
import os


def __get_loger(logger_type):
    if config.is_server_mode:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logger = logging.getLogger(logger_type)
    logger.setLevel(level=level)
    log_format = logging.Formatter(f'[{logger_type}] %(asctime)s %(levelname)50s %(filename)s:%(lineno)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    # print log to file
    log_path = './logs/'
    file_name = 'iw-algo-fx.log' if logger_type == 'Framework Log' else 'iw-algo-fx-user.log'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    time_file_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(log_path, file_name),
        when='D',
        interval=2,
        backupCount=180
    )
    time_file_handler.suffix = '%Y-%m-%d-%H.log' 
    time_file_handler.setLevel(level)
    time_file_handler.setFormatter(log_format)

    # print log to console
    log_format = logging.Formatter(f'[{logger_type}] %(levelname)s %(asctime)s %(filename)s:%(lineno)s: %(message)s', datefmt='%H:%M:%S')
    console = logging.StreamHandler()
    console.setFormatter(log_format)
    console.setLevel(level)

    logger.addHandler(time_file_handler)
    logger.addHandler(console)
    return logger

framework_logger = None
user_logger = None

def get_logger():
    global framework_logger
    if framework_logger is None:
        framework_logger = __get_loger("Framework Log")
    return framework_logger

def get_user_logger():
    global user_logger
    if user_logger is None:
        return __get_loger("Algorithm Log")
    return user_logger