from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13, unique=True, null=False, blank=False)
    Published_Date = models.DateField()
    number_of_copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

'''
my custom user model- for user creation.
        #A user should have a unique Username, Email, Date of Membership, and Active Status.
'''

from django.contrib.auth.models import AbstractUser
# email, username and pass is alrady provided by the base user.
# but i extended it to ad memebership and active status

class User(AbstractUser):
    date_of_membership = models.DateField(auto_now_add=True)
    is_active_member = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class BookLog (models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    check_out_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    # class Meta:
    #     unique_together = ('user', 'book')    # if this is turned on, indeed a user cannot loan morethan one book but it can't also borrow the same book again if he has borrowed once
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    