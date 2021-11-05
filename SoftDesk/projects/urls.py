from django.urls import path
from projects.views import ProjectsAPIView, SpecificProjectAPIView,\
    ContributorAPIView, SpecificContributorAPIView, IssueAPIView, SpecificIssueAPIView, CommentAPIView, SpecificCommentAPIView

app_name = "projects"

urlpatterns = [
    path('', ProjectsAPIView.as_view()),
    path('<int:id>', SpecificProjectAPIView.as_view()),
    path('<int:project>/users/', ContributorAPIView.as_view()),
    path('<int:project>/users/<int:id>', SpecificContributorAPIView.as_view()),
    path('<int:project>/issues/', IssueAPIView.as_view()),
    path('<int:project>/issues/<int:id>', SpecificIssueAPIView.as_view()),
    path('<int:project>/issues/<int:issue>/comments/', CommentAPIView.as_view()),
    path('<int:project>/issues/<int:issue>/comments/<int:id>', SpecificCommentAPIView.as_view()),
]
