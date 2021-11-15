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


class IsProjectCreator(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['projects.list_projects'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_projects'],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
    }


class IsProjectManager(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['projects.list_projects'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_projects'],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
    }


class IsProjectContributor(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['projects.list_projects'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_projects'],
        'PUT': ['projects.change_projects'],
        'PATCH': ['projects.change_projects'],
        'DELETE': ['projects.delete_projects'],
    }


class IsIssueAuthor(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['projects.add_issues'],
        'PUT': ['projects.change_issues'],
        'PATCH': ['projects.change_issues'],
        'DELETE': ['projects.delete_issues'],
    }


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




class BaseModelPerm(permissions.DjangoModelPermissions):

    def get_custom_perms(self, method, view):
        app_name = view.model._meta.app_label
        return [app_name + "." + perms for perms in view.extra_perms_map.get(method, [])]


def has_permission(self, request, view):
    perms = self.get_required_permissions(request.method, view.model)
    perms.extend(self.get_custom_perms(request.method, view))
    return (
            request.user and
            (request.user.is_authenticated() or not self.authenticated_users_only) and
            request.user.has_perms(perms)
    )

