from rest_framework import serializers

from projects.models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']

    def save(self):
        project = Project(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            type=self.validated_data['type'],
        )
        already_existing_projects = [project for project
                                     in Project.objects.filter(title=project.title, description=project.description,
                                                               type=project.type,)]
        if already_existing_projects:
            raise serializers.ValidationError({'already_existing_project':
                                               'Exact same project already exists'})
        project.save()
        return project


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']
        read_only_fields = ['project']

    def save(self, project):
        contributor = Contributor(
            user=self.validated_data['user'],
            project=project,
            role=self.validated_data['role'],
        )

        errors = {}
        has_manager = Contributor.objects.filter(project=contributor.project,
                                                 role='Manager').exists()
        already_has_role = [contributor for contributor
                            in Contributor.objects.filter(user=contributor.user,
                                                          project=contributor.project)]
        already_registered_contributors = [contributor for contributor
                                           in Contributor.objects.filter(user=contributor.user,
                                                                         project=contributor.project,
                                                                         role=contributor.role)]

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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue']
        read_only_fields = ['issue', 'author']
