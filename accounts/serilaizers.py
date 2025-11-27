from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class  RegistrationSerilaizer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model= User
        fields = ["email","password","password1"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({'detail': 'password does not match'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        

        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password1",None)
        return User.objects.create_user(**validated_data) # type: ignore