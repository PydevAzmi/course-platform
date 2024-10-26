from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('courses/', views.courses, name='courses'),
    path('my-courses/', views.user_courses, name='my-courses'),

    path('courses/<uuid:pk>/', views.CourseView.as_view(), name='course_detail'),
    path('courses/<uuid:pk>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<uuid:pk>/exams/', views.CoursExamListView.as_view(), name='course_exams'),
    path('courses/<uuid:pk>/exams/delete/', views.ExamDeleteView.as_view(), name='delete_exam'),
    path('courses/<uuid:pk>/exams/create/', views.ExamCreateView.as_view(), name='create_exams'),

    path('exams/', views.ExamListView.as_view(), name='exams'),
    path('exams/<uuid:pk>/', views.ExamView.as_view(), name='exam_detail'),


]