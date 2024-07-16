from django.urls import path

from . import views

urlpatterns = [
    path("books/", views.books_list, name="books_list"),
    path("book/<int:pk>/", views.detail_view, name="detail_view"),
    path("", views.home, name="home"),
]
