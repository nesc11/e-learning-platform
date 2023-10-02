from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from courses.models import Course
from courses.forms import CourseForm

# Create your views here.
@login_required
@permission_required('courses.add_course', raise_exception=True)
def create_course(request):
    course_form = CourseForm()
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.owner = request.user
            new_course.save()
            return redirect('courses:course-list')
    return render(request, 'courses/manage/course_form.html', {
        'course_form': course_form
    })


@login_required
@permission_required('courses.change_course', raise_exception=True)
def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    course_form = CourseForm(instance=course)
    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=course)
        if course_form.is_valid():
            course_form.save()
            return redirect('courses:course-list')
    return render(request, 'courses/manage/course_form.html', {
        'course': course,
        'course_form': course_form
    })


@login_required
@permission_required('courses.delete_course', raise_exception=True)
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:course-list')
    return render(request, 'courses/manage/course_delete.html', {
        'course': course
    })


@login_required
@permission_required('courses.view_course', raise_exception=True)
def list_courses(request):
    courses = Course.objects.filter(owner=request.user)
    return render(request, 'courses/manage/course_list.html', {
        'courses': courses
    })
