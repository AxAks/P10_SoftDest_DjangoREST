"""
Functions lib for the permissions of project app
"""
from constants import PROJECT_ADMIN
from projects.models import Contributor, Issue, Comment


def is_project_admin(request, view) -> bool:
    project_id = view.kwargs['id_project']
    return Contributor.objects.filter(project=project_id, user=request.user.id,
                                      role__in=PROJECT_ADMIN).exists()


def is_project_contributor(request, view) -> bool:
    project_id = view.kwargs['id_project']
    return Contributor.objects.filter(project=project_id, user=request.user.id).exists()


def is_issue_author(request, view) -> bool:
    issue_id = view.kwargs['id_issue']
    return Issue.objects.filter(id=issue_id, author=request.user.id).exists()


def is_comment_author(request, view) -> bool:
    comment_id = view.kwargs['id_comment']
    return Comment.objects.filter(id=comment_id, author=request.user.id).exists()
