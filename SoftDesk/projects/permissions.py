"""
draft


AllowAny:
- Users Signup
- Users Create

IsAuthenticated:
- Project : post/create
- Issue
- Comment

Is(Project)Creator/Manager:
- Contributor : post/ create (add)


Is(Project)Contributor:
- Project : list/get
- Contributors : List/ get
- Issue : list / get, post/ create (add)
- Comment : list /get, post/create (add)

IsAuthor:
- Issue : put/update, delete
- Comment put/update, delete
"""

from rest_framework import permissions

from projects.models import Contributor, Issue, Comment


class IsProjectCreator(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
    }

    def has_permission(self, request, view,):
        current_user = request.user
        project_id = view.kwargs['id_project']
        return Contributor.objects.filter(project=project_id, user=current_user.id, role='Creator').exists()


class IsProjectManager(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_projects'],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
    }

    def has_permission(self, request, view,):
        current_user = request.user
        project_id = view.kwargs['project']
        return Contributor.objects.filter(project=project_id, user=current_user.id, role='Manager').exists()


class IsProjectContributor(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_projects'],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
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
        'POST': ['projects.add_comments'],
        'PUT': ['projects.change_comments'],
        'PATCH': ['projects.change_comments'],
        'DELETE': ['projects.delete_comments'],
    }

    def has_permission(self, request, view,):
        pass
        current_user = request.user
        comment_id = view.kwargs['id_comment']
        return Comment.objects.filter(comment=comment_id, author=current_user.id).exists()
