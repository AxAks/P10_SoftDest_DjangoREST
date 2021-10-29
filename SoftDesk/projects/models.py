from django.db import models

from SoftDesk import settings


class Project(models.Model):
    """
    Model for a project
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.title}" by {self.author_user_id}: {self.type}'

    objects = models.Manager()


"""
class Contributor(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.Choices('read', 'write')  # choix à remplir
    role = models.CharField(max_length=128)


class Issue(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=20)
    project_id = models.IntegerField
    status = models.CharField(max_length=20)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='%(class)s_requests_created', 
    on_delete=models.CASCADE)  #CASCADE pas sur !
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='%(class)s_requests_created',
     on_delete=models.CASCADE)  #CASCADE pas sur !
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_id = models.IntegerField
    description = models.CharField(max_length=1024)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)  #CASCADE pas sur !
    created_time = models.DateTimeField(auto_now_add=True)
"""