from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course, Chapter, Enrollment, Question, Answer, VideoContent, Exam
# Create your views here.

def home(request):
    context = {
        'courses': Course.objects.all()[:3]
    }
    return render(request, 'courses/home.html', context)


def courses(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'courses/home.html', context)


def course_detail(request, pk):
    course = Course.objects.get(id=pk)
    context = {
        'course': course
    }
    return render(request, 'courses/home.html', context)

def exams(request):
    context = {
        'courses': Exam.objects.all()
    }
    return render(request, 'courses/home.html', context)
