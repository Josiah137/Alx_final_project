from django.shortcuts import render

# Create your views here.

"""                            importing modules                           """

# importing  my book model and its serializer
from .models import Book
from .serializers import BookSerializer, BorrowBookSerializer, ReturnBookSerializer

# importing generics for my generic views #importing filters to enable searchig and filtering
from rest_framework import generics, filters, status

# for my apiviews
from rest_framework.views import APIView 
from rest_framework.response import Response

#importing modules to handle the auth and autorization 
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


""" handling the views, the CRUD """

# TO LIst all books or create a new book 
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'ISBN']  # to allow searching by these fields

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        # Filter available books if the 'available' query parameter is passed
        available = self.request.query_params.get('available')
        if available == 'true':
            queryset = queryset.filter(number_of_copies_available__gt=2)
        return queryset

# Retrieve, update, or delete a single book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
""" create a view for the user registration"""
#importing the custom users from our modle and also using CreateAPIView for simplification 
from .models import User
from .serializers import UserRegistrationSerializer
from rest_framework.generics import CreateAPIView

class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # since we dont want people to be autheticated to signup lol

     # Optional: You can customize the response or add permission classes if needed  
    def create(self, request, *args, **kwargs):  
        response = super().create(request, *args, **kwargs)  
        response.data = {'message': "Readers are leaders! Wellcome, You have registered successfully." }  
        return response
    
    
"""creating a view for my BookLog"""
class BorrowBookView(APIView):  
    permission_classes = [IsAuthenticated]  

    def post(self, request):  
        serializer = BorrowBookSerializer(data=request.data, context={'request': request})  
        if serializer.is_valid():  
            serializer.save()  
            return Response({'message': 'Book borrowed successfully! Take a good care for it.'}, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
# View to handle returning books
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReturnBookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Return the book
            return Response({"message": "Book returned successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)