"""
Serialisers of main app.
"""
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Custom User serialiser.
    """
    class Meta:
        """
        Specifies the model and the fields to be included 
        in the serialized output.
        """
        model = CustomUser
        fields = ('id', 'first_name', 'last_name')
