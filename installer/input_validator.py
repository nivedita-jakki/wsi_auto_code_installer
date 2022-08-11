import json

from installer.streamline_json import StreamLineJson
from installer.service_logger import ServiceLogger
from installer.constants import ErrorCode


# ==============================================================================
# InputValidator
# ==============================================================================
class InputValidator():
    '''
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
    def __init__(self):
        pass

# |----------------------End of get_script_name-------------------------------|

# |----------------------------------------------------------------------------|
# is_valid_json
# |----------------------------------------------------------------------------|
    def is_valid_json(self):
        # TODO
        return True

# |----------------------End of is_valid_json------------------------------|

# |----------------------------------------------------------------------------|
# is_request_payload_corrupted
# |----------------------------------------------------------------------------|
    def is_request_payload_corrupted(self, request):
        error_details = data_json = {}
        try:
            data_str = request.body.decode('utf-8')
            data_json = json.loads(data_str)
        except Exception as error_msg:
            ServiceLogger.get().log_exception(error_msg)
            actual_msg, err_class = StreamLineJson.get_error_info(error_msg)
            error_details = StreamLineJson.get_json(
                "error", ErrorCode.GENERAL_ERROR.value, actual_msg)

            return False, data_json, error_details

        return True, data_json, error_details

# |----------------------End of is_request_payload_corrupted------------------|
