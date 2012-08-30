# Local settings for labgeeksrpg project.
# You should copy this file to your own local_settings.py and customize it.

# The full path to your labgeeksrpg installation.
APP_DIR = "/full/path/to/your/labgeeksrpg"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*8-x1k(+(7)da_vw3a3p*&k_i+8_gbiadevvp@5_zhytxl6@x@'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'labgeeks.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

""" All of these sections need to be reset after changing the APP_DIR from the main settings.py.
You shouldn't need to alter them at all yourself.
"""
MEDIA_ROOT = '%s/uploads/' % APP_DIR

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/static/" % APP_DIR,
    "%s/uploads/" % APP_DIR,
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/templates" % APP_DIR,
)
