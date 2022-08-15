import json

from installer.streamline_json import StreamLineJson
from installer.service_logger import ServiceLogger
from installer.constants import ErrorCode
from installer.constants import RouterInfo


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
# is_payload_valid
# |----------------------------------------------------------------------------|
    def is_payload_valid(self, api, payload):
        try:
            if api == RouterInfo.UPDATE_REPO.value:
                return self.is_payload_valid_for_api_update_repos(payload)
            else:
                return True
        except Exception as err_msg:
            raise err_msg

# |----------------------End of is_payload_valid----------------------------|

# |----------------------------------------------------------------------------|
# is_payload_valid_for_api_update_repos
# |----------------------------------------------------------------------------|
    def is_payload_valid_for_api_update_repos(self, payload):
        if "systems" in payload:
            return True
        else:
            raise Exception("key systems missed")

# |--------End of is_payload_valid_for_api_update_repos-----------------------|

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
