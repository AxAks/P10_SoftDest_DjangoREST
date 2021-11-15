from rest_framework import serializers

from projects.models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author']

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'role']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority', 'project', 'status', 'author', 'assignee']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['description', 'author', 'issue']
