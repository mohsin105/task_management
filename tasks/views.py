from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("This is the task management website home page!")

def dashboard(request):
    return HttpResponse('This is the dashboard page!')
