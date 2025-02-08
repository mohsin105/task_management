from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    password1=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','confirm_password'] 
        #by default, only fields that are declared in User model
    
    
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