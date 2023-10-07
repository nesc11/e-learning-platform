from django.urls import path
from students import views


app_name = 'students'

urlpatterns = [
    path('register/', views.register_student, name='student-register'),
    path('enroll-course/', views.enroll_to_course, name='course-enroll'),
    path('courses/<slug:course_slug>', views.get_course, name='course-detail')
]