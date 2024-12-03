from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Для подтверждения пароля

    class Meta:
        model = User  # Или CustomUser
        fields = ['name', 'password', 'password2', 'email', 'username']

    def validate(self, attrs):
        attrs['username'] = attrs['username'].lower()  # Normalize username to lowercase
        attrs['email'] = attrs['email'].lower()  # Normalize email to lowercase

        # Check if the username exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Этот имя пользователя уже занято."})

        # Check if the email exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Этот адрес электронной почты уже используется."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Убираем подтверждение пароля
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            username=validated_data['username'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')