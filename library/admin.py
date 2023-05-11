from django.contrib import admin
from .models import *


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_books')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'isbn', 'display_genre')


class BookInstanceAdmin(admin.ModelAdmin):
    def change_format(self, obj):
        return obj.due_back.strftime('%Y-%m-%d')

    list_display = ('book', 'book_status', 'due_back', 'reader')
    list_filter = ('book_status',)
    fieldsets = (
        ('General', {'fields': ('instance_id', 'book')}),
        ('Availability', {'fields': ('book_status', 'due_back', 'reader')}),
    )
    search_fields = ('instance_id', 'book__title')


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'date_created', 'reviewer', 'content')


admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
