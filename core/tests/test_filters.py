# core/tests/test_filters.py
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Institution, Teacher, Student, Course, Classroom, Enrollment
from ..serializers import CourseSerializer

class FilterTests(TestCase):
    def setUp(self):
        # Create an institution
        self.institution1 = Institution.objects.create(name="Test University", address="123 Main St")
        self.institution2 = Institution.objects.create(name="Test College", address="456 Oak Ave")

        # Create teachers
        self.teacher1 = Teacher.objects.create(
            first_name="Alice", last_name="Smith", email="alice@example.com", institution=self.institution1
        )
        self.teacher2 = Teacher.objects.create(
            first_name="Bob", last_name="Smith", email="bob@example.com", institution=self.institution2
        )

        # Create students
        self.student1 = Student.objects.create(
            first_name="Bob", last_name="Johnson", date_of_birth="2002-03-15", email="bob@example.com", institution=self.institution1
        )
        self.student2 = Student.objects.create(
            first_name="Alice", last_name="Johnson", date_of_birth="2003-04-20", email="alice2@example.com", institution=self.institution1
        )
        self.student3 = Student.objects.create(
            first_name="Charlie", last_name="Brown", date_of_birth="2004-05-25", email="charlie@example.com", institution=self.institution2
        )

        # Create courses
        self.course1 = Course.objects.create(name="Introduction to Python", institution=self.institution1, primary_teacher=self.teacher1)
        self.course2 = Course.objects.create(name="Advanced Python", institution=self.institution1, primary_teacher=self.teacher2)
        self.course3 = Course.objects.create(name="Data Structures", institution=self.institution2, primary_teacher=self.teacher2)

        # Create classrooms
        self.classroom1 = Classroom.objects.create(name="Room A101", capacity=30, institution=self.institution1)
        self.classroom2 = Classroom.objects.create(name="Room B202", capacity=25, institution=self.institution2)

        #enroll students
        Enrollment.objects.create(student=self.student1, course=self.course1)
        Enrollment.objects.create(student=self.student1, course=self.course2)
        Enrollment.objects.create(student=self.student2, course=self.course1)
        Enrollment.objects.create(student=self.student3, course=self.course3)

    def test_filter_institutions(self):
        """
        Test case: Filter institutions by name and address.
        """
        url = reverse('institution-list')
        response = self.client.get(url, {'name': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)  # Both institutions match

        response = self.client.get(url, {'name': 'University'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test University')

        response = self.client.get(url, {'address': 'Main'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['address'], '123 Main St')

    def test_filter_teachers(self):
        """
        Test case: Filter teachers by first name, last name, email, and institution.
        """
        url = reverse('teacher-list')
        response = self.client.get(url, {'first_name': 'Alice'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['first_name'], 'Alice')

        response = self.client.get(url, {'last_name': 'Smith'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        response = self.client.get(url, {'email': 'alice@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['email'], 'alice@example.com')

        response = self.client.get(url, {'institution': self.institution1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['institution']['id'], self.institution1.pk)

    def test_filter_students(self):
        """
        Test case: Filter students by various fields including date ranges.
        """
        url = reverse('student-list')

        response = self.client.get(url, {'first_name': 'Bob'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['first_name'], 'Bob')

        response = self.client.get(url, {'last_name': 'Johnson'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        response = self.client.get(url, {'email': 'bob@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['email'], 'bob@example.com')

        response = self.client.get(url, {'institution': self.institution1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        response = self.client.get(url, {'date_of_birth': '2002-03-15'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['date_of_birth'], '2002-03-15')

        response = self.client.get(url, {'date_of_birth__gt': '2003-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['first_name'], 'Alice')

        response = self.client.get(url, {'date_of_birth__lt': '2003-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['first_name'], 'Bob')

    def test_filter_courses(self):
        """
        Test case: Filter courses by name and institution.
        """
        url = reverse('course-list')
        response = self.client.get(url, {'name': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        response = self.client.get(url, {'institution': self.institution1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_filter_classrooms(self):
        """
        Test case: Filter classrooms by name and institution.
        """
        url = reverse('classroom-list')
        response = self.client.get(url, {'name': 'Room A101'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Room A101')

        response = self.client.get(url, {'institution': self.institution1.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
