from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import *


# Create your views here.
def index(request):
    book_count = Book.objects.all().count()
    book_instance_count = BookInstance.objects.all().count()
    available_books_count = BookInstance.objects.filter(book_status__exact='a').count()

    author_count = Author.objects.all().count()
    context = {
        'books': book_count,
        'book_instances': book_instance_count,
        'authors': author_count,
        'available': available_books_count
    }
    return render(request, "index.html", context)


def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context=context)


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {
        'author': author
    }
    return render(request, 'author.html', context)


class BookListView(generic.ListView):
    model = Book
    # context_object_name = 'my_book_list'
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='The')
    template_name = 'book_list.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
