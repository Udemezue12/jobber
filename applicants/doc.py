# import os
# from django.conf import settings
# from django.core.files.storage import default_storage
# from django.utils.text import slugify
# from django.core.files.base import ContentFile

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# IMAGE = os.path.join(BASE_DIR, 'static', 'images')
# DOCUMENT= os.path.join(BASE_DIR, 'static', 'documents')

# if not os.path.exists(IMAGE):
#     os.makedirs(IMAGE)

# if not os.path.exists(DOCUMENT):
#     os.makedirs(DOCUMENT)


# def save_file(file, upload_to='uploads'):
#     upload_folder = os.path.join(settings.MEDIA_ROOT, upload_to)


#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)


#     filename = slugify(file.name)
#     file_path = os.path.join(upload_folder, filename)

#     # Save the file using default_storage
#     path = default_storage.save(file_path, ContentFile(file.read()))

#     return path
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

import os
from django.conf import settings


def document(instance, filename):
    return os.path.join('documents', filename)


def image(instance, filename):
    return os.path.join('images', filename)
