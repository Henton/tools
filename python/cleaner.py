import logging
import os
import sys
import datetime
import time

logger = logging.getLogger('cleaner')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Cleaner(object):

    def __init__(self, period = 7):
        self.period = period

    def clean(self, path):
        if(os.path.isdir(path)):
            files = os.listdir(path)
            for fileName in files:
                subPath = os.path.join(path, fileName)
                self.clean(subPath)
            subSize = len(os.listdir(path))
            if(subSize <= 0):
                os.rmdir(path)
                logger.debug("delete dir %s, sub file size %s", path, subSize)
            else:
                logger.debug("can not delete dir %s, sub file size %s", path, subSize)
        elif(os.path.isfile(path)):
            seconds = self.period * 24 * 60 * 60
            now = time.time()
            mtime = os.path.getmtime(path)
            if(now - mtime >= seconds):
                os.remove(path)
                logger.debug("delete file %s, last modify %s", path, datetime.datetime.fromtimestamp(mtime))
            else:
                logger.debug("can not delete file %s, last modify %s", path, datetime.datetime.fromtimestamp(mtime))

    def cleanPaths(self, paths):
        if(len(paths) <= 0):
            logger.info("paths %s is empty, no need to clean", paths)
            return
        logger.info("start to to clean paths %s", paths)
        for path in paths:
            if(not os.path.exists(path)):
                logger.warn("path %s not found", path)
                continue
            self.clean(path)
            logger.info("path %s period %s clean sucess", path, self.period)
        logger.info("paths %s clean end", paths)


if __name__ == "__main__":
    cleaner = Cleaner(365)
    cleaner.cleanPaths(["/your/path/to/delete"])
