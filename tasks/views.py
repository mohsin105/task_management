from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    # return HttpResponse("This is the task management website home page!")
    return render(request,'home.html')

def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def user_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

def manager_dashboard(request):
    return render(request,'dashboard/manager_dashboard.html')
