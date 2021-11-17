from django.urls import path
from projects.views import ProjectsModelViewSet, ContributorModelViewSet, SpecificProjectModelViewSet, \
    SpecificContributorModelViewSet, IssueAPIView, SpecificIssueAPIView, CommentAPIView, \
    SpecificCommentAPIView

app_name = "projects"


urlpatterns = [
    path('', ProjectsModelViewSet.as_view(
        {
            'get': 'list',
            'post': 'create'
        }
    )),
    path('<int:id_project>', SpecificProjectModelViewSet.as_view({
            'get': 'list',
            'put': 'update',
            'delete': 'destroy'
        })),
    path('<int:id_project>/users/', ContributorModelViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })),
    path('<int:id_project>/users/<int:id_user>', SpecificContributorModelViewSet.as_view({
            'get': 'list',
            'delete': 'destroy'
        })),
    path('<int:id_project>/issues/', IssueAPIView.as_view()),
    path('<int:id_project>/issues/<int:id_issue>', SpecificIssueAPIView.as_view()),
    path('<int:id_project>/issues/<int:issue>/comments/', CommentAPIView.as_view()),
    path('<int:id_project>/issues/<int:issue>/comments/<int:id_comment>', SpecificCommentAPIView.as_view()),
]
