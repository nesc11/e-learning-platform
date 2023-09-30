from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
    
class Content(models.Model):
    module = models.ForeignKey(to=Module,
                               on_delete=models.CASCADE,
                               related_name='contents')
    content_type = models.ForeignKey(to=ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'model__in': (
                                             'text', 'file', 'image', 'video'
                                         )
                                     })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

class ItemBase(models.Model):
    owner = models.ForeignKey(to=User,
                              on_delete=models.CASCADE,
                              related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    content = models.FileField(upload_to='files')

class Image(ItemBase):
    content = models.ImageField(upload_to='images')

class Video(ItemBase):
    content = models.URLField()
