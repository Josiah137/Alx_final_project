from rest_framework import serializers
from .models import Book, BookLog

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' 


""" makeing serlization for user registation before me make views for them and make the api exposes """
#importing user model
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Using z create_user method instade of User.objects.create to ensure the password is hashed
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
    
    # setting validation to make emials unique
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists. Try to login instade")
        return value


""" setting serlializer for book loans and returns before creating views """
# handling book loans 
class BorrowBookSerializer(serializers.Serializer):  
    book_id = serializers.IntegerField()  

    def validate(self, data): 
         # holding the requested book using 'id'  
        book_id = data['book_id']  

        try:  
            book = Book.objects.get(pk=book_id)  
        except Book.DoesNotExist:  
            raise serializers.ValidationError("Sorry, Book could not be found.")  

        if book.number_of_copies_available <= 0:  
            raise serializers.ValidationError("Sorry, No copies of the book are available for now.")  

        user = self.context['request'].user  
        if user.booklog_set.filter(book=book, status='BORROWED').exists():  
            raise serializers.ValidationError("You have already borrowed this book.")  

        return data  
    
    def save(self, **kwargs):  
        #actually borrowing z book  
        user = self.context['request'].user  
        book = Book.objects.get(pk=self.validated_data['book_id'])  
        
        # redcuing  z book's available copies
        book.number_of_copies_available -= 1  
        book.save()  

        # Create a transaction record  
        BookLog.objects.create(user=user, book=book, status='BORROWED')

# handling book returns 
from django.utils import timezone # i was suffering beacuse i was trying to import from time module lol... n.b this is django not pure python hehe
class ReturnBookSerializer(serializers.Serializer):  
    book_id = serializers.IntegerField()  

    def validate(self, data):  
        book_id = data['book_id']  

        # Check if the book exists  
        try:  
            book = Book.objects.get(pk=book_id)  
        except Book.DoesNotExist:  
            raise serializers.ValidationError("Sorry, Book could not be found.")  

        # Check if the user has borrowed this book and it is not returned yet  
        user = self.context['request'].user  
        try:  
            book_log = BookLog.objects.get(user=user, book=book, status='BORROWED')  
        except BookLog.DoesNotExist:  
            raise serializers.ValidationError("You have not borrowed this book or have already returned it.")  

        # Save the book_log instance to use in the save method  
        self.book_log = book_log  

        return data  
    
    def save(self, **kwargs):  
        # Update the book log status to RETURNED  
        self.book_log.status = 'RETURNED'  
        self.book_log.return_date = timezone.now()  # Set the return date  
        self.book_log.save()  

        # Increase the book's available copies  
        book = self.book_log.book  
        book.number_of_copies_available += 1  
        book.save()
