from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
    # Courses
    path('my_courses/', views.manage_courses, name='course-manage'),
    path('create/', views.create_course, name='course-create'),
    path('<int:pk>/edit/', views.update_course, name='course-update'),
    path('<int:pk>/delete/', views.delete_course, name='course-delete'),

    path('subjects/<slug:subject_slug>/', views.list_courses, name='course-list-by-subject'),
    path('<slug:course_slug>/', views.get_course, name='course-detail'),

    # Modules
    path('<int:pk>/modules/',views.update_module, name='module-update'),
    path('modules/order/', views.order_modules, name='module-order'),

    # Content
    path('module/<int:module_id>/content/<str:item_name>/create/', views.create_update_content, name='content-create'),
    path('module/<int:module_id>/content/<str:item_name>/<int:item_id>/', views.create_update_content, name='content-update'),
    path('module/<int:content_id>/delete/', views.delete_content, name='content-delete'),
    path('module/<int:module_id>/', views.list_contents, name='module-content-list')
]