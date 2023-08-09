import logging
from logging.handlers import TimedRotatingFileHandler

'''Log Config'''
FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')

'''Log File Handler'''
def get_file_handler(logger_name):
   file_handler = TimedRotatingFileHandler('logs/{}.log'.format(logger_name), when='midnight', backupCount=7)
   file_handler.setFormatter(FORMATTER)
   return file_handler

'''Main Log Handler'''
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.INFO)
   logger.addHandler(get_file_handler(logger_name))
   logger.propagate = False
   return logger