from django.db import models


class Author(models.Model):
    """Model representing an author in the library system."""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book in the library system."""
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    published_date = models.DateField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author.name}"


class BorrowRecord(models.Model):
    """Model representing a borrow record for a book."""
    user_name = models.CharField(max_length=200)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_records'
    )
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.user_name} borrowed {self.book.title}"

    @property
    def is_returned(self):
        """Check if the book has been returned."""
        return self.return_date is not None
