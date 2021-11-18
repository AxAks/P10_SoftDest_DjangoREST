from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_list_or_404

from projects.models import Project, Contributor, Issue, Comment
from projects.lib_projects import find_obj
from projects.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

from projects.permissions import IsProjectCreator, IsProjectManager, IsProjectContributor,\
    IsIssueAuthor, IsCommentAuthor


class ProjectsModelViewSet(ModelViewSet):
    """
    Endpoint for Projects
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def list(self, request, *args, **kwargs):
        """
        enables an authenticated user to list all the projects he is part of.
        """
        user = request.user
        projects = get_list_or_404(self.queryset.filter(contributor__user=user.id))

        serializer = self.serializer_class(projects, many=True)
        return Response({'projects': serializer.data})

    def create(self, request, *args, **kwargs):
        """
        enables an authenticated user to create a new project
        """
        project = request.data
        user = request.user
        project_copy = project.copy()
        project_copy['author'] = user.id
        serializer = self.serializer_class(data=project_copy)
        serializer.is_valid(raise_exception=True)
        project_obj = serializer.save()
        project_creator = Contributor(user=user, project=project_obj, role='Creator')
        project_creator.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific project by ID
        """
        project_id = kwargs['id_project']
        project = find_obj(Project, project_id)
        if IsProjectContributor:   # pb marche pas, voir pourquoi !
            serializer = self.serializer_class(project)
            return Response(serializer.data)
        else:
            return Response('Insufficient permissions. '
                            'You must be a contributor to the project',
                            status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, **kwargs):
        """
        # Enables the user to update the information of a specific project
        """
        project_id = kwargs['id_project']
        project = find_obj(Project, project_id)
        if IsProjectCreator or IsProjectManager:
            project.title = request.data['title'] if 'title' in request.data.keys() else project.title
            project.description = request.data['description'] \
                if 'description' in request.data.keys() else project.description
            project.type = request.data['type'] if 'type' in request.data.keys() else project.type

            project.save()
            serializer = self.serializer_class(project)
            return Response(serializer.data)
        else:
            return Response('Insufficient permissions. '
                            'You must be the project creator or manager',
                            status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, **kwargs): # seul projects managers et creator !!
        """
        Enables the user to delete a given project and all related issues
        """
        project_id = kwargs['id_project']
        project = find_obj(Project, project_id)
        if IsProjectCreator or IsProjectManager:
            project.delete()
            serializer = self.serializer_class(project)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Insufficient permissions. '
                            'You must be the project creator or manager',
                            status=status.HTTP_401_UNAUTHORIZED)


