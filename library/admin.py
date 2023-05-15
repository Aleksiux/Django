from django.contrib import admin
from .models import Profile, Author, Book, BookInstance, Genre


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


admin.site.register(Profile)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
