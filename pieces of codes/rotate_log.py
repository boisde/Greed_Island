import os
import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler

VERSION = "8.5.2"


class TimedRotatingFileHandlerCustomHeader(TimedRotatingFileHandler):
    def __init__(self, filename, when='S', interval=10, backupCount=0, encoding=None, delay=False, utc=False, header_msg=None):
        super(TimedRotatingFileHandlerCustomHeader, self).__init__(filename, when, interval, backupCount, encoding, delay, utc)
        self.suffix = "%Y-%m-%d_%H-%M-%S.log"
        self.header_msg = header_msg

    def computeRollover(self, currentTime):
        return super(TimedRotatingFileHandlerCustomHeader, self).computeRollover(currentTime)

    def getFilesToDelete(self):
        return super(TimedRotatingFileHandlerCustomHeader, self).getFilesToDelete()

    def shouldRollover(self, record):
        return super(TimedRotatingFileHandlerCustomHeader, self).shouldRollover(record)

    def doRollover(self):
        super(TimedRotatingFileHandlerCustomHeader, self).doRollover()

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:
            if self.shouldRollover(record):
                self.doRollover()
                if self.header_msg is not None:
                    for msg in self.header_msg:
                        header_record = logging.LogRecord("", 20, "", 0, msg, (), None, None)
                        logging.FileHandler.emit(self, header_record)
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class RotatingFileHandlerCustomHeader(logging.handlers.RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0, utc=False, header_msg=None):
        super(RotatingFileHandlerCustomHeader, self).__init__(filename, mode, maxBytes, backupCount, encoding, delay)
        self.suffix = "%Y-%m-%d_%H-%M-%S.log"
        self.ext_match = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
        self.utc = utc
        self.header_msg = header_msg

    def get_files_to_delete(self):
        # Determine the files to delete when rolling over.
        dir_name, base_name = os.path.split(self.baseFilename)
        file_names = os.listdir(dir_name)
        result = []
        prefix = base_name + "."
        prefix_len = len(prefix)
        for fileName in file_names:
            if fileName[:prefix_len] == prefix:
                suffix = fileName[prefix_len:]
                if self.ext_match.match(suffix):
                    result.append(os.path.join(dir_name, fileName))
        result.sort()
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        if self.utc:
            time_tuple = time.gmtime()
        else:
            time_tuple = time.localtime()
        dfn = self.baseFilename + "." + time.strftime(self.suffix, time_tuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        # Issue 18940: A file may not have been created if delay is True.
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.get_files_to_delete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()

    def shouldRollover(self, record):
        return super(RotatingFileHandlerCustomHeader, self).shouldRollover(record)

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:
            if self.shouldRollover(record):
                self.doRollover()
                if self.header_msg is not None:
                    for msg in self.header_msg:
                        header_record = logging.LogRecord("", 20, "", 0, msg, (), None, None)
                        logging.FileHandler.emit(self, header_record)
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

if __name__ == "__main__":

    print time.strftime("%Y-%m-%d_%H-%M-%S.log")

    LOGGING_MSG_FORMAT = '%(name)-14s > [%(levelname)s] [%(asctime)s] : %(message)s'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(
                stream=sys.stdout,
                level=logging.DEBUG,
                format=LOGGING_MSG_FORMAT,
                datefmt=LOGGING_DATE_FORMAT
                )

    backup_msg = "Recording Processor Backed Up [7] messages."
    version_msg = str("Recording Processor Version %s" % VERSION)
    header_msg = [backup_msg, version_msg]

    logs_path = os.getcwd()
    test_logger = logging.getLogger()
    test_logger_file = os.path.join(logs_path, "rotate_logging_test")
    # ch = TimedRotatingFileHandlerCustomHeader(test_logger_file, when='s', interval=2, backupCount=0, encoding=None, delay=False, utc=False, header_msg=header_msg)
    ch = RotatingFileHandlerCustomHeader(test_logger_file, mode='a', maxBytes=10, backupCount=2, encoding=None, delay=0, utc=False, header_msg=header_msg)
    test_logger.addHandler(ch)

    for i in range(1, 5):
        test_logger.info("log record number [%d]." % i)
        if i % 2 == 1:
            time.sleep(2)

    ch.close()
    test_logger.removeHandler(ch)