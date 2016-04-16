from .base import *

# I know that eval is scary but I guess it's ok here since only someone with
# root access can change it anyway.
ADMINS = eval(os.environ["ADMINS"])

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "bestellen.fahrwerk-berlin.de", "fahrwerk.regulus.uberspace.de"]
USE_X_FORWARDED_HOST = True

# See https://wiki.uberspace.de/mail for configuration options
EMAIL_HOST = os.environ["DJANGO_EMAIL_HOST"]
EMAIL_PORT = os.environ["DJANGO_EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["DJANGO_EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["DJANGO_EMAIL_HOST_PASSWORD"]

DEFAULT_FROM_EMAIL = os.environ["DJANGO_DEFAULT_FROM_EMAIL"]
SERVER_EMAIL = DEFAULT_FROM_EMAIL
