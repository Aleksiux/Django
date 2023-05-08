from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q


# Create your views here.
def index(request):
    book_count = Book.objects.all().count()
    book_instance_count = BookInstance.objects.all().count()
    available_books_count = BookInstance.objects.filter(book_status__exact='a').count()
    author_count = Author.objects.all().count()
    number_of_visits = request.session.get('number_of_visits', 1)
    request.session['number_of_visits'] = number_of_visits + 1
    context = {
        'books': book_count,
        'book_instances': book_instance_count,
        'authors': author_count,
        'available': available_books_count,
        'number_of_visits':number_of_visits
    }
    return render(request, "index.html", context)


# def authors(request):
#     authors = Author.objects.all()
#     context = {
#         'authors': authors
#     }
#     return render(request, 'authors.html', context=context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors
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
    paginate_by = 2
    # context_object_name = 'my_book_list'
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='The')
    template_name = 'book_list.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


def search(request):
    """
    Simple search. query takes information from search form,
    search_results filters by input text, book title and descriptions.
    Icontains from contains different that icontains is not key sensitive.
    """
    query = request.GET.get('query')
    search_results = Book.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(author__last_name__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})
