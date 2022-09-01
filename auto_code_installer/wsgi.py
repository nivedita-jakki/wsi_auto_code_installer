"""
WSGI config for auto_code_installer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_code_installer.settings')
#sys.path.append("/var/www/wsi_auto_code_installer/auto_code_installer")
#sys.path.append("/var/www/wsi_auto_code_installer")
sys.path.append("/home/adminspin/wsi_auto_code_installer/auto_code_installer")
sys.path.append("/home/adminspin/wsi_auto_code_installer")
os.environ['DJANGO_SETTINGS_MODULE'] = 'auto_code_installer.settings'
os.environ['HTTPS'] = "on"
print("Came!!!!!!!")
application = get_wsgi_application()
