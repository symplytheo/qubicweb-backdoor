from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration and profile management.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # select what to expose in JWT payload
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "is_verified",
            "password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at", "updated_at"]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to include additional user info in JWT token response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        print('self.user:', self.user)  # Debugging line to check self.user

        data["user"] = UserSerializer(self.user).data

        data["message"] = "Login successful."

        return data
