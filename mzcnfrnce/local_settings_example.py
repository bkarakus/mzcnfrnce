import os
# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = True

ALLOWED_HOSTS = [""]

# Make these unique, and don't share it with anybody.
SECRET_KEY = "g7f*^v47$mz4eymoeu%$%z!es*m==jy%t(rt!u(i^l%o^ihcr9"
NEVERCACHE_KEY = "h*&5r1t$z93n41@c#d=kk7@ta!4vprq9z+2h9s-u7lk(=_xap&"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

SITE_MEDIA_ROOT = os.path.join('/home/user_name/public_html/site_dir', 'site_media')

MEDIA_ROOT = os.path.join(SITE_MEDIA_ROOT, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_MEDIA_ROOT, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

EMAIL_HOST = 'mail.*******.*****'
EMAIL_HOST_USER = '*****@***************'
EMAIL_HOST_PASSWORD = '**************'
DEFAULT_FROM_EMAIL = '****@**************'
SERVER_EMAIL = '*****@*****************'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_BACKEND = 'dbemail.backends.EmailBackend'


###################
# DEPLOY SETTINGS #
###################

# Domains for public site
# ALLOWED_HOSTS = [""]

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "DEPLOY_TOOL": "rsync",  # Deploy with "git", "hg", or "rsync"
#     "SSH_USER": "",  # VPS SSH username
#     "HOSTS": [""],  # The IP address of your VPS
#     "DOMAINS": ALLOWED_HOSTS,  # Edit domains in ALLOWED_HOSTS
#     "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
#     "LOCALE": "en_US.UTF-8",  # Should end with ".UTF-8"
#     "DB_PASS": "",  # Live database password
#     "ADMIN_PASS": "",  # Live admin user password
#     "SECRET_KEY": SECRET_KEY,
#     "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }
