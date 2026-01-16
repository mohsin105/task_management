from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm,CustomRegistrationForm,AssignRoleForm,CreateGroupForm,LoginForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views import View
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import TemplateView,UpdateView,View,CreateView,ListView
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin

User=get_user_model()
admin_options =[
        {
            'title':'Groups',
            'url':'group-list',
        },
        {
            'title':'Projects',
            'url':'project-list',
        },
        {
            'title':'Tasks',
            'url':'view-task',
        },
        {
            'title':'Users',
            'url':'dashboard',
        },
    ]
# Create your views here.

class Greetings(View):
    greetings="Hello World!"

    def get(self,request):
        return HttpResponse(self.greetings)

class HiGreetings(Greetings):
    greetings='Hi World!'

#test for user passes test
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    if request.method == 'GET':
        form=CustomRegistrationForm()
    
    if request.method=="POST":
        form=CustomRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            print(user)
            user.set_password(form.cleaned_data.get('password1'))
            # user.is_active=False
            user.is_active=True #email verification on korle eta False koro. and def activate_user view te True koro.
            print(form.cleaned_data)
            user.save()

            messages.success(request,"A confirmation mail sent to your email. please check")
            return redirect('sign-in')
        else:
            print("Properly fill up the form")


    return render(request,'registration/register.html',{'form':form})


#CBV of sign_in 

class CustomLoginView(LoginView):
    form_class=LoginForm

    def get_success_url(self):
        next_url=self.request.GET.get('next')

        if next_url:
            return next_url
        else:
            return super().get_success_url() #the url set in settings as LOGIN_REDIRECT_URL



# class CustomLogOutView(LogoutView):
#     redirect_field_name='sign-in'

def activate_user(reqeust,user_id,token):
    user=User.objects.get(id=user_id)
    try:
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User Not found")

@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users=User.objects.all()
    
    context={
        'users':users,
        'admin_options':admin_options
        }
    return render(request,'admin/dashboard.html',context)



class AssignRole(UserPassesTestMixin,View):
    login_url='no-permission'
    redirect_field_name = 'no-permission'
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get(self,request,*args,**kwargs):
        form= AssignRoleForm()
        context={'form':form}
        return render(request,'admin/assign_role.html',context)

    def post(self,request,*args,**kwargs):
        form=AssignRoleForm(request.POST)
        id=kwargs.get('user_id')
        # print('user id:  ',id)
        user=User.objects.get(id=id)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)

            messages.success(request,f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')
    


class CreateGroup(UserPassesTestMixin,CreateView):
    model=Group
    template_name='admin/create_group.html'
    form_class=CreateGroupForm
    context_object_name='form'
    success_url=reverse_lazy('create-group')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def form_valid(self, form):
        messages.success(self.request,f'Group {form.cleaned_data.get('name')} created successfully')
        return super().form_valid(form)
    

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups=Group.objects.prefetch_related('permissions').all()
    context={
        'groups':groups,
        'admin_options':admin_options,
        }
    return render(request,'admin/group_list.html',context)

class GroupList(UserPassesTestMixin,ListView):
    model=Group
    context_object_name='groups'
    template_name='admin/group_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()
    
class ProfileView(TemplateView):
    template_name='accounts/profile.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs) #ekhane kwargs argument dite hoy keno? 
        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['name']=user.get_full_name()
        context['bio']=user.bio
        context['profile_image']=user.profile_image
        context['member_since']=user.date_joined
        context['last_login']=user.last_login

        return context

class EditProfileView(UpdateView):
    model=User
    form_class=EditProfileForm
    template_name='accounts/update_profile.html'
    context_object_name='form'

    def get_object(self):
        return self.request.user

    def form_valid(self,form):
        form.save()
        return redirect('profile')


class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class=CustomPasswordChangeForm

class CustomPasswordResetView(PasswordResetView):
    template_name='registration/reset_password.html'
    form_class=CustomPasswordResetForm
    success_url=reverse_lazy('sign-in')
    html_email_template_name ='registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['protocol']='https' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request,'A reset email sent, please check your email')
        return super().form_valid(form)
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='registration/reset_password.html'
    form_class=CustomPasswordResetConfirmForm
    success_url=reverse_lazy('sign-in')

    def form_valid(self,form):
        messages.success(self.request,'Password reset succefully' )
        return super().form_valid(form)

        