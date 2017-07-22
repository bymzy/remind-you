import logging

class Log(object):
    def __init__(self, logFile):
        self.logFile = logFile
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d] - %(message)s', filename = logFile, level = logging.DEBUG, filemode='a');

    def debug_log(self, log):
        logging.debug(log)

    def info_log(self, log):
        logging.info(log)

    def warn_log(self, log):
        logging.warning(log)

