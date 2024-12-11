from django.urls import path
from . import views


app_name="blog"

urlpatterns = [
    path("",views.index,name="index"),
    path("post/<str:slug>",views.detail,name="details"),
    path("contact",views.contact,name="contact"),
    path("about",views.about,name="about"),
    path("register",views.register,name="register"),
    
    
    
]
