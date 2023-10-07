from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from courses.api import views

app_name = 'courses_api'

urlpatterns = [
    path('subjects/', views.SubjectList.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetail.as_view(), name='subject-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)