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
