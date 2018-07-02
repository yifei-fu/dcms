from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from rest_framework import exceptions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.response import Response

from config.authentication import default_authentication_classes
from user.serializers import *
from .permissions import *


def get_auth_token(user):
    auth_token, _ = Token.objects.get_or_create(user=user)
    return auth_token


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSelfOrAdmin,)  # optional: permissions.IsAuthenticated,
    queryset = User.objects.all()
    authentication_classes = default_authentication_classes

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullUserSerializer
        return BasicUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(validated_data=serializer.validated_data)
        auth_token = get_auth_token(user)
        ret_data = {'id': user.id, 'username': user.username}
        ret_data.update(TokenSerializer(auth_token).data)
        return Response(data=ret_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff():
            raise exceptions.PermissionDenied


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    authentication_classes = default_authentication_classes

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        login(request, user)
        auth_token = get_auth_token(user)
        return Response(data=TokenSerializer(auth_token).data, status=status.HTTP_200_OK)


class UserLogoutView(LogoutView):
    authentication_classes = default_authentication_classes

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return super().post(request, *args, **kwargs)
