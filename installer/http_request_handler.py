import json
import requests
from json.decoder import JSONDecodeError
from requests import RequestException

from .constants import Constants

# ==============================================================================
# HttpRequestHandler
# ==============================================================================


class HttpRequestHandler():
    '''
    Wrapper class around the requests package
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
#        no class variables

# |----------------------------------------------------------------------------|
# Constructor
# |----------------------------------------------------------------------------|
    def __init__(self):
        self._resp = None
        self.cert_path = Constants.CERTIFICATE_PATH

# |---------------------------End of Constructor------------------------------|

# |----------------------------------------------------------------------------|
# get_response_json
# |----------------------------------------------------------------------------|
    def get_response_json(self):
        try:
            resp_json = json.loads(self._resp.text)
            return resp_json
        except JSONDecodeError as error:
            raise Exception("Failed to convert response text to JSON due "
                            "to: {}".format(error))

# |----------------------End of get_response_json-----------------------------|

# |----------------------------------------------------------------------------|
# get_response_status_code
# |----------------------------------------------------------------------------|
    def get_response_status_code(self):
        return self._resp.status_code

# |----------------------End of get_response_status_code----------------------|

# |----------------------------------------------------------------------------|
# get_request
# |----------------------------------------------------------------------------|
    def get_request(self, request_name, dest_ip, dest_port, pay_load=None,
                    timeout=None):

        dest_url = ("https://{}:{}/{}".
                    format(dest_ip,
                           dest_port,
                           request_name))

        request_time_out_status = False

        try:
            self._resp = requests.get(url=dest_url,
                                      params=pay_load,
                                      timeout=timeout,
                                      verify=self.cert_path)

        except RequestException as error:
            request_time_out_status = True
            raise Exception("{} request timed out due to: {}".
                            format(request_name, error))

        return request_time_out_status

# |----------------------End of get_request-----------------------------------|

# |----------------------------------------------------------------------------|
# post_request
# |----------------------------------------------------------------------------|
    def post_request(self, request_name, dest_ip, dest_port, pay_load=None,
                     timeout=None):

        dest_url = ("https://{}:{}/{}".
                    format(dest_ip,
                           dest_port,
                           request_name))

        request_time_out_status = False

        try:
            self._resp = requests.post(url=dest_url,
                                       data=json.dumps(pay_load),
                                       timeout=timeout,
                                       verify=self.cert_path)

        except RequestException as error:
            request_time_out_status = True
            raise Exception("{} request timed out due to: {}".
                            format(request_name, error))

        return request_time_out_status

# |----------------------End of post_request----------------------------------|

# |----------------------------------------------------------------------------|
# put_request
# |----------------------------------------------------------------------------|
    def put_request(self, request_name, dest_ip, dest_port, pay_load=None,
                    timeout=None):

        dest_url = ("https://{}:{}/{}".
                    format(dest_ip,
                           dest_port,
                           request_name))

        request_time_out_status = False

        try:
            self._resp = requests.put(url=dest_url,
                                      data=json.dumps(pay_load),
                                      timeout=timeout,
                                      verify=self.cert_path)

        except RequestException as error:
            request_time_out_status = True
            raise Exception("{} request timed out due to: {}".
                            format(request_name, error))

        return request_time_out_status

# |----------------------End of put_request-----------------------------------|

# |----------------------------------------------------------------------------|
# patch_request
# |----------------------------------------------------------------------------|
    def patch_request(self, request_name, dest_ip, dest_port, pay_load=None,
                      timeout=None):

        dest_url = ("https://{}:{}/{}".
                    format(dest_ip,
                           dest_port,
                           request_name))

        request_time_out_status = False

        try:
            self._resp = requests.patch(url=dest_url,
                                        data=json.dumps(pay_load),
                                        timeout=timeout,
                                        verify=self.cert_path)

        except RequestException as error:
            request_time_out_status = True
            raise Exception("{} request timed out due to: {}".
                            format(request_name, error))

        return request_time_out_status

# |----------------------End of put_request-----------------------------------|

# |----------------------------------------------------------------------------|
# delete_request
# |----------------------------------------------------------------------------|
    def delete_request(self, request_name, dest_ip, dest_port, pay_load=None,
                       timeout=None):

        dest_url = ("https://{}:{}/{}".
                    format(dest_ip,
                           dest_port,
                           request_name))

        request_time_out_status = False

        try:
            self._resp = requests.delete(url=dest_url,
                                         data=json.dumps(pay_load),
                                         timeout=timeout,
                                         verify=self.cert_path)

        except RequestException as error:
            request_time_out_status = True
            raise Exception("{} request timed out due to: {}".
                            format(request_name, error))

        return request_time_out_status

# |----------------------End of delete_request--------------------------------|
