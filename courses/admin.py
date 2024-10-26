from django.contrib import admin
from .models import ( 
    Course, Chapter,
    ExamQuestion, Question,
    Answer, Enrollment, Request,
    VideoContent, FileContent, 
    Exam
    )

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class VideoContentInline(admin.TabularInline):
    model = VideoContent
    extra = 1

class FileContentInline(admin.TabularInline):
    model = FileContent
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]

class ChapterAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, VideoContentInline, FileContentInline]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class AnswerAdmin(admin.ModelAdmin):
    fields = [ 'answer', 'is_correct']

admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Enrollment)
admin.site.register(Request)
admin.site.register(VideoContent)
admin.site.register(FileContent)
admin.site.register(Exam)
admin.site.register(ExamQuestion)