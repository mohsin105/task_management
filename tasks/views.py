from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm,ProjectModelForm
from tasks.models import Task,Project
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
# Create your views here.

#test fr user passes test

def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

class CustomUserPassesTestMixin(UserPassesTestMixin):
    pass

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
# CBV of employee dashboard
class Employee_Dashboard(ContextMixin,UserPassesTestMixin,View):

    login_url='no-permission'
    redirect_field_name = 'no-permission'
    def test_func(self):
        return self.request.user.groups.filter(name='Employee').exists()
    def get(self,request,*args,**kwargs):
        return render(request,'dashboard/user_dashboard.html')




class ManagerDashboard(ListView):
    template_name='dashboard/manager_dashboard.html'
    model=Task
    context_object_name='tasks'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        task_count=Task.objects.aggregate(total=Count('id'),
                                      completed=Count('id',filter=Q(status='COMPLETED')),
                                      in_progress=Count('id',filter=Q(status='IN_PROGRESS')),
                                      pending=Count('id',filter=Q(status='PENDING')))
        context['task_count']=task_count
        return context
    
    def get_queryset(self):
        type=self.request.GET.get('type','all')
        base_query=Task.objects.select_related('details').prefetch_related('assigned_to')
        if type=='completed':
            query_set=base_query.filter(status='COMPLETED')
        elif type=='in-progress':
            query_set=base_query.filter(status='IN_PROGRESS')
        elif type=='pending':
            query_set=base_query.filter(status='PENDING')
        else:
            query_set=base_query.all()
        return query_set

# Create => C of CRUD

#CBV of create_task
# create_decorators=[login_required,permission_required('tasks.add_task',login_url='no-permission')]

# @method_decorator(create_decorators,name='dispatch')
class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required='tasks.add_task'
    # login_url='no-permission'
    login_url='sign-in'

    #as the mixin classes are inherited, the method_decorator is no longer needed. 

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['task_form']=kwargs.get('task_form',TaskModelForm)
        context['task_detail_form']=kwargs.get('task_detail_form',TaskDetailModelForm)
        return context

    def get(self,request,*args,**kwargs):
        # task_form=TaskModelForm
        # task_detail_form=TaskDetailModelForm
        # context={
        #     'task_form':task_form,
        #     'task_detail_form':task_detail_form
        # }
        context=self.get_context_data()
        return render(request,'task_form.html',context)

    def post(self,request,*args,**kwargs):
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,'Task created successfully')
            return redirect('create-task')
        else:
            messages.error(request,'Properly Fill Up the from')
            return redirect('create-task')


# Read=> R of CRUD

#CBV of show_task
view_task_decorators=[login_required,permission_required('tasks.view_task',login_url='no-permission')]

@method_decorator(view_task_decorators,name='dispatch')
class ViewTask(ListView):
    model=Task
    template_name='show_task.html'
    context_object_name='tasks'

    #apply custom queryset
    def get_queryset(self):
        queryset=Task.objects.select_related('project').prefetch_related('assigned_to').all()
        return queryset

# Update=> U of CRUD

#CBV of update_task

# update_task_decorators=[login_required,permission_required('tasks.change_task',login_url='no-permission')]

# @method_decorator(update_task_decorators,name='dispatch')
class UpdateTask(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model=Task
    form_class=TaskModelForm
    template_name='task_form.html'
    context_object_name='task'
    pk_url_kwarg='id'
    permission_required='tasks.change_task'
    login_url='no-permission' #didnt work when login passed but permission failed
    redirect_field_name='no-permission'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        task=self.get_object()
        context['task_form']=self.get_form()

        if hasattr(task,'details') and task.details:
            context['task_detail_form']=TaskDetailModelForm(instance=task.details)
        else:
            context['task_detail_form']=TaskDetailModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        task=self.get_object()
        task_form=TaskModelForm(request.POST,instance=self.get_object())
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES,instance=getattr(task,'details',None)) #zodi self.object er majhe details thake tahole sheta return korbe, na hoy none. 

        if task_form.is_valid() and task_detail_form.is_valid():
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,'Task Updated Successfully!!')
            return redirect('update-task',task.id)



# Delete=> D of CRUD
# delete is always a POST request. 
# so no need to write for GET request. 


class Delete_Task(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required='tasks.delete_task'
    login_url='no-permission'
    success_url=reverse_lazy('dashboard') #reverse_lazy is a must. 
    model=Task
    pk_url_kwarg='id'
    # redirect_field_name='dashboard'

    # def get_success_url(self):
    #     return 'dashboard'


#CBV of task_details

class TaskDetail(DetailView):
    model=Task
    template_name='task_details.html'
    context_object_name='task'
    pk_url_kwarg='task_id'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['status_choices']=Task.STATUS_CHOICES
        return context
    
    def post(self,request,*args,**kwargs):
        task=self.get_object() #gives the object which sent the request, the currently logged user
        selected_status=request.POST.get('task_status')
        task.status=selected_status
        task.save()
        return redirect('task-details',task.id)
    
class CreateProject(UserPassesTestMixin,CreateView):
    model=Project
    form_class=ProjectModelForm
    template_name='project_form.html'
    context_object_name='form'
    success_url=reverse_lazy('create-project')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
        # try using 
        # return is_admin(request.user)

    def form_valid(self, form):
        project_name = form.cleaned_data.get('name')
        does_exist = Project.objects.filter(name=project_name).exists()
        if does_exist:
            messages.error(self.request, "Project with Same Name already Exists!")
            return render(self.request,'project_form.html',self.get_context_data())
        
        messages.success(self.request, 'Project Created Successfully')
        return super().form_valid(form)

class ProjectList(ListView):
    model=Project
    template_name='project_list.html'
    context_object_name='projects'

    def get_queryset(self):
        return Project.objects.prefetch_related('task_list').all()

