from django.urls import path

from projects.views import ProjectsAPIView, SpecificProjectAPIView

app_name = "projects"

urlpatterns = [
    path('', ProjectsAPIView.as_view()),
    path('<int:id>', SpecificProjectAPIView.as_view()),
]
