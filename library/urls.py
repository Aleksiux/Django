"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='author'),
    path('authors/<int:author_id>', views.author, name='author'),
    path('', RedirectView.as_view(url='library/', permanent=False)),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('search/', views.search, name='search'),
    path('account/', include('django.contrib.auth.urls')),
    # Class based views for BookInstances
    path('my_books/', views.UserBooksListView.as_view(), name='my-books'),
    path('my_books/<uuid:pk>', views.UserBookDetailView.as_view(), name='my-book'),
    path('my_books/create/', views.UserBookCreateView.as_view(), name='create'),
    path('my_books/<uuid:pk>/update', views.UserBookUpdateView.as_view(), name='update'),
    path('my_books/<uuid:pk>/delete', views.UserBookDeleteView.as_view(), name='delete'),
    # Function based views for BookInstances
    path('my_books2/', views.user_books, name='my-books2'),
    path('my_books2/<uuid:instance_id>', views.user_book, name='my-books2'),
    path('my_books2/<uuid:pk>/update2', views.update_book_instance, name='update2'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('my_books/create2/', views.create_new_book_instance, name='create2'),

]
