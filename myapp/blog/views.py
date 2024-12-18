from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
import logging 
from .models import Post,AboutUs,Category
from django.core.paginator import Paginator
from .forms import ContactForm, PostForm,RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as authLogin,logout as authLogout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group

#static Demo Data
# posts=[
#     {"id":1,"title":"Post 1","content":"Content of Post 1"},
#     {"id":2,"title":"Post 2","content":"Content of Post 2"},
#     {"id":3,"title":"Post 3","content":"Content of Post 3"},
#     {"id":4,"title":"Post 4","content":"Content of Post 4"},
# ]


def index(request):
    blog_title="Latest Post"
    
    allPosts = Post.objects.filter(is_published=True).order_by('createdAt') 
    paginator = Paginator(allPosts, 9)
    pageNumber=request.GET.get("page")
    pageOption=paginator.get_page(pageNumber)
    
    
    return render(request,"index.html",{"blog_title":blog_title,"pageOption":pageOption})

@permission_required('blog.view_post',raise_exception=True)
def detail(request,slug):
 
    if request.user and not request.user.has_perm('blog.view_post'):
        return redirect('blog:index')
    
    try:
        post= Post.objects.get(slug=slug)
        
    except Post.DoesNotExist:
        raise Http404("Post does not Exist !")

    return render(request,"details.html",{"post":post})

def contact(request):
    if request.method=="POST":
        form= ContactForm(request.POST)
        name=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("message")
        logger=logging.getLogger("TESTING") 
        if form.is_valid():
            logger.debug(f"post data is {form.cleaned_data['name']}, {form.cleaned_data['email']}, {form.cleaned_data['message']}")
            successMessage="Your Email has been sent !"
            return render(request,"contact.html",{"form":form,"successMessage":successMessage})
        else:
            logger.debug("Form validation failed")
        return render(request,"contact.html",{"form":form,"name":name,"email":email,"message":message})
    return render(request,"contact.html")



def about(request):
    aboutUsContent=AboutUs.objects.first()
    if aboutUsContent is None or not aboutUsContent.content:
        aboutUsContent="There is no about content given."
    else:
        aboutUsContent=aboutUsContent.content
    return render(request,"about.html",{"aboutUsContent":aboutUsContent})

def register(request):
    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) 
            user.set_password(form.cleaned_data["password"])
            user.save()
            
            # adding user to reader group
            readers_group,_=Group.objects.get_or_create(name='Readers')
            user.groups.add(readers_group)
            
            messages.success(request,'Registration Successful. You can log in')
            return redirect("blog:login") 
            

    return render(request,"register.html",{"form":form})


def login(request):
    form=LoginForm()
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user=authenticate(username=username,password=password)
            if user is not None:
                authLogin(request,user)
                print("Login Successful")
                return redirect("blog:dashboard")  # redirect to dashboard
    return render(request,"login.html",{"form": form})


def dashboard(request):
    blogTitle="My Posts"
    allPosts = Post.objects.filter(user=request.user).order_by('createdAt')  
    paginator = Paginator(allPosts, 9)
    pageNumber=request.GET.get("page")
    pageOption=paginator.get_page(pageNumber)
    return render(request,"dashboard.html",{"blogTitle":blogTitle,"pageOption":pageOption})

def logout(request):
    authLogout(request)
    return redirect("blog:index")

@login_required
@permission_required('blog.add_post',raise_exception=True)
def newPost(request):
    categories=Category.objects.all()
    form=PostForm()
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect("blog:dashboard")
    return render(request,"newPost.html",{"categories":categories,"form":form})

@login_required
@permission_required('blog.change_post',raise_exception=True)

def editPost(request,post_id):
    categories=Category.objects.all()
    post=get_object_or_404(Post,id=post_id)
    form=PostForm()
    if request.method=="POST":
        form=PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:dashboard')
    
    return render(request,'editPost.html',{"categories":categories,"post":post,'form':form})

@login_required
@permission_required('blog.delete_post',raise_exception=True)
def deletePost(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.delete()
    return redirect("blog:dashboard")


@login_required
@permission_required('blog.can_publish',raise_exception=True)
def publishPost(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.is_published=True
    post.save()
    return redirect("blog:dashboard")