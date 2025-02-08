from django.shortcuts import render

# Create your views here.

def home(request):
    # return HttpResponse("This is the task management website home page!")
    return render(request,'home.html')
