# Image Display Fix - TODO List

## Planned Steps:
- [ ] Step 1: Update book/book/settings.py - Add MEDIA_URL, MEDIA_ROOT, STATICFILES_DIRS
- [ ] Step 2: Update book/book/urls.py - Add media static serving for development
- [ ] Step 3: Create media/books/ directory and copy sample images from book/books/
- [ ] Step 4: Update book/library/admin.py to register Book model for image uploads
- [ ] Step 5: Run migrations and createsuperuser if needed
- [ ] Step 6: Use Django shell/admin to assign sample cover images to existing books
- [ ] Step 7: Test runserver - verify images display in home/book_list/book_detail

**Progress:** Ready to execute Step 1.

