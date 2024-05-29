from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('book_browse.urls')),
    path('admin/', admin.site.urls),
]
