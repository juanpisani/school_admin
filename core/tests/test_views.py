# core/tests/test_views.py
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Institution, Teacher, Student, Course, Classroom, Enrollment, Schedule
from ..serializers import (
    CourseSerializer,
    ClassroomSerializer,
    EnrollmentSerializer,
)

class CourseViewTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")
        self.teacher1 = Teacher.objects.create(first_name="Bob", last_name="Johnson", email="bob@example.com", institution=self.institution)
        self.teacher2 = Teacher.objects.create(first_name="Margaret", last_name="Johnson", email="marg@example.com", institution=self.institution)
        self.course1 = Course.objects.create(name="Mathematics", institution=self.institution, primary_teacher=self.teacher1)
        self.list_url = reverse('course-list')
        self.detail_url = reverse('course-detail', args=[self.course1.pk])
        self.valid_data = {'name': 'Chemistry', 'institution_id': self.institution.pk, 'primary_teacher_id': self.teacher1.pk}
        self.updated_data = {'name': 'Biology', 'description': 'The study of life', 'institution_id': self.institution.pk, 'primary_teacher_id': self.teacher2.pk}
        self.invalid_data = {'name': 123, 'institution_id': 999, 'primary_teacher_id': 999}

    def test_get_course_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CourseSerializer([self.course1], many=True).data
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_course_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CourseSerializer(self.course1).data
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_non_existent_course_detail(self):
        non_existent_url = reverse('course-detail', args=[999])
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_course(self):
        response = self.client.post(self.list_url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertTrue(Course.objects.filter(name='Chemistry').exists())

    def test_create_course_with_invalid_data(self):
        response = self.client.post(self.list_url, data=json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 1)

    def test_update_course(self):
        response = self.client.put(self.detail_url, data=json.dumps(self.updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course1.refresh_from_db()
        self.assertEqual(self.course1.name, 'Biology')
        self.assertEqual(self.course1.description, 'The study of life')
        self.assertEqual(self.course1.primary_teacher, self.teacher2)

    def test_update_non_existent_course(self):
        non_existent_url = reverse('course-detail', args=[999])
        response = self.client.put(non_existent_url, data=json.dumps(self.updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_course_with_invalid_data(self):
        response = self.client.put(self.detail_url, data=json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.course1.refresh_from_db()
        self.assertEqual(self.course1.name, 'Mathematics') # Should not update

    def test_delete_course(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_delete_non_existent_course(self):
        non_existent_url = reverse('course-detail', args=[999])
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ClassroomViewTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")
        self.classroom1 = Classroom.objects.create(name="Room 101", capacity=30, institution=self.institution)
        self.list_url = reverse('classroom-list')
        self.detail_url = reverse('classroom-detail', args=[self.classroom1.pk])
        self.valid_data = {'name': 'Room 102', 'capacity': 25, 'institution_id': self.institution.pk}
        self.updated_data = {'name': 'Lecture Hall A', 'capacity': 100, 'institution_id': self.institution.pk}
        self.invalid_data = {'name': None, 'capacity': 'invalid', 'institution_id': 999}

    def test_get_classroom_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ClassroomSerializer([self.classroom1], many=True).data
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_classroom_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ClassroomSerializer(self.classroom1).data
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_non_existent_classroom_detail(self):
        non_existent_url = reverse('classroom-detail', args=[999])
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_classroom(self):
        response = self.client.post(self.list_url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 2)
        self.assertTrue(Classroom.objects.filter(name='Room 102').exists())

    def test_create_classroom_with_invalid_data(self):
        response = self.client.post(self.list_url, data=json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Classroom.objects.count(), 1)

    def test_update_classroom(self):
        response = self.client.put(self.detail_url, data=json.dumps(self.updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.classroom1.refresh_from_db()
        self.assertEqual(self.classroom1.name, 'Lecture Hall A')
        self.assertEqual(self.classroom1.capacity, 100)

    def test_update_non_existent_classroom(self):
        non_existent_url = reverse('classroom-detail', args=[999])
        response = self.client.put(non_existent_url, data=json.dumps(self.updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_classroom_with_invalid_data(self):
        response = self.client.put(self.detail_url, data=json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.classroom1.refresh_from_db()
        self.assertEqual(self.classroom1.name, 'Room 101') # Should not update
        self.assertEqual(self.classroom1.capacity, 30)

    def test_delete_classroom(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Classroom.objects.count(), 0)

    def test_delete_non_existent_classroom(self):
        non_existent_url = reverse('classroom-detail', args=[999])
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class EnrollmentViewTest(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name="Test School", address="123 Main St")
        self.student1 = Student.objects.create(first_name="Grace", last_name="Wilson", date_of_birth="2007-01-20", email="grace@example.com", institution=self.institution)
        self.course1 = Course.objects.create(name="Mathematics", institution=self.institution)
        self.enrollment1 = Enrollment.objects.create(student=self.student1, course=self.course1)
        self.list_url = reverse('enrollment-list')
        self.detail_url = reverse('enrollment-detail', args=[self.enrollment1.pk])
        self.valid_data = {'student_id': self.student1.pk, 'course_id': self.course1.pk}
        self.invalid_data = {'student_id': 999, 'course_id': 'invalid'}

    def test_get_enrollment_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = EnrollmentSerializer([self.enrollment1], many=True).data
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_enrollment_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = EnrollmentSerializer(self.enrollment1).data
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_non_existent_enrollment_detail(self):
        non_existent_url = reverse('enrollment-detail', args=[999])
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_enrollment(self):
        student2 = Student.objects.create(first_name="Henry", last_name="Moore", date_of_birth="2006-11-05", email="henry@example.com", institution=self.institution)
        course2 = Course.objects.create(name="Physics", institution=self.institution)
        valid_data_new = {'student_id': student2.pk, 'course_id': course2.pk}
        response = self.client.post(self.list_url, data=json.dumps(valid_data_new), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 2)
        self.assertTrue(Enrollment.objects.filter(student=student2, course=course2).exists())

    def test_create_enrollment_with_invalid_data(self):
        response = self.client.post(self.list_url, data=json.dumps(self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_delete_enrollment(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enrollment.objects.count(), 0)

    def test_delete_non_existent_enrollment(self):
        non_existent_url = reverse('enrollment-detail', args=[999])
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_duplicate_enrollment(self):
        response = self.client.post(self.list_url, data=json.dumps(self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertIn('non_field_errors', json.loads(response.content))


class ScheduleViewSetTestCase(TestCase):
    def setUp(self):
        # Create an institution
        self.institution = Institution.objects.create(name="Test Institution", address="123 Test St")

        # Create a teacher
        self.teacher = Teacher.objects.create(
            first_name="Test",
            last_name="Teacher",
            email="test@example.com",
            institution=self.institution,
        )

        # Create a course
        self.course = Course.objects.create(
            name="Test Course", institution=self.institution, primary_teacher=self.teacher
        )

        # Create a classroom
        self.classroom = Classroom.objects.create(name="Test Classroom", capacity=20, institution=self.institution)

        # Create a schedule
        self.schedule = Schedule.objects.create(
            course=self.course,
            day_of_week=0,
            start_time="09:00:00",
            end_time="10:30:00",
            classroom=self.classroom
        )

        self.schedule_data = {
            "course_id": self.course.pk,
            "day_of_week": 1,  # Tuesday
            "start_time": "09:00:00",
            "end_time": "10:30:00",
            "classroom_id": self.classroom.pk,
        }
        self.schedule_url = reverse("schedule-list")


    def test_create_schedule(self):
        """
        Test case: Create a new schedule.
        """
        response = self.client.post(
            self.schedule_url, data=json.dumps(self.schedule_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.count(), 2)
        new_schedule = Schedule.objects.latest('id')  # Get the last created schedule
        self.assertEqual(new_schedule.course.id, self.course.id)
        self.assertEqual(new_schedule.day_of_week, 1)
        self.assertEqual(str(new_schedule.start_time), "09:00:00")
        self.assertEqual(str(new_schedule.end_time), "10:30:00")
        self.assertEqual(new_schedule.classroom, self.classroom)

    def test_get_all_schedules(self):
        """
        Test case: Get all schedules.
        """
        response = self.client.get(self.schedule_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        schedule_data = response.data[0]
        self.assertEqual(schedule_data["course"]['id'], self.course.pk)
        self.assertEqual(schedule_data["day_of_week"], 0)
        self.assertEqual(schedule_data["start_time"], "09:00:00")
        self.assertEqual(schedule_data["end_time"], "10:30:00")
        self.assertEqual(schedule_data["classroom"]['id'], self.classroom.pk)

    def test_get_schedule_by_id(self):
        """
        Test case: Get a single schedule by its ID.
        """
        url = reverse("schedule-detail", args=[self.schedule.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedule_data = response.data
        self.assertEqual(schedule_data["course"]['id'], self.course.pk)
        self.assertEqual(schedule_data["day_of_week"], 0)
        self.assertEqual(schedule_data["start_time"], "09:00:00")
        self.assertEqual(schedule_data["end_time"], "10:30:00")
        self.assertEqual(schedule_data["classroom"]['id'], self.classroom.pk)

    def test_update_schedule(self):
        """
        Test case: Update an existing schedule.
        """
        url = reverse("schedule-detail", args=[self.schedule.pk])
        updated_data = {
            "course_id": self.course.pk,  # Keep the same course
            "day_of_week": 1,  # Change to Tuesday
            "start_time": "10:00:00",
            "end_time": "11:30:00",
            "classroom_id": self.classroom.pk, #keep same classroom
        }
        response = self.client.put(url, data=json.dumps(updated_data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.schedule.refresh_from_db()  # Refresh the schedule object from the database
        self.assertEqual(self.schedule.day_of_week, 1)
        self.assertEqual(str(self.schedule.start_time), "10:00:00")
        self.assertEqual(str(self.schedule.end_time), "11:30:00")

    def test_delete_schedule(self):
        """
        Test case: Delete a schedule.
        """
        url = reverse("schedule-detail", args=[self.schedule.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.count(), 0)