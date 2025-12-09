from rest_framework import serializers
from .models import CustomUser
from django.db.models import Q


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username", "email", "password",
            "full_name", "age", "phone", "city", "state", "pincode",
        ]

    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(raw_password)  # hash password
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # username OR email
    password = serializers.CharField()

    def validate(self, data):
        identifier = data['identifier']
        password = data['password']

        try:
            user = CustomUser.objects.get(
                Q(username=identifier) | Q(email=identifier)
            )
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username/email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username/email or password")

        data['user'] = user
        return data
    
# class AllotmentUploadSerializer(serializers.Serializer):
#     allotment_pdf = serializers.FileField()

#     def update(self, instance, validated_data):
#         instance.allotment_pdf = validated_data["allotment_pdf"]
#         instance.save()
#         return instance