from django.shortcuts import render

# Create your views here.

from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer

#handling the CRUD

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
    
   
