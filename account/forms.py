from django import forms
from account.models import User  
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):  
    username = forms.CharField(label="Username",max_length=50)  
    password = forms.CharField(label="Password", max_length = 100)  
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-2'


def validate_username(username):        
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists.")
    
def validate_email(user_email):        
    if User.objects.filter(email=user_email).exists():
        raise ValidationError("Email  already exists.")

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(label="First name",max_length=50)  
    last_name = forms.CharField(label="Last name",max_length=50)
    user_email = forms.EmailField(label="E-mail",max_length=50, validators=[validate_email])  
    username = forms.CharField(label="Username",max_length=50, validators=[validate_username])  
    password1 = forms.CharField(label="Password",max_length=50)  
    password2 = forms.CharField(label="Confirm password",max_length=50)  
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-1'

class UserprofileUpdate(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username" ,  "email" ]

    def __init__(self, *args, **kwargs):
        super(UserprofileUpdate, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-1'