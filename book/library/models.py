from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to='books/', blank=True, null=True)
    published_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-borrow_date']
        verbose_name_plural = 'Borrowings'

    def __str__(self):
        status = "Returned" if self.is_returned else "Borrowed"
        return f"{self.user.username} - {self.book.title} ({status})"

    def save(self, *args, **kwargs):
        if not self.return_date and self.is_returned:
            self.return_date = timezone.now().date()
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlisters')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

