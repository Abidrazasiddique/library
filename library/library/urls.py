from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/add/', views.AuthorCreateView.as_view(), name='author_add'),
    path('authors/<int:pk>/edit/', views.AuthorUpdateView.as_view(), name='author_edit'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),

    # Book URLs
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/add/', views.BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),

    # BorrowRecord URLs
    path('borrow-records/', views.BorrowRecordListView.as_view(), name='borrowrecord_list'),
    path('borrow-records/add/', views.BorrowRecordCreateView.as_view(), name='borrowrecord_add'),
    path('borrow-records/<int:pk>/edit/', views.BorrowRecordUpdateView.as_view(), name='borrowrecord_edit'),
    path('borrow-records/<int:pk>/delete/', views.BorrowRecordDeleteView.as_view(), name='borrowrecord_delete'),

    # Export
    path('export/', views.ExportToExcelView.as_view(), name='export_excel'),
]
