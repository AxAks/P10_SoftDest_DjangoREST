from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectsAPIView(ListAPIView):
    """
    The main endpoint for Projects
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        """
        enables an authenticated user to list all the projects he is part of.
        """
        user = request.user
        projects = Project.objects.filter(author=user.id)
        serializer = self.serializer_class(projects, many=True)
        return Response({'projects': serializer.data}) if serializer.data else Response("No projects to display")

    def post(self, request):
        """
        enables an authenticated user to create a new project
        """
        project = request.data
        serializer = self.serializer_class(data=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificProjectAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        """
        Returns a specific project by ID
        """
        project_id = kwargs['id']
        project = self.find_project(project_id)
        serializer = self.serializer_class(project)
        return Response(serializer.data) if serializer.data else Response("No project to display")

    def put(self, request, *args, **kwargs):
        """
        Enables the user to update the information of a specific project
        """
        project_id = kwargs['id']
        project = self.find_project(project_id)

        project.title = request.data['title'] if 'title' in request.data.keys() else project.title
        project.description = request.data['description'] \
            if 'description' in request.data.keys() else project.description
        project.type = request.data['type']if 'type' in request.data.keys() else project.type

        project.save()

        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Enables the user to delete a given project and all related issues
        """
        project_id = kwargs['id']
        project = self.find_project(project_id)

        project.delete()
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def find_project(project_id) -> Project:
        return Project.objects.get(pk=project_id)
