import os
import django
# Set environment variable > Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from accounts.models import User, Professor, Student
from courses.models import Course, Chapter, Exam, Question, Answer, Enrollment, Request, FileContent, VideoContent
import random
from faker import Faker

DIFFICULTY_CHOICES = [
    'Difficult', 
    'Simple',
]

OBJECTIVE_CHOICES = [
    'Remideing', 
    'Understanding', 
    'Creativity', 
]

fake = Faker()
def seed_users(n):
    images = ['profile-1.jpg', 'profile-2.jpg','profile-3.jpg','profile-4.jpg','profile-5.jpg','profile-6.jpg',
              'profile-7.jpg', 'profile-8.jpg','profile-9.jpg','profile-10.jpg','profile-11.jpg']
    roles = ["Student", "Professor"]
    role = random.choice(roles)
    for _ in range(n):
        image = f"../media/images/{random.choice(images)}"
        User.objects.create_user(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email=fake.email(),
            password=fake.password(length=12),
            username=fake.user_name(),
            profile_image=image,
            role="Professor",
        )
    print(f"successfully added {n} Users")


def seed_courses(n):
    images = ['course (1).jpg', 'course (2).jpg',
              'course (3).jpg','course (4).jpg',
              'course (5).jpg','course (6).jpg',
              'course (7).jpg', 'course (8).jpg',
              'course (9).jpg', 'course (10).jpg']
    profs = Professor.objects.all()
    for _ in range(n):
        image = f"../media/courses/{random.choice(images)}"
        Course.objects.create(
            title= fake.name(),
            image=image,
            professor = random.choice(profs),
        )
    print(f"successfully added {n} Courses")

def seed_courses_chapters():
    n = random.randint(7,12)
    for course in Course.objects.all():
        if course.chapters.count() == 0:
            for i in range(n):
                Chapter.objects.create(
                    title= f"chapter - {i}",
                    course = course,
                )
    print(f"successfully added chapters in all Courses")


def seed_cahpter_questions():
    difficulty = ["Simple", "Difficult"]
    objective = ["Creativity", "Understanding", "Remideing"]
    for chapter in Chapter.objects.all():
        if chapter.questions.count() == 0:
            for dif in difficulty:
                for obj in objective + objective:
                    Question.objects.create(
                        chapter = chapter,
                        question = fake.text(max_nb_chars=50),
                        difficulty = dif,
                        objective = obj,
                    )
    print(f"successfully added 12 questions in all Chapters")

def distroy_questions():
    for question in Question.objects.all():
        question.delete()
    print(f"successfully deleted all Questions")

def seed_questions_answers():
    for question in Question.objects.all():
        if question.answers.count() == 0:
            for _ in range(3):
                Answer.objects.create(
                    question = question,
                    answer = fake.text(max_nb_chars=50),
                    is_correct = False,
                )
    print(f"successfully added answers in all Questions")


def seed_correct_answers():
    for question in Question.objects.all():
        if not Answer.objects.filter(question=question, is_correct=True).exists():
            choice = random.choice(Answer.objects.filter(question=question).all())
            choice.is_correct = True
            choice.save()
    print(f"successfully added correct answers in all Questions")


def seed_enrollments():
    students = Student.objects.all()
    for student in students:
        course = random.choice(Course.objects.all())
        if not Enrollment.objects.filter(student=student, course=course).exists():
            Enrollment.objects.create(
                student = student,
                course = course,
                )
    print(f"successfully added enrollments in all Students")

def seed_files_videos():
    images = ['course (1).jpg', 'course (2).jpg',
              'course (3).jpg','course (4).jpg',
              'course (5).jpg','course (6).jpg',
              'course (7).jpg', 'course (8).jpg',
              'course (9).jpg', 'course (10).jpg']
    for chapter in Chapter.objects.all():
        FileContent.objects.create(
            chapter = chapter,
            file = f"../media/courses/{random.choice(images)}",
        )
        VideoContent.objects.create(
            chapter = chapter,
            url = fake.url()
        )
    print(f"successfully added content to all chapters")

if __name__ == "__main__":
    #seed_users(50)
    pass
