from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from core.serializers import UserSerializer, AppUserSerializer
from core.models import AppUser
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from book_rental_store.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from books.models import Book, Genre
# Create your views here.

class Register(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                return Response({"message":f' Username {user.username} is already taken. Pick a different username.'}, status=status.HTTP_200_OK)
            username=request.data['username']
            password=request.data['password']
            email=request.data["email"]
            user=User.objects.get_or_create(username=username, email=email)[0]
            user.set_password(password)
            user.save()
            print(user)
            app_user = AppUser.objects.get_or_create(user=user)
            return Response({"message":f"User {user.username} created"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]
    if request.method=='POST':
        if(request.user.is_authenticated):
            return Response({"message":f"Already logged in. Current User {request.user}"})
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user:
            auth.login(request, user)
            print(request.user.is_authenticated)
            return Response({'message':'successfully logged in'})
        else:
            return Response({'message':'invalid credentials'})

class Logout(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        print(request.user.is_authenticated)
        auth.logout(request)
        return Response({'message':'successfully logged out'})


class GetCurrentUser(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        if request.user:
            user = request.user
            app_user = AppUser.objects.get(user=user)
            serializer = AppUserSerializer(app_user)
            return Response({"user_info": {
                "id":user.id,
                "username": user.username,
                "contact":app_user.contact
            }}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"User unauthenticated"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_user(request):
    user = User.objects.filter(username=request.data.get("username"))
    if user.exists():
        user=user.first()
        books = Book.objects.filter(app_user=AppUser.objects.get(user=user))
        book_data = {}
        for book in books:
            genres = (", ").join( [_.genre for _ in book.genre.all()]  )
            book_data[book.id] = {"name": f"{book.name}", "genres": f"{genres}"}
        return Response({f"{user.username}": {
            "contact": f"{AppUser.objects.get(user=user).contact}",
            "books": book_data
            } 
        })