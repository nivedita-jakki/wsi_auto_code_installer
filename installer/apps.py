from django.apps import AppConfig

from installer.service_logger import ServiceLogger

class InstallerConfig(AppConfig):
    name = 'installer'

def startup():
    # This will get trigger as soon as we start django
    ServiceLogger.get().initialize("auto_installer")