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
