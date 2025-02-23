from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm,CustomRegistrationForm,AssignRoleForm,CreateGroupForm,LoginForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import reverse_lazy


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
            user.is_active=False
            print(form.cleaned_data)
            user.save()

            messages.success(request,"A confirmation mail sent to your email. please check")
            return redirect('sign-in')
        else:
            print("Properly fill up the form")


    return render(request,'registration/register.html',{'form':form})

# form handling is done on front-end
# def sign_in(request):
#     if request.method=='POST':
#         print(request.POST)
#         username=request.POST.get('username')
#         password=request.POST.get('password')

#         user=authenticate(request,username=username,password=password)

#         if user is not None:
#             login(request,user)
#             return redirect('home')
#     return render(request,'registration/login.html')

# sign_in with default authentication form
def sign_in(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
            
    return render(request,'registration/login.html',{'form':form})

#CBV of sign_in 

class CustomLoginView(LoginView):
    form_class=LoginForm

    def get_success_url(self):
        next_url=self.request.GET.get('next')

        if next_url:
            return next_url
        else:
            return super().get_success_url() #the url set in settings as LOGIN_REDIRECT_URL

@login_required
def sign_out(request):
    if request.method=='POST':
        logout(request)
        return redirect('sign-in')

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
    context={'users':users}
    return render(request,'admin/dashboard.html',context)

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignRoleForm()

    if request.method =='POST':
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)

            messages.success(request,f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')

    context={'form':form}
    return render(request,'admin/assign_role.html',context)

@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method=='POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f'Group {group.name} created successfully')
            return redirect('create-group')
    
    context={'form':form}
    return render(request,'admin/create_group.html',context)

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups=Group.objects.prefetch_related('permissions').all()
    context={'groups':groups}
    return render(request,'admin/group_list.html',context)

class ProfileView(TemplateView):
    template_name='accounts/profile.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs) #ekhane kwargs argument dite hoy keno? 
        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['name']=user.get_full_name()
        context['member_since']=user.date_joined
        context['last_login']=user.last_login

        return context

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

        