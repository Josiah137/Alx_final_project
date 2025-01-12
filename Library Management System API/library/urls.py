#importing the path module and my views
from django.urls import path
from .views import BookListCreateView, BookDetailView, UserRegistrationView, BorrowBookView, ReturnBookView
urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('books/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('books/return/', ReturnBookView.as_view(), name='return-book'),
]