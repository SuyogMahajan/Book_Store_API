from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from book.models import Book
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            return ValueError('The email field must be set.')
        
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email, password, **extra_fields)

class AuthUser(AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField(max_length=120)
    mobile_no = models.BigIntegerField()
    email = models.EmailField(max_length=254, unique=True)
    address = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default =True)
    join_date = models.DateField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='profile_photo/',blank=True,null=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_no']
    
    def __str__(self):
        return self.email

class Cart(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='carts')
    books = models.ManyToManyField('book.Book', through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username} created on {self.created_at}"  

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.name} in cart {self.cart.id}"

class Address(models.Model):

    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")
    is_default = models.BooleanField(default=False)  # Field to mark if this is the default address

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.zip_code}, {self.country}"