from django.shortcuts import render, HttpResponse

# Create your views here.
def homepage(request):
    return render(request, 'home/homepage.html')

def singlepost(request):
    return render(request, 'home/singlepost.html')

def about(request):
    return render(request, 'home/about.html')

def videoblog(request):
    return render(request, 'home/videoblog.html')

def contact(request):
    return render(request, 'home/contact.html')