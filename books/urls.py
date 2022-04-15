from django.urls import path
from books import views

urlpatterns = [
    path('books', views.Books.as_view(), name='book-list' ),
    path('genre', views.GetGenre.as_view(), name='genre'),
    path('add-genre', views.add_or_delete_genre, name='add-genre')
]