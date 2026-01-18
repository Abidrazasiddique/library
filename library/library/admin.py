from django.contrib import admin
from .models import Author, Book, BorrowRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    ordering = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'published_date', 'author')
    list_display_links = ('id', 'title')
    list_filter = ('genre', 'author')
    search_fields = ('title', 'author__name')
    ordering = ('title',)


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'book', 'borrow_date', 'return_date', 'is_returned')
    list_display_links = ('id', 'user_name')
    list_filter = ('borrow_date', 'return_date')
    search_fields = ('user_name', 'book__title')
    ordering = ('-borrow_date',)

    def is_returned(self, obj):
        return obj.is_returned
    is_returned.boolean = True
    is_returned.short_description = 'Returned'
