from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(selfself, data):
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError("username is already taken")
        if User.objects.filter(username=data.get('email')):
            raise serializers.ValidationError("email is already taken")
        return data

    def create(self, validated_data):
        self.validate(validated_data)
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class BasicUserSerializer(serializers.ModelSerializer):
    '''
    User information serializer for public access. Read-only.
    '''
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined', 'last_login')
        read_only_fields = ('id', 'username', 'date_joined', 'last_login')


class FullUserSerializer(serializers.ModelSerializer):
    '''
    User full information serializer for self and admins.
    '''
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'last_login')
        read_only_fields = ('id', 'username', 'date_joined', 'last_login')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("user authentication failed")
        if not user.is_active:
            raise serializers.ValidationError("user account disabled")
        data['user'] = user
        return data


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ('auth_token',)
