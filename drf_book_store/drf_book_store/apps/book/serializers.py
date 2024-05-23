from rest_framework import serializers

from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        feilds = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        feilds = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        feilds = "__all__"
