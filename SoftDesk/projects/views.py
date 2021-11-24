from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_list_or_404

from projects.models import Project, Contributor, Issue, Comment
from projects.libs import lib_projects
from projects.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

from projects.permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions


class ProjectModelViewSet(ModelViewSet):
    """
    Endpoint for Projects
    """
    permission_classes = (ProjectPermissions,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.order_by('-created_time')

    def list(self, request, *args, **kwargs):
        """
        enables an authenticated user to list all the projects he is part of.
        """
        user = request.user
        projects = get_list_or_404(self.queryset.filter(contributor__user=user.id))

        serializer = self.serializer_class(projects, many=True)
        return Response({'projects': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        enables an authenticated user to create a new project
        """
        project = request.data
        user = request.user
        project_copy = project.copy()
        project_copy['author'] = user.id
        serializer = self.serializer_class(data=project_copy)
        serializer.is_valid(raise_exception=True)
        project_obj = serializer.save(author=user)
        project_creator = Contributor(user=user, project=project_obj, role='Creator')
        project_creator.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific project by ID
        """
        project_id = kwargs['id_project']
        project = get_object_or_404(self.queryset.filter(contributor__user=request.user.id, id=project_id))
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        """
        # Enables the user to update the information of a specific project
        """
        project_id = kwargs['id_project']
        project = lib_projects.find_obj_by_id(Project, project_id)
        self.check_object_permissions(request, project)
        project.title = request.data['title'] if 'title' in request.data.keys() else project.title
        project.description = request.data['description'] \
            if 'description' in request.data.keys() else project.description
        project.type = request.data['type'] if 'type' in request.data.keys() else project.type

        project.save()
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        Enables the user to delete a given project and all related issues
        """
        project_id = kwargs['id_project']
        project = lib_projects.find_obj_by_id(Project, project_id)
        self.check_object_permissions(request, project)
        project.delete()
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ContributorModelViewSet(ModelViewSet):
    """
    End point for contributors
    """
    permission_classes = (ContributorPermissions,)
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all().order_by('-project', 'user')

    def list(self, request, **kwargs):
        """
        List all contributors of a given project
        """
        project_id = kwargs['id_project']
        lib_projects.find_obj_by_id(Project, project_id)
        contributors = get_list_or_404(self.queryset.filter(project_id=project_id))
        serializer = self.serializer_class(contributors, many=True)
        return Response({'contributors': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """
        Add a contributor to a given project
        """
        project_id = kwargs['id_project']
        project = lib_projects.find_obj_by_id(Project, project_id)

        self.check_object_permissions(request, project)
        contributor = request.data
        contributor_copy = contributor.copy()
        contributor_copy['project'] = project
        serializer = self.serializer_class(data=contributor_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific contributor to a project by the user's ID
        """
        contributor = lib_projects.find_contributor(self.queryset, kwargs)
        serializer = self.serializer_class(contributor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        """
        Updates a specific contributor (Role
        """
        contributor = lib_projects.find_contributor(self.queryset, kwargs)
        self.check_object_permissions(request, contributor)
        contributor.role = request.data['role'] if 'role' in request.data.keys() else contributor.role
        contributor.save()
        """
        contrib_as_dict = model_to_dict(contributor) # marche pas car le user est deja dans le projet en tant que contrib
        serializer = self.serializer_class(data=contrib_as_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save(contributor.project)
        """
        return Response(contributor.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        remove users from a given project
        """
        contributor = lib_projects.find_contributor(self.queryset, kwargs)
        self.check_object_permissions(request, contributor)
        contributor.delete()
        serializer = self.serializer_class(contributor)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class IssueModelViewSet(ModelViewSet):
    """
    End point for issues
    """
    permission_classes = (IssuePermissions,)
    serializer_class = IssueSerializer
    queryset = Issue.objects.all().order_by('-created_time')

    def list(self, request, **kwargs):
        """
        Lists all issue of a given project
        """
        issues = get_list_or_404(self.queryset.filter(project=kwargs['id_project']))
        serializer = self.serializer_class(issues, many=True)
        return Response({'issues': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """
        Adds an issue to a given project
        """
        project_id = kwargs['id_project']
        project = lib_projects.find_obj_by_id(Project, project_id)
        user = request.user
        issue = request.data
        issue_copy = issue.copy()
        issue_copy['author'], issue_copy['project'] = user, project
        serializer = self.serializer_class(data=issue_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save(user, project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific issue by ID
        """
        issue = lib_projects.find_issue(self.queryset, kwargs)
        serializer = self.serializer_class(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        """
        Updates a specific issue
        """
        issue = lib_projects.find_issue(self.queryset, kwargs)
        self.check_object_permissions(request, issue)
        issue.title = request.data['title'] if 'title' in request.data.keys() else issue.title
        issue.description = request.data['description'] \
            if 'description' in request.data.keys() else issue.description
        issue.tag = request.data['tag'] if 'tag' in request.data.keys() else issue.tag
        issue.priority = request.data['priority'] if 'priority' in request.data.keys() else issue.priority
        issue.status = request.data['status'] if 'status' in request.data.keys() else issue.status
        issue.assignee = request.data['assignee'] if 'assignee' in request.data.keys() else issue.assignee

        issue.save()
        serializer = self.serializer_class(issue)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        Remove a contributor from a Project
        """
        issue = lib_projects.find_issue(self.queryset, kwargs)
        self.check_object_permissions(request, issue)
        issue.delete()
        serializer = self.serializer_class(issue)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CommentModelViewSet(ModelViewSet):
    """
    End point for comments
    """
    permission_classes = (CommentPermissions,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-created_time')

    def list(self, request, **kwargs):
        """
        Lists all comments on a project related issue
        """
        issue = lib_projects.find_issue(IssueModelViewSet.queryset, kwargs)
        comments = get_list_or_404(self.queryset.filter(issue=issue))
        serializer = self.serializer_class(comments, many=True)
        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """
        Add a comment to a project-related issue
        """
        user= request.user
        issue = lib_projects.find_issue(IssueModelViewSet.queryset, kwargs)
        comment = request.data
        comment_copy = comment.copy()
        comment_copy['author'], comment_copy['issue'] = user.id, issue.id
        serializer = self.serializer_class(data=comment_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save(user, issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific Comment on a issue by ID
        """
        comment = lib_projects.find_comment(self.queryset, kwargs)
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        """
        Updates a specific Comment on a issue by ID
        """
        comment = lib_projects.find_comment(self.queryset, kwargs)
        self.check_object_permissions(request, comment)
        comment.description = request.data['description'] \
            if 'description' in request.data.keys() else comment.description

        comment.save()
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        Deletes a specific Comment on a issue by ID
        """
        comment = lib_projects.find_comment(self.queryset, kwargs)
        self.check_object_permissions(request, comment)
        comment.delete()
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
