from rest_framework import serializers
from django.contrib.auth import authenticate

from api.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name",
            "email", "username", "user_type",
            "date_joined")


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError({
                        "is_active": "User is deactivated"
                    })
            else:
                raise serializers.ValidationError({
                    "credentials": "Invalid credentials"
                })
        else:
            raise serializers.ValidationError({
                "fields": "Username and Password are required"
            })
        return data
