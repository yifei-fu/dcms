from django.db import models

# Create your models here.
from config.settings import IMAGE_UPLOAD_PATH, FILE_UPLOAD_PATH
from content.models import ContentMetadata


def get_image_upload_path(instance, filename):
    return IMAGE_UPLOAD_PATH + '{}/{}'.format(
        instance.author.username if instance.author else 'guest', filename)


def get_file_upload_path(instance, filename):
    return FILE_UPLOAD_PATH + '{}/{}'.format(
        instance.author.username if instance.author else 'guest', filename)

class Image(ContentMetadata):
    path = models.ImageField(upload_to=get_image_upload_path)

class File(ContentMetadata):
    path = models.FileField(upload_to=get_file_upload_path)
