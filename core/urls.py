# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutionViewSet, TeacherViewSet, StudentViewSet, CourseViewSet, ClassroomViewSet, EnrollmentViewSet, ScheduleViewSet # Import ScheduleViewSet

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'schedules', ScheduleViewSet) # Add this line

urlpatterns = [
    path('', include(router.urls)),
]
