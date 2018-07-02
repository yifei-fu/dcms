from django.db import models

# Create your models here.
from config.settings import IMAGE_UPLOAD_PATH, FILE_UPLOAD_PATH
from content.models import ContentMetadata


class Image(ContentMetadata):
    image = models.ImageField(upload_to=IMAGE_UPLOAD_PATH)


class File(ContentMetadata):
    file = models.FileField(upload_to=FILE_UPLOAD_PATH)
