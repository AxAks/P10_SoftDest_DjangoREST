from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author_user']
