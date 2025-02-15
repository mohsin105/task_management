from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Task
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from users.views import is_admin
# Create your views here.

#test fr user passes test

def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    # return render(request,'dashboard/dashboard.html')
    return redirect('no-permission')

@user_passes_test(is_employee,login_url='no-permission')
def employee_dashboard(request):
    return render(request,'dashboard/user_dashboard.html')

# @user_passes_test(is_manager,login_url='no-permission')
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
@login_required
@permission_required('tasks.add_task',login_url='no-permission')
def create_task(request):
    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    if request.method=='POST':
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)

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
@login_required
@permission_required('tasks.change_task',login_url='no-permission')
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
@login_required
@permission_required('tasks.delete_task',login_url='no-permission')
def delete_task(request,id):
    if request.method=='POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,'Task Deleted successfully')
        return redirect('manager-dashboard')
    
    messages.error(request,'Something went wrong')
    return redirect('manager-dashboard')

@login_required
@permission_required('tasks.view_task',login_url='no-permission')
def task_details(request,task_id):
    task=Task.objects.get(id=task_id)
    status_choices=Task.STATUS_CHOICES

    if request.method=='POST':
        selected_status=request.POST.get('task_status')
        print('new status: ',selected_status)
        task.status=selected_status
        task.save()
        return redirect('task-details',task_id)
    
    context={'task':task,'status_choices':status_choices}
    return render(request,'task_details.html',context)
