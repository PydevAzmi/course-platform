from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login
from django.urls import reverse
from .forms import UserEditForm, StudentEditForm, ProfessorEditForm, RegisterationForm, PasswordChangeForm
from .models import Student, Professor

User = get_user_model()
# Create your views here.

@login_required()
def profile(request):
    user = User.objects.get(id = request.user.id)
    context ={
        "user" : user 
    }
    return render(request, "profile/profile.html",context )

def signup(request):
    signup_form = RegisterationForm
    if request.method == "POST":
        signup_form = RegisterationForm(data=request.POST)
        if signup_form.is_valid():
            signform = signup_form.save(commit=False)
            signform.role = "Student"
            signform.save()
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password1']
            user = authenticate(email=email,password=password)
            login(request, user)
            return redirect(reverse('profile'))

    return render(request, "account/signup.html", {"form" : signup_form})

@login_required()
def profile_edit(request):
    user = request.user
    user_form = UserEditForm( instance= user)

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance = user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('profile'))
    context= {
        "form" : user_form,
    }

    return render(request, "profile/profile_edit.html", context)

@login_required()
def password_change(request, user_pk):
    user=request.user
    if user != User.objects.get(id = user_pk):
        return redirect(reverse('profile'))
    password_form = PasswordChangeForm(user)
    if request.method == "POST":
        password_form = PasswordChangeForm(user = user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            password = password_form.cleaned_data['new_password1']
            user = authenticate(username=user.email ,password=password)
            login(request, user)
            return redirect(reverse('profile'))

    return render(request, "account/password_change.html", {"form" : password_form})