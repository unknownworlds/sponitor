import os

if "SPONITOR" in os.environ and os.environ["SPONITOR"] == "heroku":
    from settings_heroku import *

DEBUG = False

APP_ROOT = '/app/Sponitor/'

try:
	MONGO_HOST = os.environ["MONGOLAB_URI"]
except:
	print "SETTINGS ERROR: mongodb can't be defined"

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'shouldbearerealkey...'
if "SECRET_KEY" in os.environ:
	SECRET_KEY = os.environ["SECRET_KEY"]


ADMINS = (
    ('Marc Delorme', 'marc@unknownworlds.com'),
)