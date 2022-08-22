from enum import Enum
from os.path import join
from pathlib import Path

class Constants():
    '''
    Constant definitions.
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
    LOCAL_HOST = "localhost"

    UPDATE_SERVICE_PORT = 8041

    # DNS INFO
    SCANNER_DNS = "scanner.pramana.com"

    CLUSTER_DNS = "cluster.pramana.com"
    
    CMS_DNS = "cms.pramana.com"

    CERTIFICATE_PATH =\
        "/home/adminspin/wsi_app/etc/security/authentication.crt"

    VERIFICATION_KEY_PATH =\
        "/home/adminspin/wsi_app/etc/security/authentication.key"

    HOME_PATH = str(Path.home())
    CONFIG_PATH = join(HOME_PATH, "wsi_app", "etc", "calib_data", "config")

    CODE_UPADATE_UTILITY_SCRIPT_PATH = join(HOME_PATH, "office",
                                            "wsi_application_software_installation",
                                            "main_script.py")

# ==============================================================================
# ErrorCode
# ==============================================================================


class ErrorCode(Enum):
    '''
    Enum class for Scanner Error Codes
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|

    GENERAL_ERROR = "E-300"

    NO_DATA_AVAILABLE = "NO_DATA_AVAILABLE"


# ==============================================================================
# RouterInfo
# ==============================================================================


class RouterInfo(Enum):
    '''
    Enum class for Scanner Error Codes
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|

    UPDATE_REPO = "update-repos"
