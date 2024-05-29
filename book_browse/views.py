from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from string import Template
import environ
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import BookSearch, SubmitBook

from rest_framework import generics
from .models import Book, Interaction
from .forms import SubmitBook 

env = environ.Env()
env.read_env()  # reading .env file

key = env.str("API_KEY")

from django.shortcuts import render

class IndexView:
    def get(self, request):
        # Your logic for handling the index view (e.g., render a template)
        context = {}  # Replace with your context data if needed
        return render(request, 'index.html', context)


def index(request):
    form = BookSearch()
    return render(request, "book_browse/index.html", {"form": form})


def books(request):

    author = request.GET.get("author", False)
    search = (
        author
        if request.GET.get("search", False) == ""
        else request.GET.get("search", False)
    )

    if (search == False and author == False) or (search == "" and author == ""):
        return redirect("/")

    queries = {"q": search, "inauthor": author, "key": key}
    print(queries)
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=queries)
    print(r)
    if r.status_code != 200:
        return render(
            request,
            "book_browse/books.html",
            {
                "message": "Sorry, there seems to be an issue with Google Books right now."
            },
        )

    data = r.json()

    if not "items" in data:
        return render(
            request,
            "book_browse/books.html",
            {"message": "Sorry, no books match that search term."},
        )

    fetched_books = data["items"]
    books = []
    for book in fetched_books:
        book_dict = {
            "title": book["volumeInfo"]["title"],
            "image": (
                book["volumeInfo"]["imageLinks"]["thumbnail"]
                if "imageLinks" in book["volumeInfo"]
                else ""
            ),
            "authors": (
                ", ".join(book["volumeInfo"]["authors"])
                if "authors" in book["volumeInfo"]
                else ""
            ),
            "publisher": (
                book["volumeInfo"]["publisher"]
                if "publisher" in book["volumeInfo"]
                else ""
            ),
            "info": book["volumeInfo"]["infoLink"],
            "popularity": (
                book["volumeInfo"]["ratingsCount"]
                if "ratingsCount" in book["volumeInfo"]
                else 0
            ),
        }
        books.append(book_dict)

    def sort_by_pop(e):
        return e["popularity"]

    books.sort(reverse=True, key=sort_by_pop)

    return render(request, "book_browse/books.html", {"books": books})

 

def submit_book(request):
  if request.method == 'POST':
    form = SubmitBook(request.POST)
    if form.is_valid():
      # Process valid form data
      title = form.cleaned_data['title']
      author = form.cleaned_data['author']
      # Save book data to your database
      new_book = Book.objects.create(title=title, author=author)
      # ... (handle successful book creation)
      return redirect('index')  # Redirect to homepage after successful submission
    else:
      # Handle form errors
      return render(request, 'submit_book.html', {'form': form})
  else:
    form = SubmitBook()  # Create an empty form for GET requests
  return render(request, 'submit_book.html', {'form': form})


def like_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    interaction, created = Interaction.objects.get_or_create(
        user=request.user, book=book, like=True)

    like_count = book.interactions.filter(like=True).count()  # Get like count
    return JsonResponse({'likeCount': like_count})