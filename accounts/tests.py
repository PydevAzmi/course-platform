from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Student, Professor
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid
from django.core import mail

User = get_user_model()

class UserModelTest(TestCase):

    def setUp(self):
        """Setup test data."""
        self.test_email = 'testuser@example.com'
        self.test_password = 'testpassword@123'
        self.test_username = 'testuser'
        self.test_phone_number = '01126732635'
        self.test_profile_image = SimpleUploadedFile(name='media/test_image.jpg', content=b'', content_type='image/jpeg')
        self.test_role = 'Student'
        
    def test_create_user(self):
        """Test user creation with mandatory fields."""
        user = User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
            username=self.test_username,
            phone_number=self.test_phone_number,
            role=self.test_role,
        )
        self.assertEqual(user.email, self.test_email)
        self.assertTrue(user.check_password(self.test_password))
        self.assertEqual(user.username, self.test_username)
        self.assertEqual(user.phone_number, self.test_phone_number)
        self.assertEqual(user.role, self.test_role)
        self.assertEqual(user.is_active, True)
    
    def test_user_uuid_generation(self):
        """Test if UUID is automatically generated on user creation."""
        user = User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
            username=self.test_username,
            phone_number=self.test_phone_number,
            role=self.test_role,
        )
        self.assertIsInstance(user.id, uuid.UUID)

    def test_create_superuser(self):
        """Test superuser creation."""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123',
            username='adminuser',
            phone_number=self.test_phone_number,
            role='Professor',
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_fields_nullability(self):
        """Test that nullable fields can be left empty."""
        user = User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
            username=self.test_username,
            role=self.test_role,
        )
        self.assertIsNone(user.phone_number)
        self.assertIsNone(user.profile_image.name)

    def test_user_profile_image(self):
        """Test user profile image upload path."""
        user = User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
            username=self.test_username,
            phone_number=self.test_phone_number,
            profile_image=self.test_profile_image,
            role=self.test_role,
        )
        expected_path = f'profile_images/users/{self.test_username}/test_image.jpg'
        self.assertEqual(user.profile_image.name, expected_path)
    
    def test_user_unique_email(self):
        """Test that user emails must be unique."""
        User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
            username=self.test_username,
            phone_number=self.test_phone_number,
            role=self.test_role,
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email=self.test_email,
                password=self.test_password,
                username='anotheruser',
                phone_number='0987654321',
                role='Student',
            )

    def test_user_phone_max_exceeds_length(self):
        """Test that phone number length exceeds maximum allowed length."""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email=self.test_email,
                password=self.test_password,
                username=self.test_username,
                phone_number='012345678901234567890123456789012345678901234567890123456789012345678901',
                role=self.test_role,
            )
            

class UserProfileTest(TestCase):

    def setUp(self):
        """Setup test data."""
        self.professor_email = 'professor@example.com'
        self.professor_password = 'profpassword123'
        self.professor_username = 'professoruser'
        self.student_email = 'student@example.com'
        self.student_password = 'studentpassword123'
        self.student_username = 'studentuser'
        self.test_phone_number = '1234567890'
    
    def test_student_profile_created(self):
        """Test that a Student profile is created when a user with role 'Student' is created."""
        user = User.objects.create_user(
            email=self.student_email,
            password=self.student_password,
            username=self.student_username,
            phone_number=self.test_phone_number,
            role='Student',
        )
        # Check that the Student profile is created
        student_profile = Student.objects.get(user=user)
        self.assertEqual(student_profile.user, user)
        self.assertEqual(student_profile.user.role, 'Student')

    def test_professor_profile_created(self):
        """Test that a Professor profile is created when a user with role 'Professor' is created."""
        user = User.objects.create_user(
            email=self.professor_email,
            password=self.professor_password,
            username=self.professor_username,
            phone_number=self.test_phone_number,
            role='Professor',
        )
        # Check that the Professor profile is created
        professor_profile = Professor.objects.get(user=user)
        self.assertEqual(professor_profile.user, user)
        self.assertEqual(professor_profile.user.role, 'Professor')

    def test_profile_creation_signal_for_student(self):
        """Test that the post_save signal correctly creates a Student profile when a Student user is saved."""
        user = User.objects.create_user(
            email=self.student_email,
            password=self.student_password,
            username=self.student_username,
            phone_number=self.test_phone_number,
            role='Student',
        )
        # Check if Student profile was automatically created
        self.assertTrue(Student.objects.filter(user=user).exists())

    def test_profile_creation_signal_for_professor(self):
        """Test that the post_save signal correctly creates a Professor profile when a Professor user is saved."""
        user = User.objects.create_user(
            email=self.professor_email,
            password=self.professor_password,
            username=self.professor_username,
            phone_number=self.test_phone_number,
            role='Professor',
        )
        # Check if Professor profile was automatically created
        self.assertTrue(Professor.objects.filter(user=user).exists())

    def test_str_method_professor(self):
        """Test the __str__ method of the Professor model."""
        user = User.objects.create_user(
            email=self.professor_email,
            password=self.professor_password,
            username=self.professor_username,
            phone_number=self.test_phone_number,
            role='Professor',
        )
        professor_profile = Professor.objects.get(user=user)
        self.assertEqual(str(professor_profile), f'Prof. {user.username}')

    def test_str_method_student(self):
        """Test the __str__ method of the Student model."""
        user = User.objects.create_user(
            email=self.student_email,
            password=self.student_password,
            username=self.student_username,
            phone_number=self.test_phone_number,
            role='Student',
        )
        student_profile = Student.objects.get(user=user)
        self.assertEqual(str(student_profile), f'{user.username}')
