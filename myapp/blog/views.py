from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
import logging 
from .models import Post

#static Demo Data
# posts=[
#     {"id":1,"title":"Post 1","content":"Content of Post 1"},
#     {"id":2,"title":"Post 2","content":"Content of Post 2"},
#     {"id":3,"title":"Post 3","content":"Content of Post 3"},
#     {"id":4,"title":"Post 4","content":"Content of Post 4"},
# ]

posts=Post.objects.all()

def index(request):
    blog_title="Latest Post"
    return render(request,"index.html",{"blog_title":blog_title,"posts":posts})

def detail(request,slug):
    #static data
    # post=next((item for item in posts if item["id"]==int(post_id) ),None)
    # logger=logging.getLogger("TESTING")
    # logger.debug(f"post variable is {post}")
    
    try:
        post= Post.objects.get(slug=slug)
        
    except Post.DoesNotExist:
        raise Http404("Post does not Exist !")

    return render(request,"details.html",{"post":post})

def old_url_redirect(request):
    return redirect(reverse("blog:new_url"))

def new_url_view(request):
    return HttpResponse("This is the new page")