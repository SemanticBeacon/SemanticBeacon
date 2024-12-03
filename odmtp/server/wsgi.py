"""
WSGI config for odmtrip_tpf_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Set the current directory as the base path for settings.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Use the settings located in the same directory as this script.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()