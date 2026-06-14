from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Book, Borrowing, Wishlist
from datetime import timedelta
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def home(request):
    books = Book.objects.filter(cover_image__isnull=False).order_by('-created_at')
    return render(request, 'home.html', {'books': books})

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        status = self.request.GET.get('status')
        
        qs = Book.objects.filter(cover_image__isnull=False).prefetch_related('category').order_by('-created_at')
        
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        
        if category_id:
            qs = qs.filter(category_id=category_id)
        
        if status == 'available':
            qs = qs.filter(available_copies__gt=0)
        elif status == 'borrowed':
            qs = qs.filter(available_copies=0)
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Category
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_status'] = self.request.GET.get('status', 'all')
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        context['borrowings'] = book.borrowings.select_related('user').order_by('-borrow_date')[:5]
        if book.category:
            context['related_books'] = Book.objects.filter(category=book.category).exclude(pk=book.pk)[:3]
        else:
            context['related_books'] = []
        if self.request.user.is_authenticated:
            context['in_wishlist'] = Wishlist.objects.filter(user=self.request.user, book=book).exists()
        else:
            context['in_wishlist'] = False
        return context

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk, available_copies__gt=0)
    borrowing = Borrowing.objects.create(
        user=request.user,
        book=book,
        due_date = timezone.now().date() + timedelta(days=14)
    )
    book.available_copies -= 1
    book.save()
    messages.success(request, f'You borrowed "{book.title}". Due: {borrowing.due_date.strftime("%Y-%m-%d")}')
    return redirect('book_detail', pk=pk)


@login_required
@require_http_methods(["POST"])
def toggle_wishlist(request, pk):
    book = get_object_or_404(Book, pk=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, book=book)
    if not created:
        wishlist.delete()
        message = "Removed from wishlist!"
        in_wishlist = False
    else:
        message = "Saved to wishlist!"
        in_wishlist = True
    return JsonResponse({'success': True, 'message': message, 'in_wishlist': in_wishlist})


@login_required
@require_http_methods(["POST"])
def reserve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available_copies > 0:
        borrowing = Borrowing.objects.create(
            user=request.user,
            book=book,
            due_date=timezone.now().date() + timedelta(days=14)
        )
        book.available_copies -= 1
        book.save()
        message = "Successfully reserved the book!"
    else:
        message = "Book added to reserve waitlist!"
    return JsonResponse({'success': True, 'message': message})

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('book').order_by('-added_at')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def my_borrowings(request):
    borrowings = Borrowing.objects.filter(user=request.user).select_related('book__category').order_by('-borrow_date')
    return render(request, 'borrowing_history.html', {'borrowings': borrowings})


def contact(request):
    return render(request, 'contact.html', {'page_title': 'Contact Us'})




