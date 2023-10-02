from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
    # Courses
    path('my_courses/', views.list_courses, name='course-list'),
    path('create/', views.create_course, name='course-create'),
    path('<pk>/edit/', views.update_course, name='course-update'),
    path('<pk>/delete/', views.delete_course, name='course-delete'),

    # Modules
    path('<pk>/modules/',views.update_module, name='module-update')
]