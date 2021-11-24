"""
Functions lib for the projects app
"""
from typing import Any

from rest_framework.generics import get_object_or_404


def find_obj_by_id(_obj, obj_id) -> Any:
    obj = get_object_or_404(_obj.objects.filter(pk=obj_id))
    return obj


def find_issue(queryset, kwargs):
    project_id = kwargs['id_project']
    issue_id = kwargs['id_issue']
    issue = get_object_or_404(queryset.queryset.filter(project=project_id, id=issue_id))
    return issue


def find_comment(queryset, kwargs):
    project_id = kwargs['id_project']
    issue_id = kwargs['id_issue']
    comment_id = kwargs['id_comment']
    comment = get_object_or_404(queryset.filter(project=project_id, issue=issue_id, comment=comment_id))
    return comment
