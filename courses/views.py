from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.genetic_algorithm import generate_exam
from .models import Course, Chapter, Enrollment, ExamQuestion, Question, Answer, VideoContent, Exam
from . import forms
# Create your views here.

def home(request):
    context = {
        'courses': Course.objects.all()[:3]
    }
    return render(request, 'courses/home.html', context)

@login_required
def dashboard(request):
    courses = Course.objects.filter(professor=request.user.professor_profile)
    paginator = Paginator(courses,20) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/course_edit_list.html', {"page_obj": page_obj})


def courses(request):
    courses = Course.objects.all()
    paginator = Paginator(courses,50) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/courses.html', {"page_obj": page_obj})


@login_required
def user_courses(request):
    user = request.user
    page_obj = None
    if user.role == 'Student':
        enrollments = user.student_profile.enrollments.all()
        courses = Course.objects.filter(enrollments__in=enrollments)
        paginator = Paginator(courses,50) 
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'courses/courses.html', context)


@login_required
def course_edit(request, pk):
    course = Course.objects.filter(id=pk).prefetch_related(
        'chapters',
        'chapters__questions',
        'chapters__questions__answers',
        'chapters__files',
        'chapters__videos',
        ).get()
    
    context = {
        'course': course
    }
    return render(request, 'courses/exam_detail.html', context)


@login_required
def exam_detail(request, pk):
    exam = Exam.objects.get(id=pk)
    context = {
        'exam': exam
    }
    return render(request, 'courses/exam_detail.html', context)


class CourseView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        context = {
            'course': course,
        }
        return render(request, 'course/course_detail.html', context)


class CourseUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, professor = request.user.professor_profile , id=pk)
        course_form = forms.CourseForm(instance=course)
        chapter_form = forms.ChapterForm()
        question_form = forms.QuestionForm()
        answer_form = forms.AnswerForm()
        file_form = forms.FileContentForm()
        video_form = forms.VideoContentForm()
        context = {
            'course': course,
            'course_form': course_form,
            'chapter_form': chapter_form,
            'question_form': question_form,
            'answer_form': answer_form,
            'file_form': file_form,
            'video_form': video_form,
        }
        return render(request, 'course/course_update.html', context)
    
    def post(self, request, pk):
        course = get_object_or_404(Course, pk)
        context = {
            'course': course
        }
        if request.method == 'POST':
            course_form = forms.CourseForm(request.POST, request.FILES, instance=course)
            chapter_form = forms.ChapterForm(request.POST)
            question_form = forms.QuestionForm(request.POST)
            answer_form = forms.AnswerForm(request.POST)
            file_form = forms.FileContentForm(request.POST, request.FILES)
            video_form = forms.VideoContentForm(request.POST, request.FILES)
            if course_form.is_valid() and chapter_form.is_valid() and question_form.is_valid() and answer_form.is_valid() and file_form.is_valid() and video_form.is_valid():
                course_form.save()
                chapter = chapter_form.save(commit=False)
                chapter.course = course
                chapter.save()
                question = question_form.save(commit=False)
                question.chapter = chapter
                question.save()
                answer = answer_form.save(commit=False)
                answer.question = question
                answer.save()
                file = file_form.save(commit=False)
                file.chapter = chapter
                file.save() 
                video = video_form.save(commit=False)
                video.chapter = chapter
                video.save()
                return redirect('course_detail', pk=course.id)
        return render(request, 'course/course_update.html', context)


class CoursExamListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        exams = Exam.objects.filter(course=course).all()
        context = {
            'course': course,
            'exams': exams,
        }
        return render(request, 'exam/course_exams.html', context)


class ExamCreateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        exams = Exam.objects.filter(course=course).all()
        form = forms.ExamForm()
        context = {
            'course': course,
            'exams': exams,
            'form': form,
        }
        return render(request, 'exam/exam_create.html', context)

    def post(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        min_questions = min([chapter.questions.count() for chapter in course.chapters.all() ]) 
        form = forms.ExamForm()
        context = {
            'course': course,
            'form': form,
            }
        
        if request.method == 'POST':
            exam_form = forms.ExamForm(request.POST)
            if exam_form.is_valid():
                simple_reminding_questions = exam_form.cleaned_data['simple_reminding_questions']
                difficult_reminding_questions = exam_form.cleaned_data['difficult_reminding_questions']
                simple_understanding_questions = exam_form.cleaned_data['simple_understanding_questions']
                difficult_understanding_questions = exam_form.cleaned_data['difficult_understanding_questions']
                simple_creativity_questions = exam_form.cleaned_data['simple_creativity_questions']
                difficult_creativity_questions = exam_form.cleaned_data['difficult_creativity_questions']
                qs_Per_ch = exam_form.cleaned_data['questions_per_chapter']
                total_levels = (
                    simple_reminding_questions + difficult_reminding_questions +
                    simple_understanding_questions + difficult_understanding_questions +
                    simple_creativity_questions + difficult_creativity_questions 
                    )
                qs_size = qs_Per_ch * course.chapters.count()
                if total_levels != qs_size and qs_Per_ch <= min_questions :
                    messages.warning(request, f'Questions per Chapter is {qs_Per_ch}, So the total number of questions must be equal to {qs_size}')
                    return render(request, 'exam/exam_create.html', context)
                genome = generate_exam(
                    course,
                    qs_Per_ch, 
                    simple_reminding_questions,
                    simple_understanding_questions,
                    simple_creativity_questions,
                    difficult_reminding_questions,
                    difficult_understanding_questions,
                    difficult_creativity_questions
                    )
                exam = exam_form.save(commit=False)
                exam.course = course
                exam.save()
                for question in genome:
                    ExamQuestion.objects.get_or_create(exam=exam, question=question)
                messages.success(request, 'Exam created successfully!')
                return redirect('course_exams', pk=course.id)
        return render(request, 'course/exam_create.html', context)


class ExamView(LoginRequiredMixin, View):
    def get(self, request, pk):
        exam = get_object_or_404(Exam, id=pk)
        
        form = forms.QuestionForm(questions =exam.questions.all()  )
        context = {
            'exam': exam,
            'form': form,
        }
        return render(request, 'exam/exam_detail.html', context)


    def post(self, request, pk):
        exam = get_object_or_404(Exam, id=pk)
        form = forms.QuestionForm(request.POST)
        context = {
            'exam': exam,
            'form': form,
        }
        if request.method == 'POST':
            if form.is_valid():
                print("Valiiiiiiiiiiiiiiiiiiiiiiiiid")
                # Handle Exam Attempts
                messages.success(request, 'Exam Attempts successfully!')
                return redirect('exams')
        return render(request, 'exam/exam_detail.html', context)


class ExamListView(LoginRequiredMixin, generic.ListView):
    model = Exam
    template_name = 'exam/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Student':
            enrollments = user.student_profile.enrollments.all()
            enrolled_courses = Course.objects.filter(enrollments__in=enrollments)
            exams = Exam.objects.filter(course__in=enrolled_courses)
        else:
            exams = Exam.objects.filter(course__in = Course.objects.filter(professor=user.professor_profile))
        return exams


class ExamDeleteView(LoginRequiredMixin, generic.DeleteView):
    def post(self, request, pk):
        if request.user.role == 'Student':
            messages.warning(request, 'You are not allowed to delete exams!')
            return redirect('exams')
        exam = get_object_or_404(Exam, id=pk)
        exam.delete()
        messages.success(request, 'Exam deleted successfully!')
        return redirect('exams')