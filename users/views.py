from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm,CustomRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator



# Create your views here.


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
        