from rest_framework import viewsets

from .models import Book

from .serializer import BookSerializer

#I just made this to try the router but i realized that the basic url of django are more eassier and better

class BookViewSet(viewsets.ModelViewSet):
    queryset= Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'