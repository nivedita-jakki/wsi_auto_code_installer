import subprocess
import json

from .service_logger import ServiceLogger


# ==============================================================================
# Helper
# ==============================================================================
class Helper():
    '''
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
    def __init__(self):
        pass

# |----------------------End of get_script_name-------------------------------|

# |----------------------------------------------------------------------------|
# get_system_host
# |----------------------------------------------------------------------------|
    def get_system_host(self):
        resp = subprocess.check_output(['hostname', '-I'])
        resp_str = resp.decode('utf-8')
        resp_str_list = resp_str.split()

        return resp_str_list[0]

# |----------------------End of get_system_host------------------------------|

# |----------------------------------------------------------------------------|
# write_json
# |----------------------------------------------------------------------------|
    @staticmethod
    def write_json(file_path, data):
        try:
            with open(file_path, 'w') as file:
                js = json.dumps(data, sort_keys=True, indent=2)
                file.write(js)
            file.close()
            return True
        except Exception as msg:
            ServiceLogger.get().log_exception(msg)
            return False

# |----------------------End of write_json------------------------------------|

# |----------------------------------------------------------------------------|
# get_host_name
# |----------------------------------------------------------------------------|
    @staticmethod
    def get_host_name(self):
        resp = subprocess.check_output(['hostname', '-I'])
        resp_str = resp.decode('utf-8')
        resp_str_list = resp_str.split()
        return resp_str_list

# |----------------------End of get_host_name----------------------------------|