class ContributorModelViewSet(ModelViewSet):
    """
    End point for contributors
    """
    permission_classes = (IsProjectContributor, )
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    def list(self, request, **kwargs):
        """
        List all contributors of a given project
        """
        project_id = kwargs['id_project']
        find_obj(Project, project_id)
        contributors = get_list_or_404(self.queryset.filter(project_id=project_id))
        serializer = self.serializer_class(contributors, many=True)
        return Response({'contributors': serializer.data})

    def create(self, request, **kwargs):
        """
        Add a contributor to a given project
        """
        project_id = kwargs['id_project']
        find_obj(Project, project_id)
        if IsProjectCreator or IsProjectManager: # ne fonctionne pas !!!
            contributor = request.data
            contributor_copy = contributor.copy()
            contributor_copy['project'] = project_id
            serializer = self.serializer_class(data=contributor_copy)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Insufficient permissions. '
                            'You must be the project creator or manager',
                            status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific contributor to a project by the user's ID
        """
        project_id = kwargs['id_project']
        project = get_object_or_404(find_obj(Project, project_id))
        contributor_id = kwargs['id_user']
        contributor = get_object_or_404(Contributor.objects.filter(project=project, user_id=contributor_id))
        serializer = self.serializer_class(contributor)
        return Response(serializer.data)

    def destroy(self, request, **kwargs):
        """
        remove users from a given project
        """
        project_id = kwargs['id_project']
        contributor_id = kwargs['id_user']
        contributor = get_object_or_404(Contributor.objects.get(project_id=project_id, user_id=contributor_id)) # pb si pas de correspondance !! à gérer
        contributor.delete()
        serializer = self.serializer_class(contributor)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class IssueModelViewSet(ModelViewSet):
    """
    End point for issues
    """
    permission_classes = (IsProjectContributor,)
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

    def list(self, request, **kwargs):
        """
        Lists all issue of a given project
        """
        issues = get_list_or_404(self.queryset.filter(project=kwargs['id_project']))
        serializer = self.serializer_class(issues, many=True)
        return Response({'issues': serializer.data})

    def create(self, request, **kwargs):
        """
        Adds an issue to a given project
        """
        project = kwargs['id_project']
        user = request.user
        issue = request.data
        issue_copy = issue.copy()
        issue_copy['author'], issue_copy['project'] = user.id, project
        serializer = self.serializer_class(data=issue_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific issue by ID
        """
        issue_id = kwargs['id_issue']
        issue = find_obj(Issue, issue_id)
        serializer = self.serializer_class(issue)
        return Response(serializer.data) if serializer.data else Response("No issue to display")

    def update(self, request, **kwargs):
        """
        Updates a specific issue
        """
        issue_id = kwargs['id_issue']
        issue = get_object_or_404(find_obj(Issue, issue_id))
        if IsIssueAuthor:
            issue.title = request.data['title'] if 'title' in request.data.keys() else issue.title
            issue.description = request.data['description'] \
                if 'description' in request.data.keys() else issue.description
            issue.tag = request.data['tag'] if 'tag' in request.data.keys() else issue.tag
            issue.priority = request.data['priority'] if 'priority' in request.data.keys() else issue.priority
            issue.status = request.data['status'] if 'status' in request.data.keys() else issue.status
            issue.assignee = request.data['assignee'] if 'assignee' in request.data.keys() else issue.assignee

            issue.save()
            serializer = self.serializer_class(issue)
            return Response(serializer.data)
        else:
            return Response('Insufficient permissions. You must be the Issue Author',
                            status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, **kwargs):
        """
        Remove a contributor from a Project
        """
        issue_id = kwargs['id_issue']
        issue = get_object_or_404(find_obj(Issue, issue_id))   # pb si pas de correspondance !! à gérer
        if IsIssueAuthor:
            issue.delete()
            serializer = self.serializer_class(issue)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Insufficient permissions. You must be the Issue Author',
                            status=status.HTTP_401_UNAUTHORIZED)


class CommentModelViewSet(ModelViewSet):
    """
    End point for comments
    """
    permission_classes = (IsProjectContributor, )
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def list(self, request, **kwargs):
        """
        Lists all comments on a project related issue
        """
        project = get_object_or_404(ProjectsModelViewSet.queryset.filter(id=kwargs['id_project'])) # peut-etre superflu
        issue = get_object_or_404(IssueModelViewSet.queryset.filter(project=project)) # si je passe ici kwargs['id_issue']
        comments = get_list_or_404(self.queryset.filter(issue=issue))
        serializer = self.serializer_class(comments, many=True)
        return Response({'comments': serializer.data})

    def create(self, request, **kwargs):
        """
        Add a comment to a project-related issue
        """
        user = request.user
        project = get_object_or_404(Project.objects.filter(id=kwargs['id_project'])) # peut-etre superflu
        issue = get_object_or_404(Issue.objects.filter(project=project)) # si je passe ici kwargs['id_issue']
        comment = request.data
        comment_copy = comment.copy()
        comment_copy['author'], comment_copy['project'], comment_copy['issue'] = user.id, project.id, issue.id
        serializer = self.serializer_class(data=comment_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific Comment on a issue by ID
        """
        comment_id = kwargs['id_comment']
        comment = find_obj(Comment, comment_id)
        serializer = self.serializer_class(comment)
        return Response(serializer.data)

    def update(self, request, **kwargs):
        """
        Updates a specific Comment on a issue by ID
        """
        comment_id = kwargs['id_comment']
        comment = find_obj(Comment, comment_id)
        if IsCommentAuthor:
            comment.description = request.data['description'] \
                if 'description' in request.data.keys() else comment.description

            comment.save()
            serializer = self.serializer_class(comment)
            return Response(serializer.data)
        else:
            return Response('Insufficient permissions. '
                            'You must be the comment author',
                            status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, **kwargs):
        """
        Deletes a specific Comment on a issue by ID
        """
        comment_id = kwargs['id_comment']
        comment = find_obj(Comment, comment_id)
        if IsCommentAuthor:
            comment.delete()
            serializer = self.serializer_class(comment)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Insufficient permissions. '
                            'You must be the comment author',
                            status=status.HTTP_401_UNAUTHORIZED)
