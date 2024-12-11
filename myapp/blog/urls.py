from django.urls import path
from . import views


app_name="blog"

urlpatterns = [
    path("",views.index,name="index"),
    path("post/<str:slug>",views.detail,name="details"),
    path("contact",views.contact,name="contact"),
    path("about",views.about,name="about"),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("logout",views.logout,name="logout"),
    path("newPost",views.newPost,name="newPost"),
    path('editPost/<int:post_id>',views.editPost,name="editPost"),
    path('deletePost/<int:post_id>',views.deletePost,name="deletePost"),
    path('publishPost/<int:post_id>',views.publishPost,name="publishPost"),

    
    
]
