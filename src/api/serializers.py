from rest_framework import serializers
from django.contrib.auth import authenticate

from api.models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'title', 'image', 'bio','phone',
            'location', 'address_1', 'address_2')
        read_only_fields = ('username',)



class UserSerializer(serializers.ModelSerializer):
    """Serializers new user request."""
    # password should 8-128 chars and unreadable. Even if 
    # listed(serializer requirement) under `fields` below 
    # it won't be returned
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    profile = ProfileSerializer(required=False)


    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email",
        "username", "password", "user_type", "profile", "date_joined")
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Performs an update on a User/Profile."""
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()

        return instance

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
                        "is_inactive": "User is inactive. Please activate!"
                    })
            else:
                raise serializers.ValidationError({
                    "credentials": "Wrong email or password"
                })
        else:
            raise serializers.ValidationError({
                "fields": "Username and Password are required"
            })
        return data
