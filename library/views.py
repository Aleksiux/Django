from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.core.paginator import Paginator
from .models import Book, BookReview, BookInstance, Author
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import EditBookInstanceForm,BookReviewForm, UserUpdateForm, ProfileUpdateForm, CreateBookInstanceForm


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


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    form_class = BookReviewForm

    # Success url
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.book_id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)


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
    paginate_by = 100

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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

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
        User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                 password=password)
        messages.info(request, f'User with username {username} registered!')
        return redirect('login')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


# --------------------------------------------------- CRUD -------------------------------------------------------------
# ------------------------------------------------- LIST VIEW ----------------------------------------------------------


class UserBookDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = 'user_book.html'


@login_required(login_url='login')
def user_book(request, instance_id):
    try:
        user_taken_book = BookInstance.objects.get(instance_id=instance_id)
    except BookInstance.DoesNotExist:
        user_taken_book = None
    context = {
        'user_taken_book': user_taken_book
    }
    return render(request, 'user_book2.html', context)


# ------------------------------------------------- CREATE VIEW --------------------------------------------------------

class UserBookCreateView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    template_name = 'create_user_book.html'
    fields = ['book', 'due_back']
    success_url = '/library/my_books/'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.book_status = 't'
        return super().form_valid(form)


"""
4. Pasiziurekit get_or_create metoda prie to pacio (kai darai per query) sito nereiks cia
:param request:
:return:
"""


@login_required(login_url='login')
def create_new_book_instance(request):
    if request.method == 'POST':
        form = CreateBookInstanceForm(data=request.POST)
        if form.is_valid:
            add_user = form.save(False)
            add_user.reader = request.user
            add_user.book_status = 't'
            add_user.save()
            return redirect('/')
    else:
        form = CreateBookInstanceForm()
    context = {
        'form': form
    }
    return render(request, 'create_user_book2.html', context)


# ------------------------------------------------- UPDATE VIEW --------------------------------------------------------

class UserBookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    template_name = 'update_book_instance.html'
    fields = ['book', 'due_back', 'book_status']
    success_url = '/library/my_books/'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader


def update_book_instance(request, pk):
    book_instance = BookInstance.objects.get(instance_id = pk)
    if request.method == "POST":
        form = EditBookInstanceForm(data=request.POST, instance=book_instance)
        if form.is_valid:
            change_form = form.save(False)
            change_form.reader = book_instance.reader
            change_form.save()
            return redirect(f'/library/my_books2/{pk}')
    else:
        form = EditBookInstanceForm(instance=book_instance)
    context = {
        'form': form,
    }
    return render(request, 'update_book_instance2.html', context)


# ------------------------------------------------- DELETE VIEW --------------------------------------------------------


class UserBookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BookInstance
    success_url = "/library/my_books/"
    template_name = 'user_book_delete.html'

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader


def delete_book_instance(request):
    pass
