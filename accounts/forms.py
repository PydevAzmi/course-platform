from django import forms
from django.contrib.auth import get_user_model
from .models import Student, Professor
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

User = get_user_model()

class RegisterationForm(UserCreationForm):
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email is already exists with deffirent user")
       
       return self.cleaned_data
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ( "email",)

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', "profile_image"]

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']

class ProfessorEditForm(forms.ModelForm):
    class Meta:
        model = Professor
        exclude = ['user']