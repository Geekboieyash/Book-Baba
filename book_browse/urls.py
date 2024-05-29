from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('books/', views.books, name='books'),
    path('submit-book/', views.submit_book, name='submit_book'),
]
