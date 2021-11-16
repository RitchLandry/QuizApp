from django.contrib.auth import logout
from django.urls import path
from .views import userLogin,registerUser,logout

urlpatterns = [
    path('',userLogin,name="login"),
    path('logout',logout,name="logout"),
    path('register/',registerUser,name="register")
    ]