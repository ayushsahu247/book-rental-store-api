from django.urls import path
from core import views
urlpatterns = [
    path('register', views.Register.as_view(), name="register" ),
    path('login', views.login, name="login" ),
    path('logout', views.Logout.as_view(), name="logout" ),
    path('', views.GetCurrentUser.as_view()),
    path('get-user', views.get_user, name="get-user")
]