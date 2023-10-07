from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from students.forms import CourseEnrollForm
from courses.models import Course

# Create your views here.


def register_student(request):
    if request.user.is_authenticated:
        return redirect('/')

    register_form = UserCreationForm()
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect(to='/')
            # return redirect('students:course-list')

    return render(request, 'students/accounts/register.html', {
        'form': register_form
    })


@login_required
@require_POST
def enroll_to_course(request, form):
    form = CourseEnrollForm(request.POST)
    if form.is_valid():
        course_id = form.cleaned_data['course']
        course = get_object_or_404(Course, pk=course_id)
        course.students.add(request.user)
        return redirect('students:course-detail', course.slug)
    return HttpResponse('Error')


@login_required
def list_enrolled_courses(request):
    courses = Course.objects.filter(students__in=[request.user])
    return render(request, 'students/course/list.html', {
        'courses': courses
    })


def get_course(request, course_slug):

