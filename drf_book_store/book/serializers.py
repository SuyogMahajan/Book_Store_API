from rest_framework import serializers

from .models import Author, Book, Language, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all())
    
    class Meta:
        model = Book
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Review
        fields = "__all__"