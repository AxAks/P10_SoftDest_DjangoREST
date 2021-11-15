from itertools import chain

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

from projects.lib_projects import find_obj
from users.models import CustomUser


class ProjectsAPIView(ListCreateAPIView):
    """
    The main endpoint for Projects
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    context = {}

    def get(self, request, *args, **kwargs):
        """
        enables an authenticated user to list all the projects he is part of.
        """
        user = request.user
        authored_projects = Project.objects.all().filter(author=user.id)
        contributed_projects = Project.objects.all().filter(contributor__user=user.id) # Project.objects.filter(author=user.id)
        projects = chain(authored_projects, contributed_projects)

        serializer = self.serializer_class(projects, many=True)
        return Response({'projects': serializer.data}) if serializer.data else Response("No projects to display")

    def post(self, request, *args, **kwargs):
        """
        enables an authenticated user to create a new project
        """
        project = request.data
        user = request.user
        project_copy = project.copy()
        project_copy['author'] = user.id
        serializer = self.serializer_class(data=project_copy)
        serializer.is_valid(raise_exception=True)
        project_obj = serializer.save()
        project_creator = Contributor(user=user, project=project_obj, role='Creator') # ne rend pas contributor du projet ...?
        project_creator.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificProjectAPIView(APIView):
    permission_classes = (AllowAny,)  # à changer pour IsAuthenticated
    serializer_class = ProjectSerializer

    def get(self, request, **kwargs):
        """
        Returns a specific project by ID
        """
        user = request.user
        project_id = kwargs['id']
        project = find_obj(Project, project_id)  # pb si pas de correspondance !! à gérer
        if project in Project.objects.all().filter(contributor=user.id):
            serializer = self.serializer_class(project, many=True)
            return Response(serializer.data) if serializer.data else Response("No project to display")
        else:
            return Response('You do not have sufficient permissions,', status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, **kwargs):
        """
        Enables the user to update the information of a specific project
        """
        project_id = kwargs['id']
        project = find_obj(Project, project_id)  # pb si pas de correspondance !! à gérer

        project.title = request.data['title'] if 'title' in request.data.keys() else project.title
        project.description = request.data['description'] \
            if 'description' in request.data.keys() else project.description
        project.type = request.data['type'] if 'type' in request.data.keys() else project.type

        project.save()

        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        """
        Enables the user to delete a given project and all related issues
        """
        project_id = kwargs['id']
        project = find_obj(Project, project_id)  # pb si pas de correspondance !! à gérer

        project.delete()
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ContributorAPIView(APIView):
    """
    Main end point for contributors
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ContributorSerializer

    def get(self, request, **kwargs):
        """
        List all contributors of a given project
        """
        contributors = Contributor.objects.filter(project=kwargs['project'])
        serializer = self.serializer_class(contributors, many=True)
        return Response({'contributors': serializer.data}) if serializer.data \
            else Response("No contributors to display")

    def post(self, request, **kwargs):
        """
        Add a contributor to a given project
        """
        current_user = request.user
        project_id = kwargs['project']
        is_project_contributor = Contributor.objects.filter(project=project_id).get(user=current_user.id)  # erreur si pas de match
        if is_project_contributor and is_project_contributor.role in ('Creator', 'Manager'):
            contributor = request.data
            contributor_copy = contributor.copy()
            contributor_copy['project'] = kwargs['project']
            serializer = self.serializer_class(data=contributor_copy)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Unsufficient permissions. '
                            'You must be the project creator or manager',
                            status=status.HTTP_401_UNAUTHORIZED)


