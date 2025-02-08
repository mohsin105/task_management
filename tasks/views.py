from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Employee,Task
from django.db.models import Q,Count
from django.contrib import messages
# Create your views here.
def home(request):
    # return HttpResponse("This is the task management website home page!")
    return render(request,'home.html')

def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def user_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

def manager_dashboard(request):
    type=request.GET.get('type','all') #if there is no 'type' keyword in request.GET dict, return 'all'

    

    # counting using aggregate

    task_count=Task.objects.aggregate(total=Count('id'),
                                      completed=Count('id',filter=Q(status='COMPLETED')),
                                      in_progress=Count('id',filter=Q(status='IN_PROGRESS')),
                                      pending=Count('id',filter=Q(status='PENDING')))

    # total_task=tasks.count()
    # completed_task=Task.objects.filter(status='COMPLETED').count()
    # in_progress_task=Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task=Task.objects.filter(status='PENDING').count()
    base_query=Task.objects.select_related('details').prefetch_related('assigned_to')
    if type=='completed':
        tasks=base_query.filter(status='COMPLETED')
    elif type=='in-progress':
        tasks=base_query.filter(status='IN_PROGRESS')
    elif type=='pending':
        tasks=base_query.filter(status='PENDING')
    elif type=='all':
        tasks=base_query.all()

    context={
        'tasks':tasks,
        'task_count':task_count
        # 'total_task':total_task,
        # 'completed_task':completed_task,
        # 'in_progress_task':in_progress_task,
        # 'pending_task':pending_task
    }
    return render(request,'dashboard/manager_dashboard.html',context)

# Create => C of CRUD
def create_task(request):
    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    if request.method=='POST':
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False) #object created but not save in DB
            task_detail.task=task
            task_detail.save()
            
            messages.success(request,'Task created successfully') 
            return redirect('create-task')
        
        else:
            messages.error(request,'Properly Fill Up the from')
            return redirect('create-task')

    context={'task_form':task_form,
             'task_detail_form':task_detail_form}
    return render(request,'task_form.html',context)

# Read=> R of CRUD
def show_task(request):
    tasks=Task.objects.all()
    context={'tasks':tasks}
    return render(request,'show_task.html',context)

# Update=> U of CRUD
def update_task(request,id):
    task=Task.objects.get(id=id)
    task_form=TaskModelForm(instance=task)
    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)
        

    if request.method == 'POST':
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task)

        task=task_form.save()
        task_detail=task_detail_form.save(commit=False)
        task_detail.task=task
        task_detail.save()

        messages.success(request,'Task Updated Successfully!!')
        return redirect('update-task',id)
    
    context={
        'task_form':task_form,
        'task_detail_form':task_detail_form
    }

    return render(request,'task_form.html',context)

# Delete=> D of CRUD
# delete is always a POST request. 
# so no need to write for GET request. 
def delete_task(request,id):
    if request.method=='POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,'Task Deleted successfully')
        return redirect('manager-dashboard')
    
    messages.error(request,'Something went wrong')
    return redirect('manager-dashboard')
