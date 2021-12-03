import logging

from rest_framework import serializers

from projects.libs import lib_projects
from projects.models import Project, Issue, Comment, Contributor

logger = logging.getLogger('projects_app')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']

    def save(self, author) -> Project:
        project = Project(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            type=self.validated_data['type'],
            author=author
        )
        if lib_projects.already_existing_project(project):
            raise serializers.ValidationError({'already_existing_project': 'Exact same project already exists'})

        project.save()
        return project


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']
        read_only_fields = ['project']

    def save(self, project) -> Contributor:
        contributor = Contributor(
            user=self.validated_data['user'],
            project=project,
            role=self.validated_data['role'],
        )

        errors = {}
        has_manager = lib_projects.has_manager(contributor.project)
        already_has_role = lib_projects.already_has_role(contributor)
        already_registered_contributors = lib_projects.already_registered_contributors(contributor)

        if contributor.role == 'Creator':
            errors['creator'] = 'Project creator cannot be added manually'
        if has_manager and contributor.role == 'Manager':
            errors['has_manager'] = 'Project already has a registered Manager'
        if already_has_role:
            errors['already_has_role'] = 'User already has another role in the project'
        if already_registered_contributors:
            errors['already_contributor'] = 'User already registered as contributor'

        if errors:
            raise serializers.ValidationError({'errors': errors})

        contributor.save()
        return contributor


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project', 'status', 'author', 'assignee']
        read_only_fields = ['project', 'author']

    def save(self, user, project) -> Issue:
        issue = Issue(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            tag=self.validated_data['tag'],
            priority=self.validated_data['priority'],
            status=self.validated_data['status'],
            assignee=self.validated_data['assignee'],
            author=user,
            project=project,
        )

        #  mettre des verifs ici si besoin

        issue.save()
        return issue


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue']
        read_only_fields = ['issue', 'author']

    def save(self, user, issue) -> Comment:
        comment = Comment(
            description=self.validated_data['description'],
            author=user,
            issue=issue,
        )

        #  mettre des verifs ici si besoin

        comment.save()
        return comment
