import logging
from logging.handlers import TimedRotatingFileHandler

# Log Config
FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')
LOG_FILE = 'remoteDAQ.log'

'''Log File Handler'''
def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler

'''Main Log Handler'''
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG)
   logger.addHandler(get_file_handler())
   logger.propagate = False
   return logger