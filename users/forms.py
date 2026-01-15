from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User=get_user_model() #the current user is assigned to User variable

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['username','password1','password2']:
            self.fields[field_name].help_text=None

class CustomRegistrationForm(forms.ModelForm):
    #manually declaring new form fields
    password1=forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter Password',
            'class':'w-full my-2 p-4 border-2 rounded-md shadow-md border-gray-400',
        }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Confirm the password',
            'class':'w-full my-2 p-4 border-2 border-gray-400 rounded-md shadow-md'
        }
    ))
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','confirm_password'] 
        #by default, only fields that are declared in User model

        widgets={
            'username':forms.TextInput(
                attrs={
                    'placeholder':'username',
                    'class':'w-full p-4 my-2 border-2 rounded-md shadow-md',
                }
            ),
            'first_name':forms.TextInput(
                attrs={
                    'placeholder':'First Name',
                    'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400',
                }
            ),
            'last_name':forms.TextInput(
                attrs={
                    'placeholder':'Last Name',
                    'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400'
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'placeholder':'Your Email',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            )
        }
    
    
    # Error validation for field-error
    def clean_password1(self):
        password1=self.cleaned_data.get('password1')
        errors=[]
        if len(password1)<8:
            errors.append("Password is less than 8 char")
        
        # elif re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password1):
        #     raise forms.ValidationError("use proper characters")
        if not re.search(r'[A-Z]',password1):
            errors.append('Password must include at least one uppercase letter.')
        
        if not re.search(r'[a-z]',password1):
            errors.append('Password must include at least one lowercase letter.')
        if not re.search(r'[0-9]',password1):
            errors.append('Password must include at least one number.')
        if not re.search(r'[@#$%^&+=]',password1):
            errors.append('Password must include at least one special character.')
        
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_exists=User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists!")
        
        return email


    # Error validation for non-field errors
    def clean(self):
        cleaned_data=super().clean()
        password1=cleaned_data.get('password1')
        confirm_password=cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError('Password did not match!!')
        
        return cleaned_data

#no model is related to this form, hence, normal form
class AssignRoleForm(forms.Form):
    role=forms.ModelChoiceField(queryset=Group.objects.all(),
                                empty_label='Select a role')

#create, update on a model can be done using modelform
class CreateGroupForm(forms.ModelForm):
    permissions=forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    class Meta:
        model=Group
        fields=['name','permissions']

        widgets={
            'name':forms.TextInput(
                attrs={
                    'placeholder':'Name of The User Group',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md'
                }
            ),
            'permissions':forms.CheckboxSelectMultiple(
                attrs={
                    'class':'p-4 my-2 border-2 border-gray-400 rounded-md font-semibold'
                }
            )
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs): #request by default chilo. keno dorkar nai ekhon?
        super().__init__( *args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder':'Enter your username',
            'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder':'Enter Your Password',
            'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400'
        })

class CustomPasswordChangeForm(PasswordChangeForm): #inherit Mixin here
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        for field in ['old_password','new_password1','new_password2']:
            self.fields[field].help_text = None
        
        self.fields['old_password'].widget.attrs.update({
            'placeholder':'Enter Current Password',
            'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400'
        })
        self.fields['new_password1'].widget.attrs.update({
            'placeholder':'New Password',
            'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400',
        })
        self.fields['new_password2'].widget.attrs.update({
            'placeholder':'Confirm New Password',
            'class':'w-full p-4 my-2 border-2 rounded-md shadow-md border-gray-400'
        })

class CustomPasswordResetForm(PasswordResetForm): #inherit Mixin here
    pass

class CustomPasswordResetConfirmForm(SetPasswordForm):#inherit Mixin here
    pass

class EditProfileForm(forms.ModelForm): #mixin user koro
    class Meta:
        model=CustomUser
        fields=['email','first_name','last_name','bio','profile_image']

        widgets={
            'email':forms.EmailInput(
                attrs={
                    'placeholder':'demo@gmail.com',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md',
                }
            ),
            'first_name':forms.TextInput(
                attrs={
                    'placeholder':'First Name',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md',
                }
            ),
            'last_name':forms.TextInput(
                attrs={
                    'placeholder':'Last Name',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            ),
            'bio':forms.Textarea(
                attrs={
                    'placeholder':'Your Bio',
                    'class':'w-full p-4 my-2 border-gray-500 rounded-md shadow-md',
                    'rows':8
                }
            ),
            'profile_image':forms.FileInput(
                attrs={

                }
            )
        }