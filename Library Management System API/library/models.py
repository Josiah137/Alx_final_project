from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13, unique=True)
    Published_Date = models.DateField()
    number_of_copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"


#my custom user model
#A user should have a unique Username, Email, Date of Membership, and Active Status.

from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=100, blank=False, null=False)
    date_of_membership = models.DateField(auto_now_add=True)
    is_active_member = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]


    def __str__(self):
        return self.username
    

class BookTracker(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    check_out_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book')    
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    