from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    SAFE_METHODS
)
from .models import Genre, Book, Comment
from .serializers import GenreSerializer, GenreDetailSerializer, BookSerializer, BookDetailSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class GenreListCreateAPIView(ListCreateAPIView):
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        genres = Genre.objects.all().order_by("name")
        search = self.request.query_params.get("search")

        if search:
            genres = genres.filter(name__icontains=search)

        return genres


class GenreDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    lookup_field = "id"
    lookup_url_kwarg = "genre_id"

    def get_queryset(self):
        return Genre.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GenreDetailSerializer
        return GenreSerializer


class BookListCreateAPIView(ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        books = Book.objects.select_related("genre").order_by("-created")
        genre_id = self.request.query_params.get("genre")
        search = self.request.query_params.get("search")

        if genre_id and genre_id.isdigit():
            books = books.filter(genre_id=genre_id)

        if search:
            books = books.filter(title__icontains=search)

        return books

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookDetailSerializer
        return BookSerializer


class BookDetailAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "book_id"

    def get_queryset(self):
        return Book.objects.select_related("genre")

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookDetailSerializer
        return BookSerializer


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        comments = Comment.objects.select_related("user", "book").order_by("-created")
        book_id = self.request.query_params.get("book")

        if book_id and book_id.isdigit():
            comments = comments.filter(book_id=book_id)

        return comments

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.select_related("user", "book")