class SpecificContributorAPIView(APIView):
    """
    End point for Specific contributor
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ContributorSerializer

    def get(self, request, **kwargs):
        """
        Returns a specific contributor to a project by ID
        """
        contributor_id = kwargs['id']
        contributor = find_obj(Contributor, contributor_id)  # pb si pas de correspondance !! à gérer
        serializer = self.serializer_class(contributor)
        return Response(serializer.data) if serializer.data else Response("No project to display")

    def delete(self, request, **kwargs):
        """
        remove users from a given project
        """
        contributor_id = kwargs['id']
        contributor = self.find_contributor(contributor_id)  # pb si pas de correspondance !! à gérer

        contributor.delete()
        serializer = self.serializer_class(contributor)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class IssueAPIView(APIView):
    """
    Main end point for issues
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueSerializer

    def get(self, request, **kwargs):
        """
        Lists all issue of a given project
        """
        issues = Contributor.objects.filter(project=kwargs['project'])
        serializer = self.serializer_class(issues, many=True)
        return Response({'contributors': serializer.data}) if serializer.data \
            else Response("No issues to display")

    def post(self, request, **kwargs):
        """
        Adds an issue to a given project
        """
        issue = request.data
        serializer = self.serializer_class(data=issue)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificIssueAPIView(APIView):
    """
    End point for Specific issue
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueSerializer

    def get(self, request, **kwargs):
        """
        Returns a specific issue by ID
        """
        issue_id = kwargs['id']
        issue = find_obj(Issue, issue_id)  # pb si pas de correspondance !! à gérer
        serializer = self.serializer_class(issue)
        return Response(serializer.data) if serializer.data else Response("No issue to display")

    def put(self, request, **kwargs):
        """
        Updates a specific issue
        """
        issue_id = kwargs['id']
        issue = find_obj(Issue, issue_id)   # pb si pas de correspondance !! à gérer

        issue.title = request.data['title'] if 'title' in request.data.keys() else issue.title
        issue.description = request.data['description'] \
            if 'description' in request.data.keys() else issue.description
        issue.tag = request.data['tag'] if 'tag' in request.data.keys() else issue.tag
        issue.priority = request.data['priority'] if 'priority' in request.data.keys() else issue.priority
        issue.project = request.data['project'] if 'project' in request.data.keys() else issue.project
        issue.status = request.data['status'] if 'status' in request.data.keys() else issue.status
        issue.author = request.data['author'] if 'author' in request.data.keys() else issue.author
        issue.assignee = request.data['assignee'] if 'assignee' in request.data.keys() else issue.assignee

        issue.save()

        serializer = self.serializer_class(issue)
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        """
        Remove a contributor from a Project
        """
        issue_id = kwargs['id']
        issue = find_obj(Issue, issue_id)   # pb si pas de correspondance !! à gérer

        issue.delete()
        serializer = self.serializer_class(issue)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CommentAPIView(APIView):
    """
    Main end point for comments
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get(self, request, **kwargs):
        """
        Lists all comments on a project related issue
        """
        comments = Comment.objects.filter(issue=kwargs['issue'])
        serializer = self.serializer_class(comments, many=True)
        return Response({'comments': serializer.data}) if serializer.data \
            else Response("No comments to display")

    def post(self, request, **kwargs):
        """
        Add a comment to a project-related issue
        """
        comment = request.data
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificCommentAPIView(APIView):
    """
    End point for Specific comment
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get(self, request, **kwargs):
        """
        Returns a specific Comment on a issue by ID
        """
        comment_id = kwargs['id']
        comment = find_obj(Comment, comment_id)  # pb si pas de correspondance !! à gérer
        serializer = self.serializer_class(comment)
        return Response(serializer.data) if serializer.data else Response("No comment to display")

    def put(self, request, **kwargs):
        """
        Updates a specific Comment on a issue by ID
        """
        comment_id = kwargs['id']
        comment = find_obj(Comment, comment_id)   # pb si pas de correspondance !! à gérer

        comment.description = request.data['description'] \
            if 'description' in request.data.keys() else comment.description
        comment.author = request.data['author'] if 'author' in request.data.keys() else comment.author
        comment.issue = request.data['issue'] if 'issue' in request.data.keys() else comment.issue

        comment.save()

        serializer = self.serializer_class(comment)
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        """
        Deletes a specific Comment on a issue by ID
        """
        comment_id = kwargs['id']
        comment = find_obj(Comment, comment_id)   # pb si pas de correspondance !! à gérer

        comment.delete()
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
