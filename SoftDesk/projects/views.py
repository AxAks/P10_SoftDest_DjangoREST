from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectsAPIView(ListAPIView):
    """
    The main endpoint for Projects
    """
    permission_classes = (AllowAny,) #  changer pour IsAuthenticated
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        """
        enables an authenticated user to list all the projects he is part of.
        """
        user = request.user
        projects = Project.objects.filter(author=user.id)  # il faut seulement les projects dont l'uitlisateur fait partie !!
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
    permission_classes = (AllowAny,)  #   changer pour IsAuthenticated
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

        project.title = request.data['title'] if request.data['title'] else None
        project.description = request.data['description'] if request.data['description'] else None
        project.type = request.data['type'] if request.data['type'] else None

        project.save()

        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

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
    def find_project(project_id):
        return Project.objects.get(pk=project_id)
