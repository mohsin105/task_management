from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
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
    employees=Employee.objects.all()
    form=TaskForm(employees=employees)
    if request.method=='POST':
        form=TaskForm(request.POST,employees=employees)
        if form.is_valid():
            data=form.cleaned_data
            #extracting each field value for this data
            title=data.get('title')
            description=data.get('description')
            due_date=data.get('due_date')
            assigned_to=data.get('assigned_to')

            task=Task.objects.create(title=title,description=description,due_date=due_date)

            # adding employee to task.assigned_to field (m2m field)
            for emp_id in assigned_to:
                emp=Employee.objects.get(id=emp_id)
                task.assigned_to.add(emp)
            
            return HttpResponse('Task added successfully!!')

    context={'form':form}
    return render(request,'task_form.html',context)
