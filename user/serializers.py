from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label="Password", write_only=True, style={"input_type": "password"}
    )
    password_repeat = serializers.CharField(
        label="Password repeat", write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_repeat",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = validated_data.pop("password", None)

        if password:
            user.set_password(password)
            user.save()

        return user
