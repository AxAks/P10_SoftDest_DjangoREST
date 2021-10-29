from django.urls import path

from projects.views import ProjectsAPIView

app_name = "projects"

urlpatterns = [
    path('', ProjectsAPIView.as_view()),
]
