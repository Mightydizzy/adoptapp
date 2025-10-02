"""
WSGI config for Adoptapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import Adoptapp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Adoptapp.settings')

application = get_wsgi_application()

gunicorn Adoptapp.wsgi:application --bind 0.0.0.0:$PORT
