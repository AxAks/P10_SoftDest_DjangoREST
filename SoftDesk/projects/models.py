from django.db import models
from SoftDesk import settings
from constants import PROJECT_TYPES, CONTRIBUTOR_ROLES, ISSUE_TAGS, ISSUE_STATUSES, ISSUE_PRIORITIES


class Project(models.Model):
    """
    Model for a project
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=10, choices=PROJECT_TYPES)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.type}) by {self.author}"

    objects = models.Manager()


class Contributor(models.Model):
    """
    Model through linking users to projects
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='project_contributor',
                             on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=CONTRIBUTOR_ROLES)

    def __str__(self):
        return f'{self.user}: {self.role} for {self.project}'

    objects = models.Manager()


class Issue(models.Model):
    """
    Model for the project-related issues
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    tag = models.CharField(max_length=10, choices=ISSUE_TAGS)
    priority = models.CharField(max_length=10, choices=ISSUE_PRIORITIES)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ISSUE_STATUSES)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='issue_author',
                               on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='issue_assignee',
                                 blank=True, null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.tag}: {self.priority}) by {self.author} for Project "{self.project.title}"'

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

    def __str__(self):
        return f'{self.description} by {self.author} for issue "{self.issue.title}"'

    objects = models.Manager()
