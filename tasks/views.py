from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task
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

def create_task(request):
    form=TaskModelForm()
    if request.method=='POST':
        form=TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            
            context={'form':form,
                     'message':'Task added successfully!!'}
            return render(request,'task_form.html',context)

    context={'form':form}
    return render(request,'task_form.html',context)
