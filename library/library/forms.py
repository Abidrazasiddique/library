from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from .models import Author, Book, BorrowRecord


class AuthorForm(forms.ModelForm):
    """Form for adding/editing authors with email validation."""

    class Meta:
        model = Author
        fields = ['name', 'email', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author biography',
                'rows': 4
            }),
        }

    def clean_email(self):
        """Validate email field with custom validation."""
        email = self.cleaned_data.get('email')
        if email:
            # Check for valid email format
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError:
                raise ValidationError('Please enter a valid email address.')

            # Check for duplicate email (excluding current instance for updates)
            existing = Author.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('An author with this email already exists.')

        return email


class BookForm(forms.ModelForm):
    """Form for adding/editing books with author dropdown."""

    class Meta:
        model = Book
        fields = ['title', 'genre', 'published_date', 'author']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate author dropdown with all authors from database
        self.fields['author'].queryset = Author.objects.all()
        self.fields['author'].empty_label = "Select an author"


class BorrowRecordForm(forms.ModelForm):
    """Form for adding/editing borrow records."""

    class Meta:
        model = BorrowRecord
        fields = ['user_name', 'book', 'borrow_date', 'return_date']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter borrower name'
            }),
            'book': forms.Select(attrs={
                'class': 'form-control'
            }),
            'borrow_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'return_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate book dropdown with all books from database
        self.fields['book'].queryset = Book.objects.all()
        self.fields['book'].empty_label = "Select a book"
        self.fields['return_date'].required = False

    def clean(self):
        """Validate that return_date is not before borrow_date."""
        cleaned_data = super().clean()
        borrow_date = cleaned_data.get('borrow_date')
        return_date = cleaned_data.get('return_date')

        if borrow_date and return_date:
            if return_date < borrow_date:
                raise ValidationError(
                    'Return date cannot be earlier than borrow date.'
                )

        return cleaned_data
