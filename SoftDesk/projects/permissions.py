"""
This File sets Customs Authorization and Access Permissions to Models
"""
from rest_framework import permissions
from projects.models import Contributor, Issue, Comment


class IsProjectCreator(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_contributor'],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
    }

    def has_permission(self, request, view,):
        current_user = request.user
        project_id = view.kwargs['id_project']
        return Contributor.objects.filter(project=project_id, user=current_user.id, role='Creator').exists()

    def has_object_permission(self, request, view, obj):
        pass  # à ecrire


class IsProjectManager(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_contributor'],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
    }

    def has_permission(self, request, view,):
        current_user = request.user
        project_id = view.kwargs['id_project']
        return Contributor.objects.filter(project=project_id, user=current_user.id, role='Manager').exists()

    def has_object_permission(self, request, view, obj):
        pass  # à ecrire


class IsProjectContributor(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['projects.list_issues', 'projects.list_comments',
                'projects.retrieve_issues', 'projects.retrieve_comments'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_issues', 'projects.add_comments'],
        'PUT': [],
        'PATCH': [],
        'DELETE': [],
    }

    def has_permission(self, request, view,):
        current_user = request.user
        project_id = view.kwargs['id_project']
        return Contributor.objects.filter(project=project_id, user=current_user.id).exists()


class IsIssueAuthor(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': ['projects.change_issues'],
        'PATCH': ['projects.change_issues'],
        'DELETE': ['projects.delete_issues'],
    }

    def has_permission(self, request, view,):
        current_user = request.user
        issue_id = view.kwargs['id_issue']
        return Issue.objects.filter(id=issue_id, author=current_user.id).exists()


class IsCommentAuthor(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': ['projects.change_comments'],
        'PATCH': ['projects.change_comments'],
        'DELETE': ['projects.delete_comments'],
    }

    def has_permission(self, request, view,):
        pass
        current_user = request.user
        comment_id = view.kwargs['id_comment']
        return Comment.objects.filter(comment=comment_id, author=current_user.id).exists()
