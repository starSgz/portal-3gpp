# -*-coding:utf-8-*-
"""
This is to get loggrr
"""
import os
import logging
import time


class Logger(object):
    """
    This is get log class
    """

    def __init__(self, path, name, Flevel=logging.DEBUG):
        self.time = time.strftime("%Y-%m-%d")
        self.fileName = path + name + "-" + self.time + ".log"
        self.logger = logging.getLogger(self.fileName)
        self.logger.setLevel(Flevel)
        fmt = logging.Formatter('[%(asctime)s %(threadName)s][ % (levelname)s] % (message)s', ' % Y - % m - % d % H: % M: % S')
        fh = logging.FileHandler(self.fileName)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(fh)

    def debug(self, message):
        """
        This is debug
        """
        self.logger.debug(message)

    def info(self, message):
        """
        This is info
        """
        self.logger.info(message)

    def warn(self, message):
        """
        This is warn
        """
        self.logger.warn(message)

    def error(self, message):
        """
        This is error
        """
        self.logger.error(message)

    def critical(self, message):
        """
        This is critical
        """
        self.logger.critical(message)


if __name__ == '__main__':
    logyyx = Logger("/home/map/workspace/zhangxianrong / crawl - brand / lib / ", "meizu")
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.warn('一个warning信息')
    logyyx.error('一个error信息')
    logyyx.critical('一个致命critical信息')