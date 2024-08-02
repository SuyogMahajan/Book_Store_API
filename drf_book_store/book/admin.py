from django.contrib import admin
from .models import Author, Book, Language, Review

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Language)
admin.site.register(Review)
