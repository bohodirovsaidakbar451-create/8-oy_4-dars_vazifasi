from django.urls import path

from .views import (
    GenreListCreateAPIView,
    GenreDetailAPIView,
    BookListCreateAPIView,
    BookDetailAPIView,
    CommentListCreateAPIView,
    CommentDetailAPIView
)

urlpatterns = [
    path('genres/', GenreListCreateAPIView.as_view()),
    path('genres/<int:genre_id>/', GenreDetailAPIView.as_view()),
    path('books/', BookListCreateAPIView.as_view()),
    path('books/<int:book_id>/', BookDetailAPIView.as_view()),
    path('comments/', CommentListCreateAPIView.as_view()),
    path('comments/<int:comment_id>/', CommentDetailAPIView.as_view()),
]
