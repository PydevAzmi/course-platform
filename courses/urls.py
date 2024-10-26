from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('courses/', views.courses, name='courses'),
    path('courses/<uuid:pk>/', views.CourseView.as_view(), name='course_detail'),
    path('courses/<uuid:pk>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<uuid:pk>/exams/', views.ExamListView.as_view(), name='course_exams'),
    path('courses/<uuid:pk>/exams/create/', views.ExamCreateView.as_view(), name='create_exams'),
    path('courses/edit/', views.prof_courses, name='dashboard'),

    path('exams/', views.exams, name='exams'),
    path('exams/<uuid:pk>/', views.exam_detail, name='exam_detail'),
    path('exams/create/', views.create_exam, name='create_exam'),
]