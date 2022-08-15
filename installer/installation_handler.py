from os.path import join
import subprocess

from .http_request_handler import HttpRequestHandler

from .helper import Helper
from .constants import Constants, ErrorCode, RouterInfo
from .streamline_json import StreamLineJson
from .service_logger import ServiceLogger
from .database_interface import DatabaseInterface


# ==============================================================================
# AutoInstaller
# ==============================================================================

class AutoInstaller():
    '''
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
    def __init__(self):
        self.db_obj = DatabaseInterface()

# |----------------------End of get_script_name-------------------------------|

# |----------------------------------------------------------------------------|
# driver_method_for_installation
# |----------------------------------------------------------------------------|
    def driver_method_for_installation(self, input_json):
        '''
            This is a driver method which will exceute commnds in a seuqnce.
            It extracts data from the incoming data and find out the each
            systems information that user sent.

            We will split system_id to get the system type. By knowing this
            system_type it will send commands for installation.
            
            This also will find out the current system information such as is
            it on CMS / CLUSTER / SCANNER. Based on this it triggers proper APIs.
            
        '''
        try:
            systems_info = input_json["systems"]

            for system in systems_info:
                # Access system_id and split the values
                system_id = system["system_id"]
                system_id_split_data = system_id.split("_")
                ServiceLogger.get().log_debug("Split system info: {}".
                                              format(system_id_split_data))
                if system_id_split_data[0] == "cms":
                    # Spawn update installer.
                    self.spawn_installer(system["repos"], "cms")

                elif system_id_split_data[0] == "cs":
                    # Check whether it is on same system.
                    # Get cluster ip from DB.
                    cluster_system_info_from_db = self.db_obj.\
                        get_system_info_on_system_id(system_id)

                    # Check whether host is of current system
                    cluster_host_status =\
                        self.is_current_system_host(cluster_system_info_from_db.host)

                    if cluster_host_status:
                        # Spawn update installer.
                        self.spawn_installer(system["repos"], "cluster")
                    else:
                        # Post request to cluster from cms to update repos
                        input_data = {
                            "systems": system
                        }
                        self.api_call_to_update_service(cluster_system_info_from_db.dns,
                                                        input_data)
                else:
                    # Check whether scanner host and current host are same.
                    scanner_system_info_from_db = self.db_obj.\
                        get_system_info_on_system_id(system_id)
                    scanner_host_status =\
                        self.is_current_system_host(scanner_system_info_from_db.host)

                    if scanner_host_status:
                        # Spawn update installer.
                        self.spawn_installer(system["repos"], "scanner")
                    else:
                        # Check whether cluster host and current host are same
                        cluster_id = "cs_" + system_id_split_data[-2]
                        cluster_system_info_from_db = self.db_obj.\
                            get_system_info_on_system_id(cluster_id)
                        cluster_host_status =\
                            self.is_current_system_host(cluster_system_info_from_db.host)

                        if cluster_host_status:
                            # Post request to scanner from cluster to update repos
                            input_data = {
                                "systems": system
                            }
                            self.api_call_to_update_service(scanner_system_info_from_db.dns,
                                                            input_data)
                        else:
                            # Post request to cluster to from cms to update repos
                            input_data = {
                                "systems": system
                            }
                            self.api_call_to_update_service(cluster_system_info_from_db.dns,
                                                            input_data)

        except Exception as error:
            ServiceLogger.get().log_exception(error)

            actual_err_msg, error_class = StreamLineJson.\
                get_error_info(error)
            error_details = StreamLineJson().get_json(
                    "error", ErrorCode.GENERAL_ERROR.value,
                    actual_err_msg
                )

            # Post scanner error to UI.
            error_json = {
                    "error_info": error.args[0],
                    "error_code": ErrorCode.GENERAL_ERROR.value,
                    "error_details": error_details
                }
            # TODO: Post to UI to show this as error.

# |----------------End of driver_method_for_installation----------------------|

# |----------------------------------------------------------------------------|
# is_current_system_host
# |----------------------------------------------------------------------------|
    def is_current_system_host(self, host):
        try:
            current_system_host_list = Helper.get_host_name()

            if host in current_system_host_list:
                return True
            else:
                return False
        except Exception as error:
            return False
            ServiceLogger.get().log_exception(error)
            actual_err_msg, error_class = StreamLineJson.\
                get_error_info(error)
            error_details = StreamLineJson().get_json(
                    "error", ErrorCode.GENERAL_ERROR.value,
                    actual_err_msg
                )

            # Post scanner error to UI.
            error_json = {
                    "error_info": error.args[0],
                    "error_code": ErrorCode.GENERAL_ERROR.value,
                    "error_details": error_details
                }
            # TODO: Post to UI to show this as error.

# |--------------------End of is_current_system_host----------------------------|

# |----------------------------------------------------------------------------|
# spawn_installer
# |----------------------------------------------------------------------------|
    def spawn_installer(self, repo_list, system_type):
        try:
            # Write repos information to disk and spawn a script
            # to update installer.
            repo_obj = {
                "repos": repo_list
            }
            repo_json_path = join(Constants.CONFIG_PATH, "repo_list.json")
            Helper.write_json(repo_json_path, repo_obj)

            # Spawn update utility
            subprocess.Popen(["python3", Constants.
                              CODE_UPADATE_UTILITY_SCRIPT_PATH, system_type])
        except Exception as error:
            ServiceLogger.get().log_exception(error)
            actual_err_msg, error_class = StreamLineJson.\
                get_error_info(error)
            error_details = StreamLineJson().get_json(
                    "error", ErrorCode.GENERAL_ERROR.value,
                    actual_err_msg
                )

            # Post scanner error to UI.
            error_json = {
                    "error_info": error.args[0],
                    "error_code": ErrorCode.GENERAL_ERROR.value,
                    "error_details": error_details
                }
            # TODO: Post to UI to show this as error.

# |--------------------End of spawn_installer----------------------------|

# |----------------------------------------------------------------------------|
# api_call_to_update_service
# |----------------------------------------------------------------------------|
    def api_call_to_update_service(self, host, input_data):
        try:
            http_obj = HttpRequestHandler()
            http_obj.post_request(RouterInfo.UPDATE_REPO.value, host,
                                  Constants.UPDATE_SERVICE_PORT,
                                  input_data)
        except Exception as error:
            ServiceLogger.get().log_exception(error)
            actual_err_msg, error_class = StreamLineJson.\
                get_error_info(error)
            error_details = StreamLineJson().get_json(
                    "error", ErrorCode.GENERAL_ERROR.value,
                    actual_err_msg
                )

            # Post scanner error to UI.
            error_json = {
                    "error_info": error.args[0],
                    "error_code": ErrorCode.GENERAL_ERROR.value,
                    "error_details": error_details
                }
            # TODO: Post to UI to show this as error.

# |--------------End of api_call_to_update_service----------------------------|
