from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<int:pk>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('books/<int:pk>/reserve/', views.reserve_book, name='reserve_book'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('my-borrowings/', views.my_borrowings, name='borrowing_history'),
    path('contact/', views.contact, name='contact'),
]


