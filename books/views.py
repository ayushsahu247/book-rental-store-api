from books.models import Book, Genre
from books.serializers import BookSerializer
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import AppUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from book_rental_store.authentication import CsrfExemptSessionAuthentication
# Create your views here.

class Books(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        genre_id = request.data.get("genre_id")
        if genre_id:
            genre_ob = Genre.objects.filter(id=int(genre_id))
            if genre_ob.exists():
                books = Book.objects.filter(genre=genre_ob.first())
            else:
                return Response({"message": "This genre does not exist"})
        else:
            books = Book.objects.all()
        data = {}
        for book in books:
            genres = book.genre.all()
            genre_list = ""
            for genre in genres:
                genre_list += genre.genre + ', '
            data[book.id] = {"owner": {"username": book.app_user.user.username, "contact": book.app_user.contact }   , "name":book.name, "genre": genre_list}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            app_user = AppUser.objects.get(user_id=request.user.id)
            book = Book.objects.get_or_create(name=request.data["name"], app_user=app_user)[0]
            genre_list = request.data.get("genre")
            if genre_list:
                for genre_id in genre_list.split(','):
                    genre_object = Genre.objects.filter(id=int(genre_id))
                    if genre_object.exists():
                        book.genre.add(genre_object.first())
            book.save()
            return Response({"message": f'Book {book.name} created.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)
        # how to add the id of the current user's app_user instance in the serializer data?

class GetGenre(APIView):
    def get(self, request):
        genre_objects = Genre.objects.all()
        data = {}
        for g_ob in genre_objects:
            data[g_ob.id] = g_ob.genre
        return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_or_delete_genre(request):
    book_id=request.data.get("book_id")
    genre_list = request.data.get("genre")
    if not book_id:
        return Response({"message": "Select a book to add genre"})
    if not genre_list:
        return Response({"message": "Give genre_ids to add genre to selected book"})
    try:
        book = Book.objects.get(id=int(book_id))
        for g_id in genre_list.split(','):
            if int(g_id)>0:
                g_ob = Genre.objects.filter(id=int(g_id))
                if g_ob.exists():
                    g_ob=g_ob.first()
                    if g_ob not in book.genre.all():
                        book.genre.add(g_ob)
                    else:
                        print(f"{g_ob} already added in this book's genres")
            else:
                g_ob = Genre.objects.filter(id=-int(g_id))
                if g_ob.exists():
                    g_ob=g_ob.first()
                    if g_ob in book.genre.all():
                        book.genre.remove(g_ob)
                    else:
                        print(f"{g_ob} is not in this book's genre so can not be deleted.")
        book.save()
        return Response({"message":f"Requested genres added to book {book.name} id {book.id}"})
    except Book.DoesNotExist:
        return Response({"message": "Give a valid book_id"})