import json


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
        try:
            data_str = request.body.decode('utf-8')
            data_json = json.loads(data_str)
        except Exception as error_msg:


# |----------------------End of is_request_payload_corrupted----------------|