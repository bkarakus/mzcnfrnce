import os

from django.template.defaultfilters import slugify

from filebrowser_safe.functions import get_directory

def slugify_filename(filename):
    filename, ext = os.path.splitext(filename)
    filename = slugify(filename)
    filename = filename + ext.lower()
    return filename

def get_abstracts_path(instance, filename):
    filename = slugify_filename(filename)
    upload_to = os.path.join(get_directory(), "abstracts", filename)
    return upload_to

def get_aippapers_path(instance, filename):
    filename = slugify_filename(filename)
    upload_to = os.path.join(get_directory(), "aippapers", filename)
    return upload_to
