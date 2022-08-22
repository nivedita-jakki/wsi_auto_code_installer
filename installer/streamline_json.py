from datetime import datetime
import json
import os
import sys
from pathlib import Path
from os.path import join
import subprocess
from installer.service_logger import ServiceLogger


class StreamLineJson:

    def __init__(self, api_name="", entity_type="general", slide_id=""):
        self.api_name = api_name
        self.entity_type = entity_type
        self._service_name = "auto_installer"
        self.slide_id = slide_id
        self.init_maps()

    def init_maps(self):

        self.error_map = {
            "DatabaseError": "SCDJ_DB_ERROR",
            "JSONDecodeError": "SCDJ_FAILED_TO_DECODE_JSON"
        }

    def get_pos_from_ip(self, ip):
        try:
            position = int(ip.split(".")[3]) - 5
            return position
        except Exception as error_msg:
            return -1

    def get_service_version(self):
        os.chdir(os.getcwd())
        git_branch = "git branch | sed -n '/\* /s///p'"
        try:
            output = subprocess.check_output(git_branch, shell=True)
            branch = output.decode().strip()
            values = branch.split(" ")
            if len(values) > 1:
                return values[-1][:-1]
            else:
                return values[-1]
        except Exception as e:
            ServiceLogger.get().log_exception(e)
            return None

    def get_error_code(self, exception_class):
        '''
        fetch error codes for the exception class
        '''
        error_code = "E-500"
        if exception_class in self.error_map.keys():
            error_code = self.error_map[exception_class]
        return error_code

    def get_service_log_file_path(self):
        home_path = str(Path.home())
        service_log_path = join(home_path, "service_logs", self._service_name)
        now = datetime.utcnow()
        service_log_filename = "{}.log".format(now.date())
        service_log_file_path = join(service_log_path,
                                     service_log_filename)
        return service_log_file_path

    def get_json(self, status, error_code="", error_info="", entity_id="-"):
        if status is False:
            status = "error"
        json =\
            {
                    "entity_id": entity_id,
                    "entity_type": self.entity_type,
                    "status": status,
                    "error_code": error_code,
                    "service_name": self._service_name,
                    "error_root_cause": error_info,
                    "api_name": self.api_name,
                    "service_version": self.get_service_version(),
                    "logs_path": ServiceLogger.get().get_new_logger_path()
            }

        return json

    @staticmethod
    def get_cluster_name():
        config_path = join(str(Path.home()), "wsi_app", "etc",
                           "calib_data", "config")
        cluster_path = join(config_path, "cluster_info.json")
        cluster_name = ""
        try:
            with open(cluster_path, 'r') as file:
                cluster_json = json.loads(file.read())
                if cluster_json is not None:
                    cluster_name = cluster_json["cluster_name"]
                else:
                    cluster_name = cluster_json
        except Exception as error_msg:
            raise error_msg
        return cluster_name

    @staticmethod
    def get_error_info(msg):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = exc_tb.tb_frame.f_code.co_filename
        print("Exception occured at ", exc_tb.tb_lineno, " in ",
              fname, "Error is ", msg)
        error_msg = \
            (f'Exception is: {msg}, exception type: {exc_type.__name__},' +
             f'execption obj: {exc_obj}, file name: {fname},' +
             f'line number: {exc_tb.tb_lineno}')

        return error_msg, exc_type

    @staticmethod
    def get_status_code(exception_class):
        if exception_class == "JSONDecodeError":
            return 400
        return 500
