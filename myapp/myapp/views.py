from django.shortcuts import render

def custom404PageNotFound(request,exception):
    return render(request,"404.html",status=404)