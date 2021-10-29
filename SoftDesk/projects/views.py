import json
from django.contrib.auth import get_user_model
from django.core import serializers
from django.shortcuts import render


# Create your views here.
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectsAPIView(ListAPIView):
    """
    The main endpoint for Projects
    """
    permission_classes = (AllowAny,) #  changer pour IsAuthenticated

    def get(self, request, *args, **kwargs):
        """
        enables an authenticated user to list all existing projets
        """
        projects = [project for project in Project.objects.all()]
        serializer = ProjectSerializer(projects, many=True)
        return Response({'projects': serializer.data}) if serializer.data else Response("No projects to display")


    def post(self, request):
        """
        enables an authenticated user to create a new project
        """
        project = request.data
        serializer = ProjectSerializer(data=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
