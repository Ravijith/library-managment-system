# Task: Display All Book Images as Matching Cards - FIXED

Status: Plan approved by user.

**Changes Made:**
- Updated library/views.py:
  - home(): Now shows ALL books with cover_image, ordered by created_at (removed availability filter & [:8])
  - BookListView.get_queryset(): Shows ALL books with cover_image (removed availability & [:100]), keeps search/pagination.
- Templates: Updated to show availability status for all books, disable borrow if 0 copies.

**Expected Result:**
- / (home): All book cards with images (no limit).
- /books/: All book cards, paginated, search works.

**Test:** `python manage.py runserver` then visit localhost:8000/books/

✅ Complete
