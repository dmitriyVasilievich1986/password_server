from rest_framework.serializers import ModelSerializer
from .models import Passwords


class PasswordsSerializer(ModelSerializer):
    class Meta:
        model = Passwords
        fields = "__all__"
