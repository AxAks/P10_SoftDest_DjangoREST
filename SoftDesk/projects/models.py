from django.db import models
from django.contrib.auth.models import Permission
from SoftDesk import settings


class Project(models.Model):
    """
    Model for a project
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.title}" by {self.author}: {self.type}'

    objects = models.Manager()


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.Choices('read', 'write')  # choix à remplir
    role = models.CharField(max_length=128)

    objects = models.Manager()


class Issue(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=20)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='author',
                                    on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='assignee',
                                      on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class Comment(models.Model):
    description = models.CharField(max_length=1024)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
