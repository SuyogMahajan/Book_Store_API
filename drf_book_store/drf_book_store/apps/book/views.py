from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Author, Book, Language
from .serializers import AuthorSerializer, BookSerializer, LanguageSerializer


class AuthorViewSet(viewsets.ViewSet):
    """
    a simple viewset for viewing authors
    """

    queryset = Author.objects.all()

    @extend_schema(responses=AuthorSerializer)
    def list(self, request):
        serializer = AuthorSerializer(self.queryset, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ViewSet):
    """
    a simple viewset for viewing authors
    """

    queryset = Book.objects.all()

    def list(self, request):
        serializer = BookSerializer(self.queryset, many=True)
        return Response(serializer.data)


class LangugaeViewSet(viewsets.ViewSet):
    """
    a simple viewset for viewing authors
    """

    queryset = Language.objects.all()

    def list(self, request):
        serializer = LanguageSerializer(self.queryset, many=True)
        return Response(serializer.data)
