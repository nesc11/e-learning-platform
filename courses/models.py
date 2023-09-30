from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
class Course(models.Model):
    owner = models.ForeignKey(to=User,
                              on_delete=models.CASCADE,
                              related_name='courses')
    subject = models.ForeignKey(to=Subject,
                                on_delete=models.CASCADE,
                                related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __atr__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(to=Course,
                               on_delete=models.CASCADE,
                               related_name='modules')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
