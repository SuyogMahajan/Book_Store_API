from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)
    disciption = models.TextField()
    photo = models.URLField()
    dob = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author_id = models.ForeignKey(Author, on_delete=models.SET)
    publication_date = models.DateField
    price = models.IntegerField
    image = models.URLField
    edition = models.IntegerField

    status = models.CharField(max_length=30)
    stock = models.BooleanField
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title


# class Reviews(models.Model):
#     # customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     review = models.TextField()
#     date = models.DateField()

#     def __str__(self):
#         return sel


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
