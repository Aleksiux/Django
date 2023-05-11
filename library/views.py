from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages


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
        'number_of_visits': number_of_visits
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


# ------------------------------------------- USER BOOK VIEWS ----------------------------------------------------------
class UserBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_books.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user, book_status__exact='t').order_by('due_back')


@login_required(login_url='login')
def user_books(request):
    user = request.user
    try:
        user_books = BookInstance.objects.filter(reader=request.user).filter(book_status__exact='t').order_by(
            'due_back')
    except BookInstance.DoesNotExist:
        user_books = None
    context = {
        'user': user,
        'user_books': user_books,
    }
    return render(request, 'user_books2.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # taking all values from registration form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # checking if passwords matches
        #     if password == password2:
        #         # checking if username is not taken
        #         if User.objects.filter(username=username).exists():
        #             messages.error(request, f'Username {username} is taken! Choose another one')
        #             return redirect('register')
        #         else:
        #             # checking if email is not taken
        #             if User.objects.filter(email=email).exists():
        #                 messages.error(request, f'User with {email} is already registered!')
        #                 return redirect('register')
        #             else:
        #                 # if everything is good, create new user.
        #                 User.objects.create_user(username=username, email=email, password=password)
        #                 messages.info(request, f'User with username {username} registered!')
        #                 return redirect('login')
        #     else:
        #         messages.error(request, 'Password does not match!')
        #         return redirect('register')
        # return render(request, 'register.html')

        # checking if passwords matches
        if password != password2:
            messages.error(request, 'Password does not match!')
            return redirect('register')

        # checking if username is not taken
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username {username} is taken! Choose another one')
            return redirect('register')

        # checking if email is not taken
        if User.objects.filter(email=email).exists():
            messages.error(request, f'User with {email} is already registered!')
            return redirect('register')

        # if everything is good, create new user.
        User.objects.create_user(username=username, email=email, password=password)
        messages.info(request, f'User with username {username} registered!')
        return redirect('login')
