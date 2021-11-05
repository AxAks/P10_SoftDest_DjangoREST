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
        return f'"{self.title} ({self.type})" by {self.author}'

    objects = models.Manager()


class Contributor(models.Model):
    """
    Model through linking users to projects
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=128)  # choix à remplir
    role = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.user}: {self.role} for {self.project}'

    objects = models.Manager()


class Issue(models.Model):
    """
    Model for the project-related issues
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=20)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='issue_author',
                               on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='issue_assignee',
                                 on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class Comment(models.Model):
    """
    Model for the project-related comments
    """
    description = models.CharField(max_length=1024)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
