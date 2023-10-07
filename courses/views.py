from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelform_factory
from django.http import JsonResponse
from django.db.models import Count
from courses.models import Course, Content, Module, Image, Video, Text, File, Subject
from courses.forms import CourseForm, ModuleFormSet
from students.forms import CourseEnrollForm
import json


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
def manage_courses(request):
    courses = Course.objects.filter(owner=request.user)
    return render(request, 'courses/manage/course_list.html', {
        'courses': courses
    })

@login_required
@permission_required('courses.change_course', raise_exception=True)
def update_module(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    formset = ModuleFormSet(instance=course)
    if request.method == 'POST':
        formset = ModuleFormSet(data=request.POST, instance=course)
        if formset.is_valid():
            formset.save()
            return redirect('courses:course-list')
    return render(request, 'courses/manage/module/formset.html', {
        'formset': formset,
        'course': course
    })


# def create_content(request, module_id, content_type_name):
    # module = get_object_or_404(Module, pk=module_id, course__owner=request.user)
    # content_type_model = content_type_dict.get(content_type_name)
    # if content_type_model is None:
    #     HttpResponse('Error')

    # ContentTypeForm = modelform_factory(model=content_type_model,
    #                                     exclude=['owner', 'created', 'updated'])
    
    # if request.method == 'POST':
    #     form = ContentTypeForm(data=request.POST, files=request.FILES)
    #     if form.is_valid():
    #         content = form.save(commit=False)
    #         content.owner = request.user
    #         content.save()
    #         Content.objects.create(module=module, item=content)
    #         return redirect('courses:course-list')
    # return render(request, 'courses/manage/content/form.html', {
    #     'form': ContentTypeForm,
    #     'module': module
    # })


def create_update_content(request, module_id, item_name, item_id=None):
    module = get_object_or_404(Module, pk=module_id, course__owner=request.user)
    item_model = get_model_by_parameter(item_dict, item_name)
    if item_model is None:
        pass
    item = None
    if item_id is not None:
        item = get_object_or_404(item_model, pk=item_id, owner=request.user)

    ItemForm = modelform_factory(model=item_model, fields=['title', 'content'])
    form = ItemForm(instance=item)
    # if item_id is not None:
    #     form = ItemForm(instance=item)
    if request.method == 'POST':
        form = ItemForm(data=request.POST, files=request.FILES, instance=item)
        if form.is_valid():
            if item_id is None:
                item = form.save(commit=False)
                item.owner = request.user
                form.save()
                Content.objects.create(module=module, item=item)
            else:
                form.save()
            return redirect('courses:module-content-list', module.id)
    return render(request, 'courses/manage/content/form.html', {
        'form': form,
        'content': item
    })
    

@require_POST
def delete_content(request, content_id):
    content = get_object_or_404(Content, pk=content_id, module__course__owner=request.user)
    module = content.module
    content.item.delete()
    content.delete()
    return redirect('module-content-list', module.id)


def list_contents(request, module_id):
    module = get_object_or_404(Module, pk=module_id, course__owner=request.user)
    return render(request, 'courses/manage/content/list.html', {
        'module': module
    })


@csrf_exempt
def order_modules(request):
    data = json.loads(request.body)
    return JsonResponse({
        'message': 'Modules reordered'
    })

def get_model_by_parameter(model_dict, parameter):
    return model_dict.get(parameter)

item_dict = {
        'text': Text,
        'video': Video,
        'image': Image,
        'file': File
    }


# Catalog of courses
def list_courses(request, subject_slug=None):
    subject = None
    subjects = Subject.objects.annotate(num_courses=Count('courses'))
    courses = Course.objects.annotate(num_modules=Count('modules'))
    if subject_slug is not None:
        subject = get_object_or_404(Subject, slug=subject_slug)
        courses = Course.objects.filter(subject=subject)
    return render(request, 'courses/course/list.html', {
        'subjects': subjects,
        'subject': subject,
        'courses': courses
    })

def get_course(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    return render(request, 'courses/course/detail.html', {
        'course': course,
        'form': CourseEnrollForm(initial={'course': course})
    })