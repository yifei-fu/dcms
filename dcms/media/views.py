from rest_framework import views, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from config.authentication import default_authentication_classes
from content.permissions import IsAuthorOrAdminOtherwiseReadOnly
from .serializers import *


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = default_authentication_classes


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    authentication_classes = default_authentication_classes


# alternative to the POST method in ImageViewSet/FileViewSet

class ImageUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        image = Image.objects.create(path=file_obj)
        return Response(data=ImageSerializer(image).data, status=status.HTTP_201_CREATED)


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        file = File.objects.create(path=file_obj)
        return Response(data=FileSerializer(file).data, status=status.HTTP_201_CREATED)
