from django.test import TestCase
from .models import Course, Chapter, Question, Exam, ExamQuestion, Answer, Enrollment, Request, FileContent, VideoContent
from django.core.exceptions import ValidationError
from accounts.models import Professor, Student, User 
import uuid



class CourseModelTest(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)

    def test_course_str(self):
        self.assertEqual(str(self.course), "Math 101")

    def test_get_number_of_chapters(self):
        Chapter.objects.create(title="Chapter 1", course=self.course)
        self.assertEqual(self.course.get_number_of_chapters(), 1)

    def test_get_absolute_url(self):
        self.assertEqual(self.course.get_absolute_url(), f"/courses/{self.course.pk}/")


class ChapterModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.chapter = Chapter.objects.create(title="Chapter 1", course=self.course)

    def test_chapter_str(self):
        self.assertEqual(str(self.chapter), "Math 101 - Chapter 1")

    def test_get_absolute_url(self):
        self.assertEqual(self.chapter.get_absolute_url(), f"/chapters/{self.chapter.pk}/")


class QuestionModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.chapter = Chapter.objects.create(title="Chapter 1", course=self.course)
        self.question = Question.objects.create(
            chapter=self.chapter,
            question="What is 2 + 2?",
            difficulty="Simple",
            objective="Understanding"
        )

    def test_question_str(self):
        self.assertEqual(str(self.question), "Math 101 - Chapter 1 - What is 2 + 2?")


class AnswerModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.chapter = Chapter.objects.create(title="Chapter 1", course=self.course)
        self.question = Question.objects.create(
            chapter=self.chapter,
            question="What is 2 + 2?",
            difficulty="Simple",
            objective="Understanding"
        )
        self.answer = Answer.objects.create(question=self.question, answer="4", is_correct=True)

    def test_answer_str(self):
        self.assertEqual(str(self.answer.title), "4")

    def test_clean_limit_answers(self):
        Answer.objects.create(question=self.question, answer="3", is_correct=False)
        Answer.objects.create(question=self.question, answer="5", is_correct=False)
        Answer.objects.create(question=self.question, answer="6", is_correct=True)
        
        with self.assertRaises(ValidationError):
            Answer.objects.create(question=self.question, answer="6", is_correct=False)
            


class ExamModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.exam = Exam.objects.create(course=self.course, title="Midterm Exam")

    def test_exam_str(self):
        self.assertEqual(str(self.exam), "Midterm Exam")

    def test_get_absolute_url(self):
        self.assertEqual(self.exam.get_absolute_url(), f"/exams/{self.exam.pk}/")


class EnrollmentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        student =User.objects.create_user(
            email='testuserr@example.com',
            password='PyDevAzmii@123',
            username='pydevazmii',
            phone_number='01126732635',
            role='Student',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.student = Student.objects.get(user = student)
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course)

    def test_enrollment_str(self):
        self.assertEqual(str(self.enrollment), "pydevazmii - Math 101")


class RequestModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        student =User.objects.create_user(
            email='testuserr@example.com',
            password='PyDevAzmii@123',
            username='pydevazmii',
            phone_number='01126732635',
            role='Student',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.student = Student.objects.get(user = student)
        self.request = Request.objects.create(student=self.student, course=self.course)

    def test_request_str(self):
        self.assertEqual(str(self.request), "pydevazmii - Math 101")

    def test_approved_enrollment_creation(self):
        Request.objects.create(student=self.student, course=self.course, status='Approved')
        enrollment = Enrollment.objects.get(student=self.student, course=self.course)
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)

    def test_denied_enrollment_creation(self):
        Request.objects.create(student=self.student, course=self.course, status='Declined')
        self.assertFalse(Enrollment.objects.filter(student=self.student, course=self.course).exists())


class ExamQuestionModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.chapter = Chapter.objects.create(title="Chapter 1", course=self.course)
        self.question = Question.objects.create(
            chapter=self.chapter,
            question="What is 2 + 2?",
            difficulty="Simple",
            objective="Understanding"
        )
        self.exam = Exam.objects.create(course=self.course, title="Midterm Exam")
        self.exam_question = ExamQuestion.objects.create(exam=self.exam, question=self.question)

    def test_exam_question_str(self):
        self.assertEqual(str(self.exam_question.question.title), "What is 2 + 2?")

    def test_clean_exam_question_course_constraint(self):
        another_course = Course.objects.create(title="Science 101", professor=self.professor)
        another_chapter = Chapter.objects.create(title="Chapter 2", course=another_course)
        another_question = Question.objects.create(
            chapter=another_chapter,
            question="What is 3 + 3?",
            difficulty="Simple",
            objective="Understanding"
        )
        exam_question = ExamQuestion(exam=self.exam, question=another_question)
        with self.assertRaises(ValidationError):
            exam_question.clean()


class FileContentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.chapter = Chapter.objects.create(title="Chapter 1", course=self.course)
        self.file_content = FileContent.objects.create(file="media/test_image.jpg", chapter=self.chapter)

    def test_file_content_str(self):
        self.assertEqual(str(self.file_content), "media/test_image.jpg")


class VideoContentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            password='PyDevAzmi@123',
            username='pydevazmi',
            phone_number='01126732635',
            role='Professor',
        )
        self.professor = Professor.objects.get(user=user)
        self.course = Course.objects.create(title="Math 101", professor=self.professor)
        self.chapter = Chapter.objects.create(title="Chapter 1", course=self.course)
        self.video_content = VideoContent.objects.create(url="http://example.com/video", chapter=self.chapter)

    def test_video_content_str(self):
        self.assertEqual(str(self.video_content), "http://example.com/video")

