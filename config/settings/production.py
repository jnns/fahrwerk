# This file is deprecated and is superseded by production-settings for each
# domain that this site is run as.
# For example, the site running as bestellen.fahrwerk-berlin.de should be
# deployed with config.settings.fahrwerk

from .base import *

# eval() poses a security risk but it may be negligible because 
# there's no user input validated. Should use the ast library in the 
# future though.
ADMINS = eval(os.environ["ADMINS"])

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "bestellen.fahrwerk-berlin.de"]
USE_X_FORWARDED_HOST = True

# See https://wiki.uberspace.de/mail for configuration options
EMAIL_HOST = os.environ["DJANGO_EMAIL_HOST"]
EMAIL_PORT = os.environ["DJANGO_EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["DJANGO_EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["DJANGO_EMAIL_HOST_PASSWORD"]

DEFAULT_FROM_EMAIL = os.environ["DJANGO_DEFAULT_FROM_EMAIL"]
SERVER_EMAIL = DEFAULT_FROM_EMAIL
