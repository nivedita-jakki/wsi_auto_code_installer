import os
import logging
import time
from os.path import join, exists
from pathlib import Path
import glob
from datetime import datetime
import sys

# ==============================================================================
# ServiceLogger
# ==============================================================================


class ServiceLogger():
    '''
    Interface method to log data for this service
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
    _singleton = None

# |----------------------------------------------------------------------------|
# Constructor
# |----------------------------------------------------------------------------|
    def __init__(self):
        if ServiceLogger._singleton is not None:
            raise Exception("ServiceLogger is a singleton class")
        else:
            ServiceLogger._singleton = self
            self._service_name = ""

# |---------------------------End of Constructor------------------------------|

# |----------------------------------------------------------------------------|
# get
# |----------------------------------------------------------------------------|
    @staticmethod
    def get():
        if ServiceLogger._singleton is None:
            ServiceLogger()
        return ServiceLogger._singleton

# |------------------------------End of get-----------------------------------|

# |----------------------------------------------------------------------------|
# get_new_logger_path
# |----------------------------------------------------------------------------|
    def get_new_logger_path(self):
        home_path = str(Path.home())
        service_log_path = join(home_path, "service_logs", self._service_name)

        if not exists(service_log_path):
            os.makedirs(service_log_path, exist_ok=True)

        now = datetime.utcnow()
        service_log_filename = "{}.log".format(now.date())
        service_log_file_path = join(service_log_path,
                                     service_log_filename)
        # self.set_logger_for_filehandler(service_log_file_path)
        return service_log_file_path

# |----------------------End of get_new_logger_path--------------------------|

# |----------------------------------------------------------------------------|
# initialize
# |----------------------------------------------------------------------------|
    def initialize(self, service_name):
        self._service_name = service_name
        # home_path = join("/var", "www")
        home_path = join("/home", "adminspin")
        service_log_path = join(home_path, "service_logs", self._service_name)

        if not exists(service_log_path):
            os.makedirs(service_log_path, exist_ok=True)

        date_change_status, service_log_file_path = self.is_date_changed()
        if date_change_status:
            now = datetime.utcnow()
            service_log_filename = "{}.log".format(now.date())
            service_log_file_path = join(service_log_path,
                                         service_log_filename)

        self.set_logger_for_filehandler(service_log_file_path)

# |----------------------End of initialize-----------------------------------|

# |----------------------------------------------------------------------------|
# set_logger_for_filehandler
# |----------------------------------------------------------------------------|
    def set_logger_for_filehandler(self, service_log_file_path,
                                   date_changed=True):
        # Create the logger.
        logger = logging.getLogger(self._service_name)
        logger.setLevel(logging.DEBUG)
        # Convert local time zone into UTC time format.
        logging.Formatter.converter = time.gmtime

        # Create formatter.
        formatter = logging.Formatter("[%(name)s] [%(asctime)s] "
                                      "[%(levelname)s] : %(message)s",
                                      datefmt='%d/%m/%Y %I:%M:%S %p')

        if date_changed is True:
            # Create console handler and set level to debug.
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        fh = logging.FileHandler(service_log_file_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

# |---------------------End of set_logger_for_filehandler---------------------|

# |----------------------------------------------------------------------------|
# log_debug
# |----------------------------------------------------------------------------|
    def log_debug(self, log_msg):
        if self._service_name:
            # Check whether date changed or not.
            date_change_status, service_log_file_path = self.is_date_changed()
            if date_change_status:
                self.close_log_file()
                service_log_path = self.get_new_logger_path()
                self.set_logger_for_filehandler(service_log_path,
                                                date_changed=False)
            logger = logging.getLogger(self._service_name)
            logger.debug("{}".format(log_msg))

# |----------------------End of log_debug-------------------------------------|

# |----------------------------------------------------------------------------|
# log_info
# |----------------------------------------------------------------------------|
    def log_info(self, log_msg):
        if self._service_name:
            # Check whether date changed or not.
            date_change_status, service_log_file_path = self.is_date_changed()
            if date_change_status:
                self.close_log_file()
                service_log_path = self.get_new_logger_path()
                self.set_logger_for_filehandler(service_log_path,
                                                date_changed=False)

            logger = logging.getLogger(self._service_name)
            logger.info("{}".format(log_msg))

# |----------------------End of log_info--------------------------------------|

# |----------------------------------------------------------------------------|
# log_error
# |----------------------------------------------------------------------------|
    def log_error(self, log_msg):
        if self._service_name:
            # Check whether date changed or not.
            date_change_status, service_log_file_path = self.is_date_changed()
            if date_change_status:
                self.close_log_file()
                service_log_path = self.get_new_logger_path()
                self.set_logger_for_filehandler(service_log_path,
                                                date_changed=False)

            logger = logging.getLogger(self._service_name)
            logger.error("{}".format(log_msg))

# |----------------------End of log_error-------------------------------------|

# |----------------------------------------------------------------------------|
# log_exception
# |----------------------------------------------------------------------------|
    def log_exception(self, log_msg):
        if self._service_name:
            # Check whether date changed or not.
            date_change_status, service_log_file_path = self.is_date_changed()
            if date_change_status:
                self.close_log_file()
                service_log_path = self.get_new_logger_path()
                self.set_logger_for_filehandler(service_log_path,
                                                date_changed=False)

            logger = logging.getLogger(self._service_name)
            logger.exception("{}".format(log_msg))

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            self.log_error("Exception occured at {} in {} ".
                           format(exc_tb.tb_lineno, fname))

# |----------------------End of log_exception--------------------------------|

# |----------------------------------------------------------------------------|
# is_date_changed
# |----------------------------------------------------------------------------|
    def is_date_changed(self):
        home_path = str(Path.home())
        service_log_path = join(home_path, "service_logs", self._service_name)

        folder_path = service_log_path
        list_of_files = glob.glob(folder_path + "/*.log")

        if len(list_of_files) > 0:
            latest_file = max(list_of_files)
            latest_file_time = latest_file[
                latest_file.rfind('/') + 1:].strip("\n")

            latest_date = latest_file_time[
                0:latest_file_time.rfind('.log')].strip("\n")
            previous_date = datetime.strptime(latest_date, '%Y-%m-%d').date()
            current_date = datetime.utcnow().date()
            date_change_status = current_date > previous_date

            return date_change_status, latest_file
        else:
            return True, ""

# |----------------------End of is_date_changed-----------------------------|

# |----------------------------------------------------------------------------|
# close_log_file
# |----------------------------------------------------------------------------|
    def close_log_file(self):
        log_obj = logging.getLogger(self._service_name)
        log_obj.handlers.clear()

# |----------------------End of close_log_file--------------------------------|
