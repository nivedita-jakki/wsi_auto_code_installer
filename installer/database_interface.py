import pymongo

from installer.service_logger import ServiceLogger

# ==============================================================================
# DatabaseInterface
# ==============================================================================


class DatabaseInterface():
    '''
    This class connects to the Mongo database provides methods to access
    the installed_services database & its tables.
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
#        no class variables

# |----------------------------------------------------------------------------|
# Constructor
# |----------------------------------------------------------------------------|
    def __init__(self):
        self._mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self._mongo_db = self._mongo_client["installed_services"]

# |---------------------------End of Constructor-----------------------------|

# |--------------------------------------------------------------------------|
# add_systems
# |--------------------------------------------------------------------------|
    def add_systems(self, system_info):
        try:
            collection = self._mongo_db["systems"]
            collection.insert_one(system_info)
        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            raise err_msg

# |----------------------End of add_systems---------------------------------|

# |--------------------------------------------------------------------------|
# is_system_exists
# |--------------------------------------------------------------------------|
    def is_system_exists(self, system_id):
        try:
            collection = self._mongo_db["systems"]

            filter_query = {
                "system_id": system_id
            }
            doc = collection.find_one(filter_query)

            if doc:
                return True
            else:
                return False
        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            raise err_msg

# |----------------------End of is_system_exists---------------------------|

# |--------------------------------------------------------------------------|
# delete_record_on_system_id
# |--------------------------------------------------------------------------|
    def delete_record_on_system_id(self, system_id):
        try:
            collection = self._mongo_db["systems"]

            delete_query = {
                "system_id": system_id
            }
            collection.delete_many(delete_query)

        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            raise err_msg

# |--------------End of delete_record_on_system_id-------------------------|

# |--------------------------------------------------------------------------|
# get_system_info_on_system_id
# |--------------------------------------------------------------------------|
    def get_system_info_on_system_id(self, system_id):
        try:
            collection = self._mongo_db["systems"]

            filter_query = {
                "system_id": system_id
            }
            doc = collection.find_one(filter_query)

            if doc:
                return doc
            else:
                return None
        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            raise err_msg

# |---------------End of get_system_info_on_system_id-----------------------|

# |--------------------------------------------------------------------------|
# get_systems
# |--------------------------------------------------------------------------|
    def get_systems(self):
        try:
            collection = self._mongo_db["systems"]
            select_query = {
                "_id": 0
            }
            print("select_query: ", select_query)
            docs = collection.find({}, select_query)

            if docs:
                return docs
            else:
                return None
        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            return None

# |--------------------------End of get_systems-----------------------------|

# |--------------------------------------------------------------------------|
# add_repo_info
# |--------------------------------------------------------------------------|
    def add_repo_info(self, repo_obj):
        try:
            collection = self._mongo_db["repo_info"]
            collection.insert_one(repo_obj)
        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            raise err_msg

# |----------------------End of add_repo_info------------------------------|

# |--------------------------------------------------------------------------|
# is_repo_id_exists
# |--------------------------------------------------------------------------|
    def is_repo_id_exists(self, id):
        try:
            collection = self._mongo_db["repo_info"]

            filter_query = {
                "id": id
            }
            doc = collection.find_one(filter_query)

            if doc:
                return True
            else:
                return False
        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            raise err_msg

# |----------------------End of is_repo_id_exists--------------------------|

# |--------------------------------------------------------------------------|
# delete_record_on_repo_id
# |--------------------------------------------------------------------------|
    def delete_record_on_repo_id(self, id):
        try:
            collection = self._mongo_db["repo_info"]

            delete_query = {
                "id": id
            }
            collection.delete_many(delete_query)

        except Exception as err_msg:
            ServiceLogger.get().log_exception(err_msg)
            raise err_msg

# |--------------End of delete_record_on_repo_id-------------------------|
