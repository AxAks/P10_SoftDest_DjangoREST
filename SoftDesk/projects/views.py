import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_list_or_404

from projects.models import Project, Contributor, Issue, Comment
from projects.libs import lib_projects
from projects.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

from projects.permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions

logger = logging.getLogger('projects_app')


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
        logger.info(f"(Success) Projects: User {user.username} requested the list of projects")
        return Response({'Projects': serializer.data}, status=status.HTTP_200_OK)

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
        serialized_project = self.serializer_class(project_obj)
        logger.info(f"(Success) Projects: User {user.username} created the project {project_obj.title}")
        return Response(serialized_project.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific project by ID
        """
        project_id = kwargs['id_project']
        project = get_object_or_404(self.queryset.filter(contributor__user=request.user.id, id=project_id))
        serializer = self.serializer_class(project)
        logger.info(f"(Success) Projects: User {request.user.username} "
                    f"requested project #{project.id}: {project.title}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        """
        # Enables the user to update the information of a specific project
        """
        project_id = kwargs['id_project']
        project = lib_projects.find_obj_by_id(Project, project_id)
        self.check_object_permissions(request, project)
        uneditable_fields = {}
        if 'author' in request.data.keys():
            uneditable_fields['author'] = request.data['author']
        if 'created_time' in request.data.keys():
            uneditable_fields['created_time'] = request.data['created_time']
        serializer = self.serializer_class(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if uneditable_fields:
            return Response(f'{list(uneditable_fields.keys())}: cannot be modified',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            project_obj = serializer.update(project, serializer.validated_data)
            serialized_project = self.serializer_class(project_obj)
            logger.info(f"(Success) Projects: User {project.author.username} updated "
                        f"project #{project.id}: {project_obj.title}")
            return Response(serialized_project.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        Enables the user to delete a given project and all related issues
        """
        project_id = kwargs['id_project']
        project = lib_projects.find_obj_by_id(Project, project_id)
        self.check_object_permissions(request, project)
        project.delete()
        serializer = self.serializer_class(project)
        logger.info(f"(Success) Projects: User {project.author.username} deleted "
                    f"project #{project.id}: {project.title}")
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
        logger.info(f"(Success) Contributors: User {request.user.username} requested the list of contributors for "
                    f"project #{project_id}")
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
        contributor_obj = serializer.save(project)
        serialized_contributor = self.serializer_class(contributor_obj)
        logger.info(f"(Success) Contributors: User {request.user.username} added user {contributor_obj.user.username} "
                    f" to the list of contributors "
                    f"for project #{contributor_obj.project.id}: {contributor_obj.project.title}")
        return Response(serialized_contributor.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific contributor to a project by the user's ID
        """
        contributor = lib_projects.find_contributor(self.queryset, kwargs)
        serializer = self.serializer_class(contributor)
        logger.info(f"(Success) Contributors: User {request.user.username} "
                    f"requested Contributor {contributor.user.username} "
                    f"of project #{contributor.project.id}: {contributor.project.title}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        """
        Updates a specific contributor (Role
        """
        contributor = lib_projects.find_contributor(self.queryset, kwargs)
        self.check_object_permissions(request, contributor)
        uneditable_fields = {}
        if 'project' in request.data.keys():
            uneditable_fields['project'] = request.data['project']
        serializer = self.serializer_class(contributor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if uneditable_fields:
            return Response(f'{list(uneditable_fields.keys())}: cannot be modified',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            contributor_obj = serializer.update(contributor, serializer.validated_data)
            serialized_contributor = self.serializer_class(contributor_obj)
            logger.info(f"(Success) Contributors: User {request.user.username} updated {contributor.user.username}'s "
                        f"role in project #{contributor.project.id}: {contributor.project.title}")
            return Response(serialized_contributor.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        remove users from a given project
        """
        contributor = lib_projects.find_contributor(self.queryset, kwargs)
        self.check_object_permissions(request, contributor)
        if contributor.role == 'Creator':
            return Response("Project Creator cannot be removed from project", status=status.HTTP_400_BAD_REQUEST)
        else:
            contributor.delete()
            serializer = self.serializer_class(contributor)
            logger.info(f"(Success) Contributors: User {request.user.username} "
                        f"removed user {contributor.user.username} from "
                        f"project #{contributor.project.id}: {contributor.project.title}")
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
        project_id = kwargs['id_project']
        issues = get_list_or_404(self.queryset.filter(project_id))
        serializer = self.serializer_class(issues, many=True)
        logger.info(f"(Success) Issues: User {request.user.username} requested the list of issues for "
                    f"project #{project_id}")
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
        issue_obj = serializer.save(user, project)
        serialized_issue = self.serializer_class(issue_obj)
        logger.info(f"(Success) Issues: User {user.username} "
                    f"created the issue #{issue_obj.id}: {issue_obj.title} "
                    f"in project #{issue_obj.project.id}: {issue_obj.project.title}")
        return Response(serialized_issue.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific issue by ID
        """
        issue = lib_projects.find_issue(self.queryset, kwargs)
        serializer = self.serializer_class(issue)
        logger.info(f"(Success) Issues: User {request.user.username} "
                    f"requested issue #{issue.id}: {issue.title} "
                    f"of project #{issue.project.id}: {issue.project.title}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        """
        Updates a specific issue
        """
        issue = lib_projects.find_issue(self.queryset, kwargs)
        self.check_object_permissions(request, issue)
        uneditable_fields = {}
        if 'project' in request.data.keys():
            uneditable_fields['project'] = request.data['project']
        if 'author' in request.data.keys():
            uneditable_fields['author'] = request.data['author']
        serializer = self.serializer_class(issue, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if uneditable_fields:
            return Response(f'{list(uneditable_fields.keys())}: cannot be modified',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            issue_obj = serializer.update(issue, serializer.validated_data)
            serialized_issue = self.serializer_class(issue_obj)
            logger.info(f"(Success) Issues: User {request.user.username} updated issue #{issue.id}: {issue.title} "
                        f" of project #{issue.project.id}: {issue.project.title}")
            return Response(serialized_issue.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        deletes an issue in a Project
        """
        issue = lib_projects.find_issue(self.queryset, kwargs)
        self.check_object_permissions(request, issue)
        issue.delete()
        serializer = self.serializer_class(issue)
        logger.info(f"(Success) Issues: User {request.user.username} "
                    f"deleted issue #{issue.id}: {issue.title} in "
                    f"project #{issue.project.id}: {issue.project.title}")
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
        user = request.user
        issue = lib_projects.find_issue(IssueModelViewSet.queryset, kwargs)
        comment = request.data
        comment_copy = comment.copy()
        comment_copy['author'], comment_copy['issue'] = user.id, issue.id
        serializer = self.serializer_class(data=comment_copy)
        serializer.is_valid(raise_exception=True)
        comment_obj = serializer.save(user, issue)
        serialized_comment = self.serializer_class(comment_obj)
        return Response(serialized_comment.data, status=status.HTTP_201_CREATED)

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
        uneditable_fields = {}
        if 'issue' in request.data.keys():
            uneditable_fields['issue'] = request.data['issue']
        if 'author' in request.data.keys():
            uneditable_fields['author'] = request.data['author']
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if uneditable_fields:
            return Response(f'{list(uneditable_fields.keys())}: cannot be modified',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            comment_obj = serializer.update(comment, serializer.validated_data)
            serialized_comment = self.serializer_class(comment_obj)
            return Response(serialized_comment.data, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, **kwargs):
        """
        Deletes a specific Comment on a issue by ID
        """
        comment = lib_projects.find_comment(self.queryset, kwargs)
        self.check_object_permissions(request, comment)
        comment.delete()
        serializer = self.serializer_class(comment)
        logger.info(f"(Success) Comments: User {request.user.username} "
                    f"deleted comment #{comment.id}: {comment.description} of "
                    f"issue #{comment.issue.id}: {comment.issue.title} "
                    f"(project #{comment.issue.project.id}: {comment.issue.project.title}")
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
