from django.urls import path

from projects.models import Project
from projects.views import ProjectsAPIView, SpecificProjectAPIView, ContributorAPIView, SpecificContributorAPIView

app_name = "projects"

urlpatterns = [
    path('', ProjectsAPIView.as_view()),
    path('<int:id>', SpecificProjectAPIView.as_view()),
    path('<int:project>/users/', ContributorAPIView.as_view()),  #  POST : add user to project, GET: list project's users
    path('<int:project>/users/<int:id>', SpecificContributorAPIView.as_view()),  # DELETE : remove user from project
]
"""
path('<int:id>/issues', SpecificProjectAPIView.as_view()), # GET: list projet's issues POST: add/edit issue to project 
path('<int:id>/issues/<int:id>', SpecificProjectAPIView.as_view()), # PUT : edit issue DELETE: delete issue
path('<int:id>/issues/<int:id>/comments', SpecificProjectAPIView.as_view()), POST: add comment to project GET: list project's comments
path('<int:id>/issues/<int:id>/comments/<int:id>', SpecificProjectAPIView.as_view()), GET : get specific commment, PUT: edit comment, delete: delete comment
"""
