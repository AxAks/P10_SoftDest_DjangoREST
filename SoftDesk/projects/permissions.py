"""
This File sets Customs Authorization and Access Permissions to Models
"""
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from projects.libs import lib_permissions


class ProjectPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in [SAFE_METHODS, 'POST']:
            return True
        else:
            return lib_permissions.is_project_admin(request, view)


class ContributorPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return lib_permissions.is_project_contributor(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return lib_permissions.is_project_admin(request, view)


class IssuePermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return lib_permissions.is_project_contributor(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in [SAFE_METHODS, 'POST']:
            return True
        else:
            return lib_permissions.is_issue_author(request, view)


class CommentPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        return lib_permissions.is_project_contributor(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in [SAFE_METHODS, 'POST']:
            return True
        else:
            return lib_permissions.is_comment_author(request, view)

