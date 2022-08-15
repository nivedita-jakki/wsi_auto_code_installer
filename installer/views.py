import json

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from .installation_handler import AutoInstaller

from installer.service_logger import ServiceLogger
from installer.streamline_json import StreamLineJson
from installer.constants import ErrorCode, RouterInfo
from installer.input_validator import InputValidator
from installer.database_interface import DatabaseInterface


# |----------------------------------------------------------------------------|
# system_details
# |----------------------------------------------------------------------------|
@csrf_exempt
def system_details(request):
    ServiceLogger.get().log_debug(
        "system_details Request method: {}".format(request.method))

    try:
        if request.method == "POST":
            resp_json = {
                "status": False,
                "error_code": "",
                "error_info": "",
                "error_details": {}
            }

            is_valid, data, error_obj = InputValidator().\
                is_request_payload_corrupted(request)

            if not is_valid:
                resp_json["error_code"] = ErrorCode.GENERAL_ERROR.value
                resp_json["error_details"] = error_obj
                resp_json["error_info"] = "Invalid payload"
                resp_str = json.dumps(resp_json)
                return HttpResponse(resp_str, status=400)

            for system_info in data["systems"]:
                if DatabaseInterface().is_system_exists(
                    system_info["system_id"]):
                    # Delete exissting one and add it again
                    DatabaseInterface().delete_record_on_system_id(
                            system_info["system_id"])

                DatabaseInterface().add_systems(system_info)

            resp_str = json.dumps(resp_json)
            return HttpResponse(resp_str, status=200)
            
        elif request.method == "GET":
            status_cdoe = 200
            resp_json = {
                "status": False,
                "error_code": "",
                "error_info": "",
                "error_details": {},
                "systems": []
            }

            docs = DatabaseInterface().get_systems()

            if docs is None:
                status_cdoe = 500
                error_details = StreamLineJson().get_json(
                        "error", ErrorCode.NO_DATA_AVAILABLE.value,
                        actual_err_msg, ""
                    )
                resp_json = {
                        "error_code": ErrorCode.NO_DATA_AVAILABLE.value,
                        "error_info": "No systems available",
                        "error_details": error_details,
                        "systems": []
                    }
            else:
                for doc in docs:
                    resp_json["systems"].append(doc)

            resp_str = json.dumps(resp_json)
            return HttpResponse(resp_str, status=status_cdoe)
        else:
            ServiceLogger.get().log_debug(
                "system_details Response status: 405")
            return HttpResponse(status=405)

    except Exception as error_msg:
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
        return HttpResponse(resp_str, status=500)

# |----------------------End of system_details-----------------------|


# |----------------------------------------------------------------------------|
# update_repos
# |----------------------------------------------------------------------------|
@csrf_exempt
def update_repos(request):
    ServiceLogger.get().log_debug(
        "update_repos Request method: {}".format(request.method))

    try:
        if request.method == "POST":
            resp_json = {
                "status": False,
                "error_code": "",
                "error_info": "",
                "error_details": {}
            }

            is_valid, data, error_obj = InputValidator().\
                is_request_payload_corrupted(request)

            if not is_valid:
                resp_json["error_code"] = ErrorCode.GENERAL_ERROR.value
                resp_json["error_details"] = error_obj
                resp_json["error_info"] = "Invalid payload"
                resp_str = json.dumps(resp_json)
                return HttpResponse(resp_str, status=400)

            InputValidator().is_payload_valid(RouterInfo.UPDATE_REPO.value,
                                              data)
            resp_json["status"] = AutoInstaller().\
                driver_method_for_installation(data)

            resp_str = json.dumps(resp_json)
            return HttpResponse(resp_str, status=200)
        else:
            ServiceLogger.get().log_debug(
                "update_repos Response status: 405")
            return HttpResponse(status=405)

    except Exception as error_msg:
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
        return HttpResponse(resp_str, status=500)

# |----------------------End of update_repos-----------------------|
