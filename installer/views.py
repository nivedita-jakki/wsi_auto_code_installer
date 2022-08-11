import json

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from installer.service_logger import ServiceLogger
from installer.streamline_json import StreamLineJson
from installer.constants import ErrorCode
from installer.input_validator import InputValidator
from installer.database_interface import DatabaseInterface


# |----------------------------------------------------------------------------|
# add_system_details_into_db
# |----------------------------------------------------------------------------|
@csrf_exempt
def add_system_details_into_db(request):
    ServiceLogger.get().log_debug("add_system_details_into_db Request method: " +
                                  request.method)
    if request.method == "POST":
        resp_json = {
            "status": False,
            "error_code": "",
            "error_info": "",
            "error_details": ""
        }
        status_code = 400

        is_valid, data, error_obj = InputValidator().\
            is_request_payload_corrupted(request)

        if not is_valid:
          resp_json["error_code"] = ErrorCode.GENERAL_ERROR.value
          resp_json["error_details"] = error_obj
          resp_json["error_info"] = "Invalid payload"
          resp_str = json.dumps(resp_json)
          return HttpResponse(resp_str, status=status_code)

        try:
            # TODOD: validate json keys
            for system_info in data["systems"]:
                if DatabaseInterface().is_system_exists(
                    system_info["system_id"]):
                    # Delete exissting one and add it again
                    DatabaseInterface().delete_record_on_system_id(
                            system_info["system_id"])
                DatabaseInterface().add_systems(system_info)
            status_code = 200
        except Exception as error_msg:
            status_code = 500
            ServiceLogger.get().log_exception(error_msg)
            actual_err_msg, error_class = StreamLineJson.\
                get_error_info(error_msg)
            error_details = StreamLineJson().get_json(
                    "error", ErrorCode.GENERAL_ERROR.value,
                    actual_err_msg, ""
                )
            resp_json["error_code"] = ErrorCode.GENERAL_ERROR.value
            resp_json["error_details"] = error_details
            resp_json["error_info"] = error_msg.args[0]

        resp_str = json.dumps(resp_json)
        return HttpResponse(resp_str, status=status_code)
    else:
        ServiceLogger.get().log_debug(
            "add_system_details_into_db Response status: 405")
        return HttpResponse(status=405)

# |----------------------End of add_system_details_into_db-----------------|