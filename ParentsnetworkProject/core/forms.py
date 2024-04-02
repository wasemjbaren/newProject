from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.forms import ModelForm

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            username = self.cleaned_data.get('username')
            user_id = self.instance.id if self.instance else None  # Get the user id if it's an update, otherwise set to None for new user
            existing_user = User.objects.filter(email=email).exclude(id=user_id).first()

            if existing_user:
                raise forms.ValidationError("This email address is already in use.")
            return email

        def clean_username(self):
            username = self.cleaned_data.get('username')
            email = self.cleaned_data.get('email')
            user_id = self.instance.id if self.instance else None
            existing_user = User.objects.filter(username=username).exclude(id=user_id).first()

            if existing_user:
                raise forms.ValidationError("This username is already taken.")
            return username

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super(TaskForm, self).__init__(*args, **kwargs)
        self.user = user  # Assign user to an instance variable

    class Meta:
        model = Task
        fields = ['text']

    def save(self, commit=True):
        instance = super(TaskForm, self).save(commit=False)
        instance.user = self.user  # Set the user for the task
        if commit:
            instance.save()
        return instance
    

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['task', 'duration']
        exclude = ['week', 'week_days', 'type']


