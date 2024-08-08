from django.db import models
from auth_app.models import AuthUser


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    disciption = models.TextField(null=True)
    photo = models.ImageField(upload_to ='uploads/',null=True)
    dob = models.DateField(null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null= True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null= True)
    publication_date = models.DateField
    price = models.IntegerField
    image = models.URLField
    edition = models.IntegerField

    status = models.CharField(max_length=30)
    stock = models.BooleanField
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(AuthUser,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1,default=5.0) 
    review = models.TextField(null=True)
    date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user} - {self.book}"
