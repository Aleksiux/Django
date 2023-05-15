from PIL import Image
from django.db import models
import uuid
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField


# Create your models here.

class Genre(models.Model):
    """For genre table in database"""
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField('Name', max_length=100, help_text='Enter type of genre:')

    def __str__(self):
        return self.name


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField('First name', max_length=100)
    last_name = models.CharField('Last name', max_length=100)
    description = HTMLField('Description', help_text='Enter author description:')

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

    def display_books(self):
        return ', '.join(book.title for book in self.books.all())


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    title = models.CharField('Title', max_length=200, help_text="Enter book title:")
    description = models.TextField('Description', max_length=1000, help_text='Enter books description:')
    isbn = models.CharField(
        'ISBN', max_length=13,
        help_text='ISBN nr.: <a href="https://www.isbn-international.org/content/what-isbn">ISBN code</a>'
    )
    genre = models.ManyToManyField(Genre, help_text='Enter books genre: ')
    cover = ResizedImageField('Cover', size=[300, 400], upload_to='covers', null=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())


class BookInstance(models.Model):
    instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique UUID code")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='book_instances')
    due_back = models.DateField('', null=True, blank=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Processing'),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    book_status = models.CharField(max_length=1, default='a', blank=True, choices=LOAN_STATUS, help_text='Book status')

    @property
    def is_overdue(self):
        if date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.book.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        """ Run the usual save function but also resize uploaded photo        """
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        # if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.photo.path)


class BookReview(models.Model):
    book_review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Review', max_length=2000)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = 'Review'
        ordering = ['-date_created']
