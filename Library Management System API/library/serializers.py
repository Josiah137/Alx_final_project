from rest_framework import serializers
from .models import Book

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
