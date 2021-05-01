# import Models (for model form)
from users.models import Profile
from django.contrib.auth.models import User

# Registration form (provided by Django | verification and all)
from django.contrib.auth.forms import UserCreationForm

# General forms from django
from django import forms 

# Registration form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    mobile = forms.CharField(max_length = 15)

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        return cleaned_data

    class Meta: # Give your form a metadata, i.e. 'anything which is not field'
        model = User
        fields = ['username', 'mobile', 'email', 'password1', 'password2']


# User can update his username, email by this form (custom model form)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
    

# User can update his profile picture by this form (custom model form)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


# custom user login form
class Login(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    mobile = forms.CharField(label='mobile', max_length=15)
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput())


