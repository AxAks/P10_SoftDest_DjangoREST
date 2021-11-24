from django.urls import path
from projects.views import ProjectModelViewSet, ContributorModelViewSet, IssueModelViewSet, CommentModelViewSet

app_name = "projects"


urlpatterns = [
    path('', ProjectModelViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
    path('<int:id_project>', ProjectModelViewSet.as_view({
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
    path('<int:id_project>/issues/<int:id_issue>/comments/', CommentModelViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })),
    path('<int:id_project>/issues/<int:id_issue>/comments/<int:id_comment>', CommentModelViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })),
]
