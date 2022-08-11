import json

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from installer.service_logger import ServiceLogger
from installer.streamline_json import StreamLineJson
from installer.constants import ErrorCode


# |----------------------------------------------------------------------------|
# add_system_details_into_db
# |----------------------------------------------------------------------------|
@csrf_exempt
def add_system_details_into_db(request):
    ServiceLogger.get().log_debug("add_system_details_into_db Request method: " +
                                  request.method)
    if request.method == "POST":
        status_code = 400

        try:
            data_str = request.body.decode('utf-8')
            data_json = json.loads(data_str)
            return HttpResponse(status=200)

        except Exception as error_msg:
            ServiceLogger.get().log_exception(error_msg)

            actual_err_msg, error_class = StreamLineJson.\
                get_error_info(error_msg)
            error_details = StreamLineJson().get_json(
                    "error", ErrorCode.GENERAL_ERROR.value,
                    actual_err_msg, ""
                )

            # Post scanner error to node to halt the scanner.
            scanner_error_json = {
                    "error_info": error_msg.args[0],
                    "error_code": ErrorCode.GENERAL_ERROR.value,
                    "error_details": error_details
                }

            StreamLineJson.get_error_info(error_msg)
            ServiceLogger.get().log_debug("bad request: {}".
                                          format(error_msg))

        return HttpResponse(status=status_code)
    else:
        ServiceLogger.get().log_debug(
            "add_system_details_into_db Response status: 405")
        return HttpResponse(status=405)

# |----------------------End of add_system_details_into_db-----------------|