from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema
from .models import Author, Book, Language, Review
from .serializers import AuthorSerializer, BookSerializer, LanguageSerializer, ReviewSerializer
from auth_app.models import AuthUser

class AuthorViewSet(viewsets.ViewSet):
    """
    a simple viewset for viewing authors
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @extend_schema(responses=AuthorSerializer)
    def list(self, request):
        serializer = AuthorSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(request=AuthorSerializer, responses=AuthorSerializer)
    def create(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class BookViewSet(viewsets.ViewSet):
    """
    a simple viewset for viewing Books
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(responses=BookSerializer)
    def list(self, request):
        serializer = BookSerializer(self.queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)

    @extend_schema(request=BookSerializer, responses=BookSerializer)
    def create(self, request):
        print(type(request.data),request.data)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LanguageViewSet(viewsets.ViewSet):
    """
    a simple viewset for viewing Languages
    """

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    @extend_schema(responses=LanguageSerializer)
    def list(self, request):
        serializer = LanguageSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(request=LanguageSerializer, responses=LanguageSerializer)
    def create(self, request):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ViewSet):
    """
    a simple viewset for viewing Reviews
    """
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    @extend_schema(responses=ReviewSerializer)
    def list(self, request):
        serializer = ReviewSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(request=ReviewSerializer, responses=ReviewSerializer)
    def create(self, request):
        serializer = ReviewSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=ReviewSerializer)
    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error':'Review Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    @extend_schema(request=ReviewSerializer,responses=ReviewSerializer)
    def update(self, request, pk):

        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error':'Review Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review, data=request.data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):

        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error':'Review Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    @action(detail=False, methods=['GET'],url_path='by-book/(?P<book_id>[^/.]+)')
    @extend_schema(responses=ReviewSerializer(many=True))
    def get_by_book(self, request, book_id=None):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'error':'Review Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['GET'],url_path='by-user/(?P<user_id>[^/.]+)')
    @extend_schema(responses=ReviewSerializer(many=True))
    def get_by_user(self, request, user_id=None):
        try:
            user = AuthUser.objects.get(pk=user_id)
        except AuthUser.DoesNotExist:
            return Response({'error':'Review Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = Review.objects.filter(user=user)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)    
