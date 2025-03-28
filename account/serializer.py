from rest_framework import serializers
from account.models import Visitor
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class VisitorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Visitor
        fields = "__all__"