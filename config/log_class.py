import logging.config
import os
from datetime import datetime
# import datetime
from PyQt5.QtCore import *


class Logging():
    def __init__(self, name):
        # self.config_path = 'config/logging.conf'
        self.config_path = os.path.join(os.path.dirname(__file__), "logging.conf")
        # self.log_path = 'log'
        self.name = name
        kiwoom_log_file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log/kiwoom.log")
        trading_log_file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log/trading.log")

        logging.config.fileConfig(self.config_path, disable_existing_loggers=False,
                                  defaults={"kiwoom_log_file_name": kiwoom_log_file_name,
                                            "trading_log_file_name": trading_log_file_name})

        # logging.config.fileConfig(self.config_path)
        self.logger = logging.getLogger(self.name)
        # self.handler_file()

    # #로그설정
    # def handler_file(self):
    #     now = datetime.now().strftime("%Y-%m-%d")
    #     file = logging.FileHandler(self.log_path+'/{0:s}_{1:s}.log'.format(now, self.name), encoding='utf-8')
    #     formatter = logging.Formatter('[%(asctime)s] %(filename)s | %(name)s | %(funcName)s | %(lineno)04d | %(levelname)-8s > %(message)s')
    #
    #     file.setFormatter(formatter)
    #     self.logger.addHandler(file)

    # def emit(self, record):
    #     """
    #     Emit a record.
    #
    #     If a formatter is specified, it is used to format the record.
    #     The record is then written to the stream with a trailing newline.  If
    #     exception information is present, it is formatted using
    #     traceback.print_exception and appended to the stream.  If the stream
    #     has an 'encoding' attribute, it is used to determine how to do the
    #     output to the stream.
    #     """
    #     try:
    #         msg = self.format(record)
    #         stream = self.stream
    #         # issue 35046: merged two stream.writes into one.
    #         stream.write(msg + self.terminator)
    #         print("A")
    #         self.flush()
    #     except RecursionError:  # See issue 36272
    #         raise
    #     except Exception:
    #         self.handleError(record)
