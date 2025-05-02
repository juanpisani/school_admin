# core/tests/test_models.py
from django.test import TestCase
from ..models import Institution, Teacher, Student, Course, Classroom, Enrollment

class InstitutionModelTest(TestCase):
    def test_create_institution(self):
        institution = Institution.objects.create(name="Test School", address="123 Main St")
        self.assertEqual(institution.name, "Test School")
        self.assertEqual(institution.address, "123 Main St")
        self.assertEqual(str(institution), "Test School")

class TeacherModelTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")

    def test_create_teacher(self):
        teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            institution=self.institution
        )
        self.assertEqual(teacher.first_name, "John")
        self.assertEqual(teacher.last_name, "Doe")
        self.assertEqual(teacher.institution, self.institution)
        self.assertEqual(str(teacher), "John Doe")

class StudentModelTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")

    def test_create_student(self):
        student = Student.objects.create(
            first_name="Alice",
            last_name="Smith",
            date_of_birth="2005-08-15",
            email="alice.smith@example.com",
            institution=self.institution
        )
        self.assertEqual(student.first_name, "Alice")
        self.assertEqual(student.institution, self.institution)
        self.assertEqual(str(student), "Alice Smith")

class CourseModelTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")
        self.teacher = Teacher.objects.create(first_name="Bob", last_name="Johnson", email="bob@example.com", institution=self.institution)

    def test_create_course(self):
        course = Course.objects.create(name="Mathematics", institution=self.institution, primary_teacher=self.teacher)
        self.assertEqual(course.name, "Mathematics")
        self.assertEqual(course.institution, self.institution)
        self.assertEqual(course.primary_teacher, self.teacher)
        self.assertEqual(str(course), "Mathematics")

class ClassroomModelTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")

    def test_create_classroom(self):
        classroom = Classroom.objects.create(name="Room 101", capacity=35, institution=self.institution)
        self.assertEqual(classroom.name, "Room 101")
        self.assertEqual(classroom.capacity, 35)
        self.assertEqual(classroom.institution, self.institution)
        self.assertEqual(str(classroom), "Room 101")

class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")
        self.student = Student.objects.create(first_name="David", last_name="Williams", date_of_birth="2006-03-10", email="david@example.com", institution=self.institution)
        self.course = Course.objects.create(name="Science", institution=self.institution)

    def test_create_enrollment(self):
        enrollment = Enrollment.objects.create(student=self.student, course=self.course)
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)
        self.assertIsNotNone(enrollment.enrollment_date)
        self.assertEqual(str(enrollment), f"{self.student} enrolled in {self.course}")

    def test_unique_enrollment(self):
        Enrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(Exception): # Django's IntegrityError for unique constraints
            Enrollment.objects.create(student=self.student, course=self.course)