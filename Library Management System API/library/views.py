from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

#handling the CRUD

# TO LIst all books or create a new book 
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Retrieve, update, or delete a single book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
