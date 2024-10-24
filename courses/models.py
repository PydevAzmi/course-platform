from django.db import models
from django.db.models import Q
import uuid
from django.forms import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ('Pending', _('Pending')),
    ('Approved', _('Approved')),
    ('Declined', _('Declined')),
]

DIFFICULTY_CHOICES = [
    ('Difficult', _('Difficult')),
    ('Simple', _('Simple')),
]

OBJECTIVE_CHOICES = [
    ('Remideing', _('Remideing')),
    ('Understanding', _('Understanding')),
    ('Creativity', _('Creativity')),
]

def file_path(instance, file_name):
    return f"files/{instance.chapter.course.professor}/{instance.chapter.course.title}/{instance.chapter.title}/{file_name}"

def file_path_image(instance, file_name):
    return f"files/{instance.professor}/courses/{instance.title}/{file_name}"

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Title"), max_length=50)
    professor = models.ForeignKey('accounts.Professor', verbose_name=_("professor"), related_name="courses", on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to=file_path_image, blank=True, null=True)
    date = models.DateField(auto_now_add=True, verbose_name=_("Date"))

    def __str__(self) -> str:
        return self.title
    
    def get_number_of_chapters(self):
        return self.chapters.all().count()
    
    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})


class ExamQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey('Exam', verbose_name=_("Exam"), on_delete=models.CASCADE, related_name='exam_questions')
    question = models.ForeignKey('Question', verbose_name=_("Question"), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('exam', 'question') 

    def clean(self):
        if self.question.chapter.course != self.exam.course:
            raise ValidationError(_("The question must belong to the same course as the exam"))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(_("Title"),max_length=255)
    created_date = models.DateTimeField(_("Created Date"),auto_now_add=True)
    dead_time = models.DateTimeField(_("Dead Time"), null=True, blank=True)
    questions = models.ManyToManyField('Question', verbose_name=_("Questions"), through=ExamQuestion, blank=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("exam_detail", kwargs={"pk": self.pk})
    

class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(_("Title"),max_length=255)
    upload_date = models.DateTimeField(_("Upload Date"),auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.course.title} - {self.title}'
    
    def get_absolute_url(self):
        return reverse("chapter_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['upload_date']


class FileContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(_("File"), upload_to=file_path, max_length=100)
    chapter = models.ForeignKey(Chapter, verbose_name=_("Chapter"), related_name="files", on_delete=models.CASCADE, null=True, blank=True)
    upload_date = models.DateTimeField(_("Upload Date"),auto_now_add=True)

    def __str__(self):
        return f'{self.file.name}'      


class VideoContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(_("Video Link"), max_length=200)
    chapter = models.ForeignKey(Chapter, verbose_name=_("Chapter"), related_name="videos", on_delete=models.CASCADE, null=True, blank=True)
    upload_date = models.DateTimeField(_("Upload Date"),auto_now_add=True)
    
    def __str__(self):
        return f'{self.url}'


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey(Chapter, verbose_name=_("chapter"), on_delete=models.CASCADE, related_name='questions')
    question = models.TextField(_("Question"))
    difficulty = models.CharField(_("Difficulty"), max_length=50, choices=DIFFICULTY_CHOICES)
    objective = models.CharField(_("Objective"), max_length=50, choices=OBJECTIVE_CHOICES)

    def __str__(self):
        return f'{self.chapter.course} - {self.chapter.title} - {self.question}'
    
    class Meta:
        ordering = ['chapter']

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField(_("Answer"))
    is_correct = models.BooleanField(_("Is Correct"), default=False)

    def __str__(self):
        return self.answer
    
    # validate that only 3 answers related to a question
    def clean(self):
        if not Answer.objects.filter(pk = self.pk).exists():
            if Answer.objects.filter(question=self.question).count() >= 3:
                raise ValidationError(_('Only 3 answers are allowed for each question'))



class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('accounts.Student',verbose_name=_('Student'), on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(_('Enrollment Date'), auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.student} - {self.course}'


class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('accounts.Student',verbose_name=_("Student"), on_delete=models.CASCADE, related_name='requests')
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(verbose_name=_("Status"), max_length=50, choices=STATUS_CHOICES, default="Pending")
    request_date = models.DateTimeField(verbose_name=_("Request Date"), auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.student} - {self.course}'
    
    def save(self, *args, **kwargs):
        exist = Enrollment.objects.filter(Q(student=self.student) & Q(course=self.course)).exists()
        if self.status == "Approved" and not exist :
            Enrollment.objects.create(
                student = self.student,
                course = self.course
            )
        super().save(*args, **kwargs)
