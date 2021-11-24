"""
Functions lib for the projects app
"""
from typing import Any

from rest_framework.generics import get_object_or_404

from projects.models import Contributor, Project, Issue, Comment


def already_existing_project(project) -> list[Project]:
    return [project for project in Project.objects.filter(title=project.title,
                                                          description=project.description,
                                                          type=project.type)]


def has_manager(project: Project) -> bool:
    return Contributor.objects.filter(project=project,
                                      role='Manager').exists()


def already_has_role(contributor: Contributor) -> list[Contributor]:
    return [contributor for contributor
            in Contributor.objects.filter(user=contributor.user,
                                          project=contributor.project)]


def already_registered_contributors(contributor: Contributor) -> list[Contributor]:
    return [contributor for contributor in Contributor.objects.filter(user=contributor.user, role=contributor.role)]


def find_obj_by_id(_obj, obj_id) -> Any:
    obj = get_object_or_404(_obj.objects.filter(pk=obj_id))
    return obj


def find_contributor(queryset, kwargs) -> Contributor:
    project_id, contributor_id = kwargs['id_project'], kwargs['id_user']
    contributor = get_object_or_404(queryset.filter(project_id=project_id, user_id=contributor_id))
    return contributor


def find_issue(queryset, kwargs) -> Issue:
    project_id, issue_id = kwargs['id_project'], kwargs['id_issue']
    issue = get_object_or_404(queryset.filter(project=project_id, id=issue_id))
    return issue


def find_comment(queryset, kwargs) -> Comment:
    project_id = kwargs['id_project']
    issue_id, comment_id = kwargs['id_issue'], kwargs['id_comment']
    comment = get_object_or_404(queryset.filter(issue__project=project_id, issue=issue_id, id=comment_id))
    return comment
