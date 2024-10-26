from django import forms
from .models import Course, Chapter, Question, Answer, Enrollment, Request, VideoContent, FileContent, Exam, ExamQuestion

class ExamQuestionForm(forms.ModelForm):
    class Meta:
        model = ExamQuestion
        fields = ['exam', 'question']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter questions to only show questions related to the selected course
        if self.instance and self.instance.exam:
            self.fields['question'].queryset = Question.objects.filter(chapter__course=self.instance.exam.course)

class ExamForm(forms.ModelForm):
    questions_per_chapter = forms.IntegerField(min_value=1, initial=1)
    simple_reminding_questions = forms.IntegerField(min_value=0, initial=1)
    simple_understanding_questions = forms.IntegerField(min_value=0, initial=1)
    simple_creativity_questions = forms.IntegerField(min_value=0, initial=1)
    difficult_reminding_questions = forms.IntegerField(min_value=0, initial=1)
    difficult_understanding_questions = forms.IntegerField(min_value=0, initial=1)
    difficult_creativity_questions = forms.IntegerField(min_value=0, initial=1)
    class Meta:
        model = Exam
        fields = [
            'title',
            'questions_per_chapter' ,
            'simple_reminding_questions',
            'simple_understanding_questions',
            'simple_creativity_questions',
            'difficult_reminding_questions',
            'difficult_understanding_questions',
            'difficult_creativity_questions',
            ]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer','is_correct']


class FileContentForm(forms.ModelForm):
    class Meta:
        model = FileContent
        fields = ['file']


class VideoContentForm(forms.ModelForm):
    class Meta:
        model = VideoContent
        fields = ['url']


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'image']
    

