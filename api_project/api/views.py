
from rest_framework import generics
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()          # ✅ Query all Book objects
    serializer_class = BookSerializer      # ✅ Use BookSerializer for output
    # new viewset for full CRUD
class BookViewSet(viewsets. ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer