from django.contrib import admin
from .models import Book, Borrowing, Category, Wishlist

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available_copies', 'total_copies', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['available_copies']

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'due_date', 'is_returned']
    list_filter = ['is_returned', 'borrow_date']
    raw_id_fields = ['user', 'book']
    readonly_fields = ['borrow_date']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):


    pass


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'added_at']
    list_filter = ['added_at']
    raw_id_fields = ['user', 'book']
