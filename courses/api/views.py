from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from courses.models import Subject, Module
from courses.api.serializers import SubjectSerializer, ModuleSerializer


class SubjectList(generics.ListAPIView):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer    


class SubjectDetail(generics.RetrieveAPIView):
    
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer