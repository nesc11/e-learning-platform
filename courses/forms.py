from django import forms
from django.forms.models import inlineformset_factory
from courses.models import Course, Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['subject', 'title', 'slug', 'overview']

ModuleFormSet = inlineformset_factory(parent_model=Course,
                                      model=Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)