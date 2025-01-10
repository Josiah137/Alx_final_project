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


#my custom user model
#A user should have a unique Username, Email, Date of Membership, and Active Status.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  

# email, username and pass is alrady provided by the base user. #  but to make the emial mandatory and unique
# but i extended it to ad memebership and active status



# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  
# from django.db import models  

# class UserManager(BaseUserManager):  
#     def create_user(self, username, email, password=None, **extra_fields):  
#         if not username:  
#             raise ValueError('The Username field must be set')  
#         if not email:  
#             raise ValueError('The Email field must be set')  
        
#         email = self.normalize_email(email)  # Normalize the email address  
#         user = self.model(username=username, email=email, **extra_fields)  
#         user.set_password(password)  # Hash the password  
#         user.save(using=self._db)  
#         return user  
#     def create_superuser(self, username, email, password=None, **extra_fields):  
#         extra_fields.setdefault('is_staff', True)  
#         extra_fields.setdefault('is_superuser', True)  # Ensure superuser status  
#         return self.create_user(username, email, password, **extra_fields)  

    # def get_by_natural_key(self, username):  
    #     return self.get(username=username)  # This is important for authentication 
     

class User(AbstractBaseUser):  
    username = models.CharField(max_length=50, unique=True)  
    email = models.EmailField(max_length=100)  
    date_of_membership = models.DateField(auto_now_add=True)  
    is_active_member = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # New field to indicate staff status  
    is_superuser = models.BooleanField(default=False)  # New field to indicate superuser status    

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = []  

    objects = UserManager()  # Set the custom user manager  

    def __str__(self):  
        return self.username








# class UserManager(BaseUserManager):  
#     def create_user(self, username, email, password=None, **extra_fields):  
#         if not username:  
#             raise ValueError('The Username field must be set')  
#         if not email:  
#             raise ValueError('The Email field must be set')  
        
#         email = self.normalize_email(email)  # Normalizingg z email address
#         user = self.model(username=username, email=email, **extra_fields)  
#         user.set_password(password)  # Hashing the password(to aviod plain texts)  
#         user.save(using=self._db)  
#         return user  

#     def create_superuser(self, username, email, password=None, **extra_fields):  
#         extra_fields.setdefault('is_staff', True)  
#         extra_fields.setdefault('is_superuser', True)  
#         user = self.create_user(username, email, password, **extra_fields)
#         # user.is_staff = True
#         # user.is_superuser = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True, max_length=100, blank=False, null=False)
#     date_of_membership = models.DateField(auto_now_add=True) #  set to the current date and time when a new User instance is created.
#     is_active_member = models.BooleanField(default=True)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ["email"]

#     objects = UserManager() 

#     def __str__(self):
#         return self.username
    





class BookLog (models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    check_out_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    # class Meta:
    #     unique_together = ('user', 'book')    # if this is turned on, indeed a user can not load morethan one book but it can't also borrow the same book again if he has borrowed once
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    