from django.urls import path
from projects.views import ProjectsModelViewSet, ContributorModelViewSet, IssueModelViewSet, CommentModelViewSet

app_name = "projects"


urlpatterns = [
    path('', ProjectsModelViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
    path('<int:id_project>', ProjectsModelViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })),
    path('<int:id_project>/users/', ContributorModelViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })),
    path('<int:id_project>/users/<int:id_user>', ContributorModelViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })),

    path('<int:id_project>/issues/', IssueModelViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })),
    path('<int:id_project>/issues/<int:id_issue>', IssueModelViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })),
    path('<int:id_project>/issues/<int:issue>/comments/', CommentModelViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })),
    path('<int:id_project>/issues/<int:issue>/comments/<int:id_comment>', CommentModelViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })),
]
