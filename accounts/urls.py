from django.urls import path, include
from . import views

urlpatterns = [
    path("<uuid:user_pk>/password/", views.password_change , name = "password_change"),
    path('', include('allauth.urls')),
    path("signup/", views.signup , name = "signup"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
]